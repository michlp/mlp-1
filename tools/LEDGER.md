# Proposition ledger — file format

The ledger is the artifact that makes equivalence checkable (Part 3). This file
defines a machine-readable form of it so that checks 10 through 17 can run
automatically, as the standard says they can.

The ledger is built **before** the restatement is drafted, and it is built from
the source alone.

## File

One JSON object. UTF-8. Conventionally `<name>.ledger.json`.

```json
{
  "register": "R2",
  "conformance_target": 3,
  "sources": [
    {
      "id": "S1",
      "citation": "Fed. R. App. P. 4(a)(1)(A)",
      "version": "Effective 2024-12-01",
      "text_file": "source/farp-4a1a.txt"
    }
  ],
  "restatement_file": "restatement/farp-4a1a.md",
  "propositions": [
    {
      "id": "P1",
      "source": "S1",
      "locus": "4(a)(1)(A)",
      "actor": "party",
      "source_operator": "shall",
      "construction": "mandatory",
      "authority": "Bowles v. Russell, 551 U.S. 205 (2007)",
      "operator": "must",
      "action": "file the notice of appeal",
      "conditions": ["judgment or order entered"],
      "quantifiers": [],
      "connector": null,
      "consequence": "NONE STATED",
      "citations": [],
      "numerals": ["30 days"],
      "defined_terms": [],
      "flags": [],
      "carried_by": ["R1"]
    }
  ]
}
```

## Fields

### Top level

| Field | Required | Meaning |
|---|---|---|
| `register` | yes | `R1`–`R4`. Sets the sentence cap. |
| `conformance_target` | yes | 1, 2, or 3. Level 3 runs every check. |
| `sources` | yes | One or more source instruments. |
| `restatement_file` | yes | The restatement being checked. |
| `front_matter` | no | Sentences that are apparatus, not propositions: the register line, the version binding. Exempt from check 18. |
| `glosses` | no | Sentences that gloss a term of art. R3 and R4 require these and the source does not contain them, so they are exempt from check 18. |
| `propositions` | yes | One entry per atomic proposition. |

### Source

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Short handle (`S1`), referenced by each proposition. |
| `citation` | yes | Full citation. |
| `version` | yes | Effective date or amendment identifier. Rule 10.9. |
| `text_file` | yes | Plain-text file holding the source text. |
| `source_sha256` | yes | SHA-256 of that file, line endings normalized. Rule 10.9 and Part 3's version binding. |

**Multi-source restatements.** List each instrument separately. A restatement
that synthesizes a rule, a local rule, and a standing order carries three
entries, and every proposition names the one it came from. This is what makes
provenance checkable: a proposition whose `source` is the standing order can be
told apart from one that came from the rule, and an amendment to any one source
identifies exactly the propositions and sentences it touches.

Where two sources state the same proposition, record it once per source and
give each its own `id`. Do not merge them — the merge is a construction, and if
the sources later diverge the ledger has to say which one moved.

Where sources **conflict**, record both and flag `CONFLICT`. Resolving a
conflict between instruments is construction, not restatement.

### Proposition

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | `P1`, `P2`, … Unique. |
| `source` | yes | A source `id`. |
| `locus` | yes | Subsection designation, as the source spells it. |
| `actor` | yes | The actor, verbatim, or `NONE STATED`. Never inferred. |
| `source_operator` | yes | The source's own word, verbatim. |
| `construction` | no | One of the values below. An unrecognised value fails check 17. |
| `authority` | no | What supports `construction`. Required when it is `mandatory` or `directory`. |
| `operator` | yes | The mapped CLW operator, or `null` where mapping is refused. |
| `action` | yes | The act, in the source's terms. |
| `conditions` | yes | Array. Each condition separately. `[]` if none. |
| `quantifiers` | yes | Array: `each`, `any`, `all`, `only`, `at least`, … |
| `connector` | yes | `AND`, `OR`, or `null`. |
| `consequence` | yes | The stated consequence, or `NONE STATED`. |
| `citations` | yes | Citations appearing in this proposition. |
| `numerals` | yes | Numerals appearing in this proposition. |
| `defined_terms` | yes | Terms the source defines, in the source's exact form. |
| `flags` | yes | Array. See below. |
| `carried_by` | yes | What carries this proposition: sentence ids, or snippets (preferred). |
| `series` | no | A declared list: `{connector, items, stem}`. Makes checks 7 and 14 decidable. |

### Constructions

| Value | Means |
|---|---|
| `mandatory` | The operator imposes a duty or a prohibition |
| `directory` | The operator states a preference; non-compliance does not void the act |
| `permissive` | The operator confers discretion, or exempts |
| `declaratory` | The sentence states an amount, a status, or what is treated as what. It maps to the simple present and carries no operator |
| `conditional` | The source word inverts a conditional clause and is not deontic at all: *Should the court desire* means *if* |
| `contested` | Courts have divided |
| `unverified` | The construction has not been checked against authority |

`declaratory`, `contested` and `unverified` all require `operator` to be
`null`. For the first the sentence is not deontic; for the other two the
mapping cannot be established, and Rule 10.7 forbids mapping on a construction
you cannot show.

`conditional` describes the source word, not the provision. The provision may
still carry an operator of its own — *Should the court desire to hear argument,
the court **may** pass an order* is conditional as to *should* and permissive
as to *may*.

### Flags

| Flag | Means |
|---|---|
| `AMBIGUOUS` | A word or structure has more than one available reading |
| `AGENT UNSTATED` | The source does not say who acts |
| `OPERATOR CONTESTED` | Courts have divided on what the operator requires |
| `GAP` | The source does not address a question a reader will have |
| `CONFLICT` | Two sources state inconsistent propositions |

Every flag must map to a sentence that marks it. That is check 16.

## The restatement file

Markdown or plain text. Sentences are numbered for mapping by an `{#R1}`
marker at the end of each sentence. Without markers the checker numbers them
positionally, `R1`, `R2`, … in order, treating each markdown list item as its
own sentence.

**Positional numbering shifts when the prose is edited.** Splitting one
over-length sentence renumbers everything after it, and every `carried_by`
below that point then points at the wrong sentence. On a restatement that is
still being drafted, use explicit `{#R1}` markers, or re-derive `carried_by`
after each edit.

## Operator strength

Check 17 forbids a restatement operator stronger than the source's. Strength is
ranked:

| Rank | Operators |
|---|---|
| 4 | must, must not |
| 3 | may not, is entitled to |
| 2 | will |
| 1 | may |
| 0 | need not |

A source word is ranked through its `construction`:

| Source word | Construction | Rank |
|---|---|---|
| shall, must | mandatory | 4 |
| shall | directory | 1 |
| shall not, must not | mandatory | 4 |
| may | permissive | 1 |
| should | — | 1 |
| is entitled to | — | 3 |
| is not required to, need not | — | 0 |

Where `construction` is `contested` or `unverified`, the checker does not rank
the source operator. It requires `operator` to be `null` instead, because
Rule 10.7 forbids mapping a construction you cannot establish.

## carried_by: prefer snippets

An entry is either a sentence id (`R7`) or a snippet of the sentence it points
at. **Prefer snippets.** Positional ids shift the moment any earlier sentence
is split, and every `carried_by` below the edit then points at the wrong text
without anything reporting it. A snippet survives renumbering; the checker
resolves it by search and reports it if it matches nothing, or more than one
sentence.

```json
"carried_by": ["the court must enter a judgment of acquittal",
               "The court must do so on the defendant"]
```

## Declared series

A series a regex cannot parse becomes checkable once the ledger declares it:

```json
"series": {
  "connector": "AND",
  "stem": "the court may do all of the following",
  "items": ["Reserve decision on the motion",
            "Proceed with the trial",
            "Submit the case to the jury",
            "Decide the motion"]
}
```

- **Check 7** requires the serial comma where three or more items run in to one
  sentence. A vertical list under Rule 4.4 has no run-in conjunction, so the
  check does not apply to it.
- **Check 14** requires the connector in the text carrying the series. Rule 4.4
  puts it in the introductory text as a phrase, so `all of the following`,
  `each of the following`, `any of the following` and `one or more of the
  following` all count, as do the bare words.

Declaring a series is optional. Undeclared lists are still reported as
candidates in the detail line, but they cannot fail the run.

## Check 18 — backward coverage

Part 3 Step 4 maps every restatement sentence back to a proposition. A sentence
no proposition claims is either added content or an unmapped proposition, and
both are defects.

This is the only mechanical check on the backward map, and the backward map is
where fidelity defects actually surface. Front matter and glosses are exempt,
and nothing else is.

## Blocking and advisory

Part 3 splits failures by what they cost. A failure blocks where it changes
what the text says or conceals that something is unsaid. Where the text still
says the same thing, it is recorded and queues editorial review.

| | Checks |
|---|---|
| **Blocking** | 3, 5, 7, 10–19 |
| **Advisory** | 1, 2, 4, 6, 8, 9 — length, wording, punctuation, register |

An advisory failure prints `REVIEW` and leaves the exit status at 0. A blocking
failure exits 1. A semicolon and a misstated deadline are not comparable harms,
and giving them the same veto rejects sound work over prose.

## Check 19 — version binding

`source_sha256` is compared against the file on every run. A mismatch means the
source moved under the ledger, and Rule 10.9 makes the document unverified
until it is re-verified rather than silently republished.

Compute it the way Part 3 specifies — over the source as retrieved, normalized
only for line endings:

```
python3 -c "import hashlib,sys;p=sys.argv[1];print(hashlib.sha256(open(p,'rb').read().replace(b'\r\n',b'\n')).hexdigest())" source/rule.txt
```

## Advisory checks

Checks 7 and 14 fail only on what the ledger declares. What they find in
undeclared prose is reported in the detail line as candidates, because a regex
cannot settle it: *the applicant, appellant, or counsel for the applicant or
appellant* carries its serial comma correctly and trips every pattern simple
enough to write, and two amounts in consecutive sentences are disjunctive by
structure with no *or* anywhere.

Read the candidates. They are not failures, and they are not noise either.

## What the checker does not do

It does not read the source for you. A ledger that omits a proposition is a
ledger the checker will call complete, because the checker has no independent
view of the source. **Decomposition is human work, and so is the signature.**

The checker catches mechanical divergence between a ledger, a source, and a
restatement. It does not verify that the ledger is faithful to the source.
