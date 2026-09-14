#!/usr/bin/env python3
"""Run MLP-1 Part 3 mechanical checks against a proposition ledger.

    ./tools/check_ledger.py <ledger.json>
    ./tools/check_ledger.py <ledger.json> --style-only   # checks 1-9
    ./tools/check_ledger.py <ledger.json> --json         # machine-readable

Checks 1 through 9 are style checks and need only the restatement.
Checks 10 through 17 are fidelity checks and run against the ledger.

Exits non-zero on any failure, so it can gate a release.

The checker has no independent view of the source. A ledger that omits a
proposition is a ledger this tool calls complete. Decomposition is human
work, and so is the Level 3 signature.

Format: tools/LEDGER.md
"""
import argparse, hashlib, json, pathlib, re, sys

OPERATORS = ["must not", "may not", "need not", "is not entitled to",
             "is entitled to", "must", "may", "will"]

STRENGTH = {"must": 4, "must not": 4, "may not": 3, "is entitled to": 3,
            "will": 2, "may": 1, "need not": 0, "is not entitled to": 0}

# A construction the checker understands. "declaratory" covers a shall that
# states an amount, a status, or what is treated as what -- it maps to the
# simple present, so it carries no operator at all.
KNOWN_CONSTRUCTIONS = {"mandatory", "directory", "permissive", "declaratory",
                       "conditional", "contested", "unverified", None}

# Constructions that forbid an operator: either the mapping cannot be
# established, or the source sentence is not deontic in the first place.
NO_OPERATOR = {"contested", "unverified", "declaratory", "conditional"}

SOURCE_STRENGTH = {
    ("shall", "mandatory"): 4, ("shall", "directory"): 1,
    ("must", "mandatory"): 4, ("shall not", "mandatory"): 4,
    ("must not", "mandatory"): 4, ("shall not", "directory"): 3,
    ("may", "permissive"): 1, ("should", None): 1,
    ("shall not be required", "permissive"): 0,
    ("shall not be required", "mandatory"): 0,
    ("is entitled to", None): 3, ("is not required to", None): 0,
    ("need not", None): 0,
}

CAPS = {"R1": 30, "R2": 30, "R3": 25, "R4": 20}

QUANTIFIERS = ["each", "any", "all", "every", "some", "one or more",
               "at least", "no more than", "not fewer than", "only",
               "solely", "exclusively"]

LATIN_ABBR = ["inter alia", "e.g.", "i.e.", "etc.", "viz.", "supra", "infra"]

PROHIBITED = ["aforesaid", "herein", "hereinafter", "hereby", "thereof",
              "thereto", "thereunder", "whereas", "pursuant to", "prior to",
              "subsequent to", "utilize", "commence", "endeavor", "forthwith",
              "in the event that", "with respect to", "set forth", "said "]

FLAGS_NEEDING_MARK = {"AMBIGUOUS", "AGENT UNSTATED", "GAP", "OPERATOR CONTESTED",
                      "CONFLICT"}

# A marker has to answer the flag it is paired with. Accepting any marker
# let one flag's sentence satisfy another flag, which is how an unmarked
# agent gap slipped past this check.
FLAG_MARKERS = {
    "AGENT UNSTATED": ["does not state who", "does not say who",
                       "does not name who", "does not identify who",
                       "no actor", "does not state the actor"],
    "GAP": ["does not state", "does not address", "does not define",
            "does not limit", "no consequence", "does not say"],
    "AMBIGUOUS": ["is not clear", "not clear whether", "more than one",
                  "does not resolve", "not resolved", "ambiguous"],
    "OPERATOR CONTESTED": ["have divided", "has divided", "construed",
                           "does not resolve", "not settled"],
    "CONFLICT": ["conflict", "inconsistent", "cannot be reconciled"],
}


# Part 3's blocking and advisory distinction. A failure blocks where it
# changes what the text says or conceals that something is unsaid. Where the
# text still says the same thing, it is recorded and queues editorial review.
# Vetoing a semicolon as hard as a softened operator rejects sound work.
ADVISORY_CHECKS = {1, 2, 4, 6, 8, 9}     # length, wording, punctuation, register
BLOCKING_CHECKS = {3, 5, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19}


class Report:
    def __init__(self):
        self.rows = []

    def add(self, num, label, ok, detail="", advisory=None):
        if advisory is None:
            advisory = num in ADVISORY_CHECKS
        self.rows.append({"check": num, "label": label, "ok": bool(ok),
                          "detail": detail, "advisory": advisory})

    @property
    def failed(self):
        return [r for r in self.rows if not r["ok"] and not r["advisory"]]

    @property
    def review(self):
        return [r for r in self.rows if not r["ok"] and r["advisory"]]


def sentences(text):
    """Split a restatement into numbered sentences.

    An explicit {#R3} marker wins. Otherwise mask the abbreviation periods
    that legal citations are full of, split on what is left, and restore.
    Lookbehind guards do not work here: the split point sits after the
    period, so the guard never sees the abbreviation it is meant to protect.
    """
    text = re.sub(r'^\s*#.*$', '', text, flags=re.M)          # headings
    # A list item is a unit of its own. Flattening first ran the whole list
    # together as one sentence, which read as a 75-word cap violation.
    text = re.sub(r'\n\s*[-*+]\s+', '\n\x01', text)
    text = re.sub(r'[ \t]+', ' ', text)
    items = [seg.strip() for seg in text.split('\x01')]
    text = ' \x02 '.join(re.sub(r'\s+', ' ', i).strip() for i in items if i.strip())
    if re.search(r'\{#R\d+\}', text):
        out = {}
        for m in re.finditer(r'(.+?)\s*\{#(R\d+)\}', text):
            out[m.group(2)] = m.group(1).strip()
        return out

    ABBR = ["Fed", "R", "App", "Civ", "Crim", "Evid", "P", "U.S.C", "U.S",
            "Stat", "Ct", "No", "Nos", "v", "Pub", "L", "Inc", "Co", "Corp",
            "Cir", "Supp", "Ann", "Rev", "Mich", "Cal", "N.D", "S.D", "E.D",
            "W.D", "Jan", "Feb", "Mar", "Apr", "Jun", "Jul", "Aug", "Sept",
            "Sep", "Oct", "Nov", "Dec", "al", "seq", "art", "sec", "subsec"]
    DOT = "\x00"
    masked = text
    for a in sorted(ABBR, key=len, reverse=True):
        masked = re.sub(r'(?<![\w.])' + re.escape(a) + r'\.',
                        a + DOT, masked)
    masked = re.sub(r'(?<=\b[A-Z])\.(?=\s*[A-Z]\.)', DOT, masked)
    # A middle initial is not a sentence end: "Chancellor Anne C. Martin"
    # was splitting after the initial.
    masked = re.sub(r'(?<=\b[A-Z])\.(?=\s+[A-Z][a-z])', DOT, masked)

    chunks = [c for c in masked.split('\x02') if c.strip()]
    parts = []
    for c in chunks:
        parts += [x.strip() for x in
                  re.split(r'(?<=[.!?])\s+(?=[A-Z"\u201c])', c) if x.strip()]
    parts = [x.replace(DOT, ".").strip() for x in parts]
    return {f"R{i}": x for i, x in enumerate(parts, 1)}


def source_hash(path):
    """SHA-256 of the source, normalized only for line endings.

    Part 3's version binding specifies exactly this. Normalizing anything
    else would let a real change in the source pass as unchanged.
    """
    raw = pathlib.Path(path).read_bytes()
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def resolve_refs(refs, sents):
    """Map carried_by entries to sentence ids.

    An entry is either a sentence id ("R7") or a snippet of the sentence it
    points at. Snippets survive renumbering: splitting one sentence shifts
    every id below it, which silently repointed carried_by three times
    before this existed.
    """
    out, missing = [], []
    for r in refs or []:
        if re.fullmatch(r'R\d+', str(r)):
            (out if r in sents else missing).append(r)
            continue
        want = norm(str(r))
        hit = [k for k, v in sents.items() if want in norm(v)]
        if len(hit) == 1:
            out.append(hit[0])
        elif not hit:
            missing.append(f'snippet not found: {str(r)[:40]!r}')
        else:
            missing.append(f'snippet ambiguous ({len(hit)} matches): {str(r)[:34]!r}')
    return out, missing


def count_words(s):
    """Rule 9.7: a citation, quotation, date, defined term or parenthetical
    counts as one word."""
    s = re.sub(r'"[^"]*"|“[^”]*”', ' X ', s)     # quotations
    # A rule citation is one word, subdivisions included. Collapsing these
    # before the generic parenthetical rule matters: "Rule 29(d)(3)(A)" was
    # scoring 4 and pushing faithful sentences over the cap.
    s = re.sub(r'\b(?:Rule|Rules)\s+\d+(?:\.\d+)?(?:\([^)]*\))*', ' X ', s)
    s = re.sub(r'\b§+\s*[\d\-.]+(?:\([^)]*\))*', ' X ', s)
    s = re.sub(r'\([^)]*\)', ' X ', s)                           # parentheticals
    s = re.sub(r'\b\d+\s+U\.S\.C\.\s+§+\s*[\d\-.()]+', ' X ', s)
    s = re.sub(r'\bFed\.\s*R\.\s*\w+\.\s*P\.\s*[\d\w().]+', ' X ', s)
    s = re.sub(r'\b[A-Z][A-Za-z.]*\s+v\.\s+[A-Z][A-Za-z.]*', ' X ', s)
    s = re.sub(r'\b(?:January|February|March|April|May|June|July|August|'
               r'September|October|November|December)\s+\d{1,2},\s*\d{4}', ' X ', s)
    s = re.sub(r'\b\d+\s+(?:days?|months?|years?|percent)\b', ' X ', s)
    return len([w for w in s.split() if re.search(r'\w', w)])


def operator_in(sentence):
    low = sentence.lower()
    for op in OPERATORS:                      # longest-first ordering matters
        if re.search(r'(?<![\w-])' + re.escape(op) + r'(?![\w-])', low):
            return op
    return None


def norm(t):
    return re.sub(r'\s+', ' ', t.lower().replace('’', "'")).strip()


def run(ledger, root, style_only=False):
    rep = Report()
    reg = ledger.get("register", "R2")
    cap = CAPS.get(reg, 30)
    rst_path = (root / ledger["restatement_file"])
    rst_text = rst_path.read_text(encoding="utf-8")
    sents = sentences(rst_text)
    body = norm(rst_text)
    props = ledger.get("propositions", [])

    # ---------------------------------------------------- style, 1-9
    over = [f"{k} ({count_words(v)}w)" for k, v in sents.items()
            if count_words(v) > cap]
    rep.add(1, f"no sentence over the {reg} cap of {cap} words", not over,
            ", ".join(over[:4]))

    unquoted = re.sub(r'"[^"]*"|“[^”]*”', ' ', rst_text).lower()
    hits = [w for w in PROHIBITED
            if re.search(r'(?<![\w-])' + re.escape(w), unquoted)]
    rep.add(2, "no prohibited word outside a quotation", not hits,
            ", ".join(hits[:5]))

    strays = []
    for w in ["shall", "should", "ought to", "is required to", "is obligated to",
              "is permitted to", "has the right to"]:
        if re.search(r'(?<![\w-])' + re.escape(w) + r'(?![\w-])', unquoted):
            strays.append(w)
    rep.add(3, "no word outside the seven operators used as an operator",
            not strays, ", ".join(strays))

    rep.add(4, "no semicolon outside a quotation", ";" not in unquoted)
    rep.add(5, "no and/or outside a quotation", "and/or" not in unquoted)
    contractions = re.findall(
        r"\b(?:can|could|would|should|do|does|did|is|are|was|were|has|have|had|"
        r"will|must|ain)n['’]t\b|\b(?:it|that|there|here|what|who|he|she|"
        r"they|we|you|i)['’](?:s|re|ve|ll|d|m)\b", unquoted)
    rep.add(6, "no contraction", not contractions,
            ", ".join(sorted(set(contractions))[:4]))

    # A three-item list carries one comma: "A, B and C". Requiring two
    # commas missed exactly the case the rule exists for.
    # Work clause by clause. Matching a span instead truncated at the first
    # "or" inside an item and reported a list that did carry its comma.
    missing_serial = []
    flat = re.sub(r'\s+', ' ', rst_text)
    for clause in re.split(r'[.;:]\s+', flat):
        if ',' not in clause:
            continue
        joins = list(re.finditer(r'\s(?:and|or)\s', clause))
        if not joins:
            continue
        last = joins[-1]
        if not clause[:last.start()].rstrip().endswith(','):
            missing_serial.append(clause.strip()[:44])
    # Advisory. Telling a list's terminating conjunction from one inside an
    # item needs parsing, not a regex: "the applicant, appellant, or counsel
    # for the applicant or appellant" carries its serial comma correctly and
    # still trips every pattern simple enough to write. Reported for review.
    # A declared series makes this decidable: the ledger says what the items
    # are and what binds them, so the check stops guessing whether prose is
    # a list and asks whether the text carries the list the ledger declares.
    series_bad = []
    if not style_only:
        for p_ in props:
            ser = p_.get("series")
            if not ser or len(ser.get("items", [])) < 3:
                continue
            ids, _ = resolve_refs(p_.get("carried_by"), sents)
            for i in ids:
                sent = sents[i]
                low = norm(sent)
                if sum(1 for it in ser["items"] if norm(it) in low) < 3:
                    continue                      # not the run-in sentence
                if not re.search(r',\s*(?:and|or)\b', sent, re.I):
                    series_bad.append(f'{p_["id"]}:{i}')
    detail = "; ".join(series_bad[:3])
    if missing_serial:
        detail += ("  |  candidates for review: "
                   + "; ".join(missing_serial[:2]))
    rep.add(7, "serial comma in every declared series", not series_bad,
            detail.strip(" |"))

    lat = [a for a in LATIN_ABBR if a in unquoted]
    rep.add(8, "no Latin abbreviation", not lat, ", ".join(lat))

    lead = [k for k, v in sents.items()
            if re.match(r'^(And|But|Or|So|However|Therefore|Thus|Moreover)\b', v)]
    rep.add(9, "no sentence-initial connective in R1 text",
            reg != "R1" or not lead, ", ".join(lead[:3]))

    if style_only:
        return rep, sents

    # ------------------------------------------------ fidelity, 10-17
    src_text = " ".join(
        (root / s["text_file"]).read_text(encoding="utf-8")
        for s in ledger["sources"])
    src_norm = norm(src_text)

    miss = [c for p in props for c in p.get("citations", [])
            if norm(c) not in body]
    rep.add(10, "every citation appears in the restatement, in the same form",
            not miss, ", ".join(miss[:4]))

    miss = [n for p in props for n in p.get("numerals", [])
            if norm(n) not in body
            and not re.search(re.escape(norm(n).split()[0]) + r'\b', body)]
    rep.add(11, "every numeral appears, or its absence is explained",
            not miss, ", ".join(miss[:4]))

    miss = [d for p in props for d in p.get("defined_terms", [])
            if d not in rst_text]
    rep.add(12, "every defined term appears in its exact form",
            not miss, ", ".join(miss[:4]))

    miss = [q for p in props for q in p.get("quantifiers", [])
            if not re.search(r'(?<![\w-])' + re.escape(norm(q)) + r'(?![\w-])',
                             body)]
    rep.add(13, "every quantifier appears in the restatement",
            not miss, ", ".join(miss[:4]))

    # Counting every "and" and "or" in the prose compared nothing useful:
    # "applicant or appellant" is one item, not a disjunction of propositions.
    # Require instead that each proposition's connector appears in the text
    # that carries it.
    lost_conn = []
    for p in props:
        c = p.get("connector")
        if c not in ("AND", "OR"):
            continue
        ids, _ = resolve_refs(p.get("carried_by"), sents)
        carried = [sents[i] for i in ids]
        pool = norm(" ".join(carried)) if carried else body
        word = "and" if c == "AND" else "or"
        if not re.search(r'(?<![\w-])' + word + r'(?![\w-])', pool):
            lost_conn.append(f'{p["id"]}:{c}')
    # Advisory. A connector between propositions need not surface as the word
    # itself: two amounts stated in consecutive sentences are disjunctive by
    # structure, with no "or" anywhere. Deciding this needs the restatement
    # parsed into propositions, which is the work the ledger exists to record.
    # Declared series are decidable the same way: the connector binding the
    # items has to appear in the text that carries them, whether run-in or
    # in a vertical list's stem.
    series_conn = []
    for p_ in props:
        ser = p_.get("series")
        if not ser or not ser.get("connector"):
            continue
        # Rule 4.4 puts the connector in the introductory text, and its
        # prescribed forms are phrases, not the bare word: a vertical list
        # binds with "all of the following", never with a trailing "and".
        forms = ({"and", "and both", "all of the following",
                  "each of the following", "both of the following"}
                 if ser["connector"] == "AND" else
                 {"or", "or both", "any of the following",
                  "one or more of the following", "either"})
        ids, _ = resolve_refs(p_.get("carried_by"), sents)
        pool = norm(" ".join(sents[i] for i in ids)) if ids else body
        ok = any(re.search(r'(?<![\w-])' + re.escape(f) + r'(?![\w-])', pool)
                 for f in forms)
        if not ok:
            series_conn.append(f'{p_["id"]}:{ser["connector"]}')
    detail = ", ".join(series_conn[:4])
    if lost_conn:
        detail += ("  |  undeclared, for review: " + ", ".join(lost_conn[:3]))
    rep.add(14, "each declared series carries its connector", not series_conn,
            detail.strip(" |"))

    # Scan forward from the last match. Searching from position 0 each time
    # found "5-6-6" inside the document's own heading citation, ahead of
    # every other locus, and called a correctly ordered document unordered.
    # With several instruments the same subdivision number appears in each --
    # both Tennessee orders have a "3. Case Assignment, a. Request for
    # Designation" -- so a bare locus does not identify a provision. A source
    # may declare a short_ref ("the 2017 order"), and a proposition satisfies
    # this check by carrying either its locus or its source's short_ref.
    short_ref = {s_["id"]: s_.get("short_ref") for s_ in ledger["sources"]}
    seen_loci, missing_loci, at, order_ok = [], [], 0, True
    for p_ in props:
        l = p_.get("locus")
        if not l or l in seen_loci:
            continue
        seen_loci.append(l)
        i = body.find(norm(l), at)
        if i != -1:
            at = i
            continue
        ref = short_ref.get(p_.get("source"))
        if ref and norm(ref) in body:
            continue                      # identified by instrument instead
        if norm(l) in body:
            order_ok = False
        else:
            missing_loci.append(l)
    rep.add(15, "every subsection designation appears, in the source's order",
            not missing_loci and order_ok,
            ("missing " + ", ".join(missing_loci[:3])) if missing_loci
            else "out of order")

    unmarked = []
    for p in props:
        fl = set(p.get("flags", [])) & FLAGS_NEEDING_MARK
        if not fl:
            continue
        ids, _ = resolve_refs(p.get("carried_by"), sents)
        carried = [sents[i] for i in ids]
        pool = norm(" ".join(carried)) if carried else body
        for f in sorted(fl):
            if not any(m in pool for m in FLAG_MARKERS.get(f, [])):
                unmarked.append(f'{p["id"]}:{f}')
    rep.add(16, "every flagged proposition maps to a marking sentence",
            not unmarked, ", ".join(unmarked[:4]))

    stronger, unmapped, unknown = [], [], []
    for p in props:
        so, con = p.get("source_operator"), p.get("construction")
        op = p.get("operator")
        if con not in KNOWN_CONSTRUCTIONS:
            unknown.append(f'{p["id"]}:{con}')
            continue
        if con in NO_OPERATOR:
            # A conditional carries an operator of its own ("the court may"),
            # so only the source_operator side is non-deontic there.
            if op is not None and con in ("contested", "unverified", "declaratory"):
                unmapped.append(f'{p["id"]} maps {so}->{op} on a {con} construction')
            continue
        if op is None:
            continue
        src_rank = SOURCE_STRENGTH.get((norm(so), con),
                                       SOURCE_STRENGTH.get((norm(so), None)))
        if src_rank is None:
            continue
        if STRENGTH.get(op, 0) > src_rank:
            stronger.append(f'{p["id"]} {so}({con})->{op}')
    # Version binding. Rule 10.9 and Part 3: a document whose source hash no
    # longer matches is marked unverified, not silently republished. Without
    # this the binding is a field nobody verifies.
    hash_bad, hash_missing = [], []
    for src in ledger["sources"]:
        want = (src.get("source_sha256") or "").lower().strip()
        got = source_hash(root / src["text_file"])
        if not want:
            hash_missing.append(src["id"])
        elif want != got:
            hash_bad.append(f'{src["id"]}: recorded {want[:12]}…, source is {got[:12]}…')
    rep.add(19, "every source matches its recorded hash",
            not hash_bad and not hash_missing,
            "; ".join(hash_bad[:3]) if hash_bad
            else ("no source_sha256 recorded for " + ", ".join(hash_missing)))

    # Backward coverage. Part 3 Step 4 maps each restatement sentence back to
    # a proposition; a sentence no proposition claims is added content or an
    # unmapped proposition, and both are defects. Every fidelity failure found
    # while testing this tool came from the backward map, which until now
    # nothing checked.
    claimed = set()
    ref_errors = []
    for p_ in props:
        ids, bad = resolve_refs(p_.get("carried_by"), sents)
        claimed.update(ids)
        ref_errors += [f'{p_["id"]}: {b}' for b in bad]
    # Two kinds of sentence legitimately map to no proposition. Front matter
    # (the register line, the version binding) is apparatus. A gloss is
    # content R3 and R4 REQUIRE and the source does not contain -- flagging
    # a required gloss as added content would be exactly backwards.
    fm_ids, fm_bad = resolve_refs(ledger.get("front_matter"), sents)
    gl_ids, gl_bad = resolve_refs(ledger.get("glosses"), sents)
    fm_bad += gl_bad
    exempt = claimed | set(fm_ids) | set(gl_ids)
    unclaimed = [k for k in sents if k not in exempt]
    rep.add(18, "every restatement sentence maps back to a proposition",
            not unclaimed and not ref_errors,
            "; ".join(([f"unclaimed: {', '.join(unclaimed[:5])}"] if unclaimed else [])
                      + (ref_errors + fm_bad)[:3]))

    rep.add(17, "no operator stronger than the source's",
            not stronger and not unmapped and not unknown,
            "; ".join((stronger + unmapped +
                       [f"unknown construction {u}" for u in unknown])[:4]))
    return rep, sents


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ledger")
    ap.add_argument("--style-only", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    path = pathlib.Path(a.ledger).resolve()
    ledger = json.loads(path.read_text(encoding="utf-8"))
    rep, sents = run(ledger, path.parent, a.style_only)

    if a.json:
        print(json.dumps({"checks": rep.rows,
                          "failed": len(rep.failed),
                          "review": len(rep.review),
                          "sentences": len(sents)}, indent=2))
    else:
        print(f"{path.name} — register {ledger.get('register')}, "
              f"{len(ledger.get('propositions', []))} propositions, "
              f"{len(sents)} sentences\n")
        head = None
        for r in sorted(rep.rows, key=lambda x: x["check"]):
            h = "Style checks (Level 1)" if r["check"] <= 9 else \
                "Fidelity checks (Level 3)"
            if h != head:
                print(("" if head is None else "\n") + h)
                head = h
            mark = "PASS" if r["ok"] else ("REVIEW" if r["advisory"] else "FAIL")
            extra = f" — {r['detail']}" if r["detail"] and not r["ok"] else ""
            print(f"  {mark:<6} {r['check']:>2}. {r['label']}{extra}")
        print()
        if rep.review:
            print(f"{len(rep.review)} advisory failure(s). The text still says "
                  "what the source says;\n  these are recorded and queue "
                  "editorial review (Part 3). They do not block.")
        if rep.failed:
            print(f"{len(rep.failed)} check(s) failed.")
        else:
            print("All checks passed.")
            print("\nThis is not Level 3. The ledger still needs a human "
                  "signature from a\nreviewer who did not draft the "
                  "restatement.")
    sys.exit(1 if rep.failed else 0)


if __name__ == "__main__":
    main()
