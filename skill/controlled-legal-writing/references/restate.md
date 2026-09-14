# Restating an authoritative source

Use this when the source text already exists and you did not write it: a statute, court rule, regulation, ordinance, order, or contract.

The source is fixed. You cannot change what it requires. Your only job is to say the same thing in different words, at a stated register, and to mark honestly where the source does not answer a question.

Work the steps in order. Step 1 must be finished before you draft anything.

---

## Step 0 — Bind the version

Record before anything else:

- Full citation of the source.
- Effective date of the version you are restating.
- Register you are writing at (R1–R4).

A restatement without a version is unsafe, because rules amend and the summary silently goes stale. The Federal Rules take effect on December 1 in most years.

If the user has not said which version, ask, or state plainly which one you used.

---

## Step 1 — Decompose the source

**Do not draft yet. Do not think about phrasing.** Read only the source and break it into atomic propositions.

A proposition is atomic when removing any part of it loses a legal element. One duty, one permission, one condition, one consequence, one definition.

Build a ledger. One row per proposition:

| ID | Locus | Actor | Operator | Action | Conditions | Quantifiers | Connector | Consequence | Flags |
|---|---|---|---|---|---|---|---|---|---|
| P1 | 4(a)(1)(A) | party | must | file notice of appeal | — | — | — | none stated | |
| P2 | 4(a)(1)(A) | — | must | be filed within 30 days after entry of judgment | judgment entered | — | AND | none stated | |

Fill the columns exactly as the source has them:

- **Actor** — copy it, or write `NONE STATED`. Never infer one.
- **Operator** — the source's own word, verbatim. If the source says `shall`, write `shall`. Do not map it yet.
- **Conditions** — every one, listed separately. `On motion and for good cause` is two.
- **Quantifiers** — `each`, `any`, `all`, `only`, `at least`, `no more than`. These carry legal weight and are easy to lose.
- **Connector** — `AND` or `OR` between this proposition and its siblings. Whether a court must find all elements or any one of them is the whole content of a multi-part test.
- **Consequence** — what happens on non-compliance, or `NONE STATED`.

**Flags** — mark any of these:

| Flag | Means |
|---|---|
| `AMBIGUOUS` | A word or structure has more than one available reading |
| `AGENT UNSTATED` | The source does not say who acts |
| `OPERATOR CONTESTED` | Courts have divided on what the operator requires |
| `GAP` | The source simply does not address a question a reader will have |

Every flag becomes a sentence in the output. That is the point of flagging.

---

## Step 2 — Draft

Now write, at the declared register.

Order each provision: general rule, then exceptions, then consequences, then cross-references. Put conditions before their consequences. Split anything over the register's word cap.

Map each source operator to one of the seven, and record what you did:

| Source | Restatement |
|---|---|
| shall (mandatory) | must |
| shall not (prohibition) | must not |
| shall not (no authority) | may not |
| shall (future consequence) | will, or present tense |
| may | may |
| is not required to | need not |
| shall (construction contested) | **do not map** — state that the source says *shall* and cite both readings |

Never strengthen an operator. `may` does not become `will`. Never weaken one. `shall` in a mandatory clause does not become `may`.

Preserve the actor, or preserve its absence. If the source is agentless and no other provision supplies an actor, the restatement is agentless too, plus a sentence saying so.

---

## Step 3 — Map forward

For each row in the ledger, find the sentence in your draft that carries it.

- No sentence carries it → **dropped content**. Fix.
- The sentence changed the operator, actor, quantifier, or a condition → **altered content**. Fix.
- The row is flagged and no sentence marks the flag → **unmarked ambiguity**. Fix.

---

## Step 4 — Map backward

For each sentence in your draft, find the ledger row it came from.

- No row → **added content**. Cut it.
- Part row, part inference → **added content**. Cut the inference.

This direction catches what the forward pass misses. Do it as a separate reading. Read the draft as if someone else wrote it and you are hunting for claims the source never made.

The additions that recur most:

| Added | Looks like |
|---|---|
| An actor | "The clerk must…" where the source said only "must be…" |
| A purpose | "…to protect the parties' privacy" |
| A limit | "a reasonable extension" where the source set none |
| A form | "written notice" where the source said "notice" |
| A consequence | "the filing will be rejected" where the source is silent |
| A characterization | "this rule gives the court broad discretion" |

---

## Step 5 — Mark what the source does not answer

Every flag from Step 1 needs a sentence. Use a consistent form:

- "The rule does not state who must file the notice."
- "The rule requires notice. It does not state whether notice must be written."
- "The rule sets a 21-day period. It does not state what happens if a party files late."
- "The statute uses *shall*. Courts have divided on whether this imposes a duty or states a preference."

Do not soften these into hedges. "Notice generally must be in writing" is a fidelity failure, not a summary.

---

## Step 6 — Scan the wording

Read `references/prohibited.md` and check your draft against it. Then confirm:

- Every sentence within the register's word cap, counting citations and quotations as one word each
- Every list of three or more carries a serial comma
- No `and/or`, no semicolons outside quoted text, no Latin abbreviations
- No archaic pointing words: *herein*, *thereof*, *said*, *aforesaid*, *such* as a demonstrative
- Numbers as numerals once — `14 days`, never `fourteen (14) days`
- Every period states its length, its trigger, and its direction — `within 21 days after service`
- Terms of art carry their exact source form, and defined terms their exact capitalization

---

## Step 7 — Return

Return three things together:

1. **The restatement**, at the declared register.
2. **The ledger**, including every flag.
3. **The version binding** from Step 0.

Then state the conformance level honestly:

- **Level 1** — written under the style rules only.
- **Level 2** — Level 1 plus controlled vocabulary.
- **Level 3** — Level 2 plus a verified, human-signed ledger.

**You cannot certify Level 3.** A model that drafted a sentence will find that sentence faithful; your agreement is not verification. Say the ledger is complete and awaiting review. Level 3 requires a person who did not draft the text to sign it.

If a published restatement is going out alongside the source, say plainly that it has not reached Level 3 yet.

---

## Quick reference — the failures that matter most

| Failure | Why it happens |
|---|---|
| Supplying an actor for an agentless passive | Active voice feels better written |
| Resolving an ambiguity | Completeness feels more helpful |
| Paraphrasing a legal standard | It reads like jargon worth simplifying |
| Writing `must not` for `need not` | Both look like negation |
| Converting prose to a bulleted list | Lists imply a discreteness the source may not have |
| Adding a closing summary sentence | It characterizes, and characterization is construction |
