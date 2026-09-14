# Verifying a restatement

Use this when a restatement already exists and you are checking it against its source — someone else's work, or your own from an earlier session.

Verification is not rereading. **A reader who has just written a restatement reads the source through it.** That is the whole problem this procedure exists to solve.

---

## Before you start: the anchoring constraint

Where a language model assists with any step:

- The model **must not see the restatement while decomposing the source.**
- The model **must not see the ledger while drafting.**
- Forward mapping and backward mapping are **separate calls with no shared context.**
- **A model's agreement is not verification.** A model that drafted a sentence will find that sentence faithful.
- **A human reviewer signs the ledger.**

The reason is anchoring. A checker that has seen the draft will read the source to confirm the draft.

**Practical consequence for you:** if you drafted the restatement in this conversation, you cannot verify it here. Say so. Offer the mechanical checks, which are anchoring-resistant, and state that the fidelity check needs a fresh context or another reviewer.

---

## Step 1 — Check the version binding first

Before reading a word of substance:

- Does the restatement name the source's full citation?
- Does it name the effective date of the version restated?
- Does it name the register?

A restatement without a version binding cannot be verified at all, because you cannot tell which text it was supposed to match. Stop and report that.

---

## Step 2 — Decompose the source, without reading the restatement

Read **only the source**. Build the ledger from scratch. One row per atomic proposition:

| ID | Locus | Actor | Operator | Action | Conditions | Quantifiers | Connector | Consequence | Flags |
|---|---|---|---|---|---|---|---|---|---|

Fill it exactly as the source has it. Copy the actor or write `NONE STATED`. Copy the operator verbatim — if the source says *shall*, write *shall*. List every condition separately.

Flags: `AMBIGUOUS`, `AGENT UNSTATED`, `OPERATOR CONTESTED`, `GAP`.

**If a ledger came with the restatement, do not read it yet.** Build your own, then compare. A supplied ledger that you read first anchors you to the drafter's decomposition, and a missed proposition stays missed.

---

## Step 3 — Run the mechanical checks

Cheap, and they catch a substantial share of failures. These need no ledger.

**Style (Level 1):**

1. No sentence over the register's word cap, counting each citation, quotation, case name, date, defined term, and parenthetical as one word.
2. No prohibited word outside a quotation. See `prohibited.md`.
3. No word outside the seven operators used as a normative operator.
4. No semicolon outside a quotation or a reproduced series.
5. No `and/or` outside a quotation.
6. No contraction.
7. Serial comma in every list of three or more, outside quotations.
8. No Latin abbreviation.
9. No sentence-initial connective in R1 text.

**Fidelity (Level 3) — these run against the ledger:**

10. Every citation in the source appears in the restatement, in the same form.
11. Every numeral in the source appears, or its absence is explained.
12. Every defined term appears in its exact form, and no near-synonym for a defined term appears.
13. Every quantifier appears — *each, any, all, only, at least, no more than*.
14. The count of `AND` and `OR` connectors between propositions matches.
15. Every subsection designation appears, in the source's order.
16. Every proposition flagged `AMBIGUOUS`, `AGENT UNSTATED`, or `GAP` maps to a marking sentence.
17. No sentence carries an operator stronger than the source's.

Checks 10 through 17 can be automated against the ledger.

---

## Step 4 — Map forward

For each ledger row, find the sentence in the restatement that carries it.

| Finding | Name it |
|---|---|
| No sentence carries the proposition | **Dropped content** |
| The sentence changes the operator, actor, quantifier, or a condition | **Altered content** |
| The row is flagged and no sentence marks the flag | **Unmarked ambiguity** |

---

## Step 5 — Map backward

For each sentence in the restatement, find the ledger row it came from.

| Finding | Name it |
|---|---|
| No row | **Added content** |
| Part row, part inference | **Added content** — the inference half |

**This is the harder direction and it catches what the forward pass misses.** Do it as a separate reading, preferably on a different day. Read the restatement as if a stranger wrote it and you are hunting for claims the source never made.

The additions that recur most:

| Added | Looks like |
|---|---|
| An actor | "The clerk must…" where the source said only "must be…" |
| A purpose | "…to protect the parties' privacy" |
| A limit | "a reasonable extension" where the source set none |
| A form | "written notice" where the source said "notice" |
| A consequence | "the filing will be rejected" where the source is silent |
| A characterization | "this rule gives the court broad discretion" |
| A hedge | "notice generally must be in writing" |

---

## Step 6 — Reconstruct blind

The maps in Steps 4 and 5 are done holding the source, which is their weakness:
a checker who has read the source supplies missing propositions from memory
without noticing.

1. Give a reader the restatement, and nothing else.
2. Ask them to write what the source must have said — every duty, condition,
   actor, period, and consequence.
3. Compare that reconstruction against the real source.

A divergence in either direction is a defect in the restatement, not in the
reconstruction. A reconstruction divergence blocks publication.

**If you drafted the restatement, you cannot do this step either**, and neither
can a model that has seen the source in this conversation. It has to be a
separate call that never received it. Say so rather than performing a
reconstruction you are not blind for.

A clean reconstruction proves the restatement carries enough to rebuild the
source. It does not prove the restatement says only what the source says —
Step 5 does that.

---

## Step 7 — Report

Report findings as defects against the source, not as suggestions. For each:

- **Locus** in the source.
- **Class**: dropped, altered, added, unmarked ambiguity, or style.
- **The source text** and **the restatement text**, quoted.
- **What changed**, in one sentence.

Do not rewrite the restatement as part of a verification report unless asked. Verification and drafting are separate jobs, and a verifier who rewrites has become a drafter and lost independence.

---

## Step 8 — State the level reached, honestly

| Level | Requires |
|---|---|
| **Level 1 — Style** | Sections 1 through 9 and 11 |
| **Level 2 — Controlled** | Level 1, plus the dictionary |
| **Level 3 — Verified** | Level 2, plus Section 10 and a completed, human-signed ledger |

A published restatement must be Level 3. Nothing below Level 3 may be labeled a restatement or published alongside a source text.

**You cannot certify Level 3.** Report that the ledger is complete and awaiting review. Level 3 requires a person who did not draft the text to sign it.

---

## What a clean verification looks like

Not "the restatement is accurate." That is an assertion, and Rule 10.1 says equivalence is verified rather than asserted.

A clean result says: the ledger has *n* propositions; every one maps forward to a sentence; every sentence maps backward to a proposition; every flag has a marking sentence; the mechanical checks pass; and the ledger awaits a human signature.

If you cannot say all of that, say which part fails.
