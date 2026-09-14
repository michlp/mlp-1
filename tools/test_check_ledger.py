#!/usr/bin/env python3
"""Prove every check in check_ledger.py fires.

Each case mutates the known-good example so that exactly one check should
fail, then asserts that it does. A check that never fails is worthless.

    ./tools/test_check_ledger.py
"""
import copy, json, pathlib, shutil, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parent
EX = ROOT / "example"
CHECKER = ROOT / "check_ledger.py"


def run(tmp):
    r = subprocess.run([sys.executable, str(CHECKER),
                        str(tmp / "appeal-deadline.ledger.json"), "--json"],
                       capture_output=True, text=True)
    return json.loads(r.stdout)


def failed_checks(result):
    return {c["check"] for c in result["checks"] if not c["ok"]}


def case(name, want, mutate):
    with tempfile.TemporaryDirectory() as d:
        tmp = pathlib.Path(d) / "example"
        shutil.copytree(EX, tmp)
        lp = tmp / "appeal-deadline.ledger.json"
        rp = tmp / "restatement" / "appeal-deadline.md"
        ledger = json.loads(lp.read_text())
        text = rp.read_text()
        ledger, text = mutate(copy.deepcopy(ledger), text)
        lp.write_text(json.dumps(ledger, indent=2))
        rp.write_text(text)
        got = failed_checks(run(tmp))
        ok = want in got
        print(f"  {'PASS' if ok else 'FAIL'}  check {want:>2} fires on: {name}"
              + ("" if ok else f"   (failed: {sorted(got) or 'none'})"))
        return ok


CASES = [
 ("a sentence over the R2 word cap", 1,
  lambda l, t: (l, t + "\n\n" + " ".join(["word"] * 34) + ".\n")),
 ("a prohibited word", 2,
  lambda l, t: (l, sub(t, "must be filed with", "must be filed pursuant to"))),
 ("a bare shall outside a quotation", 3,
  lambda l, t: (l, sub(t, "must be filed", "shall be filed"))),
 ("a semicolon", 4,
  lambda l, t: (l, sub(t, "file the notice.", "file the notice; the clerk does not."))),
 ("and/or", 5,
  lambda l, t: (l, sub(t, "a duty or states", "a duty and/or states"))),
 ("a contraction", 6,
  lambda l, t: (l, sub(t, "does not state", "doesn't state"))),
 ("a Latin abbreviation", 8,
  lambda l, t: (l, sub(t, "in a civil case", "in a civil case, e.g. an appeal"))),
 ("a dropped citation", 10,
  lambda l, t: (l, sub(t, "Fed. R. App. P. 3 and", ""))),
 ("a dropped numeral", 11,
  lambda l, t: (l, sub(t, "within 30 days", ""))),
 ("a defined term missing from the restatement", 12,
  lambda l, t: (_set(l, 0, "defined_terms", ["Appellate Record"]), t)),
 ("a dropped quantifier", 13,
  lambda l, t: (_set(l, 0, "quantifiers", ["each"]), t)),
 ("a subsection designation never cited", 15,
  lambda l, t: (_set(l, 0, "locus", "9(z)(99)"), t)),
 ("a flagged proposition with no marking sentence", 16,
  lambda l, t: (l, sub(t, "The rule does not state who must file the notice.", ""))),
 ("an operator stronger than the source's", 17,
  lambda l, t: (_set(_set(l, 0, "construction", "directory"),
                     0, "operator", "must"), t)),
 ("a mapping made on a contested construction", 17,
  lambda l, t: (_set(l, 2, "operator", "must"), t)),
 ("an unknown construction value", 17,
  lambda l, t: (_set(l, 0, "construction", "sort of mandatory"), t)),
 ("a sentence no proposition claims", 18,
  lambda l, t: (l, t + "\n\nThe clerk will also notify the parties by email.\n")),
 ("front matter that is no longer exempt", 18,
  lambda l, t: (_front(l, []), t)),
 ("a carried_by snippet that matches nothing", 18,
  lambda l, t: (_set(l, 0, "carried_by", ["no such sentence exists here"]), t)),
 ("a declared series missing its serial comma", 7,
  lambda l, t: (_carry(_series(l, 0, "AND",
                               ["the notice", "the brief", "the exhibits"]),
                       0, ["The clerk files the notice"]),
                t + "\n\nThe clerk files the notice, the brief and the exhibits.\n")),
 ("a declared series whose connector is absent", 14,
  lambda l, t: (_carry(_series(l, 0, "OR",
                               ["alpha", "beta", "gamma"]),
                       0, ["The clerk files alpha"]),
                t + "\n\nThe clerk files alpha, beta, and gamma.\n")),
]


def sub(text, phrase, repl):
    """Replace ignoring how the source file wrapped its lines."""
    import re
    pat = r'\s+'.join(re.escape(w) for w in phrase.split())
    out, n = re.subn(pat, repl, text, count=1)
    assert n == 1, f"mutation did not apply: {phrase!r}"
    return out


def _front(ledger, val):
    ledger["front_matter"] = val
    return ledger


def _set(ledger, idx, key, val):
    ledger["propositions"][idx][key] = val
    return ledger


def _carry(ledger, idx, refs):
    ledger["propositions"][idx]["carried_by"] = refs
    return ledger


def _series(ledger, idx, connector, items):
    p = ledger["propositions"][idx]
    p["series"] = {"connector": connector, "items": items}
    return ledger


def _all_connector(ledger, val):
    for p in ledger["propositions"]:
        p["connector"] = val
    return ledger


def main():
    print("Baseline: the unmutated example must pass everything")
    with tempfile.TemporaryDirectory() as d:
        tmp = pathlib.Path(d) / "example"
        shutil.copytree(EX, tmp)
        base = failed_checks(run(tmp))
    print(f"  {'PASS' if not base else 'FAIL'}  clean example has no failures"
          + ("" if not base else f"   (failed: {sorted(base)})"))
    print("\nEach mutation must trip its own check")
    results = [not base] + [case(n, w, m) for n, w, m in CASES]
    bad = results.count(False)
    print(f"\n{len(results) - bad}/{len(results)} passed.")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
