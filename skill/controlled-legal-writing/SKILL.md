---
name: controlled-legal-writing
description: Draft, restate, and verify legal text under MLP-1 Controlled Legal Writing (CLW), a controlled language for court rules, statutes, regulations, and contracts. Use whenever the task involves summarizing a statute, rule, or regulation into plain language, drafting court rule or contract language, producing public-facing explanations of legal procedure, or checking whether a summary faithfully matches its source. Use it even when the user only says "summarize this rule", "explain this statute in plain English", "rewrite this clause more clearly", or "what does this regulation require" without naming CLW.
---

# Controlled Legal Writing

CLW is a controlled language for legal text. It has two jobs: writing operative text that has legal effect, and restating authoritative text that someone else wrote.

Controlled languages for technical documentation assume the writer may swap any word for a simpler one. That assumption fails in law. A legal term of art is not a hard word chosen over an easy one. It is a name for a rule, and replacing it deletes the rule. Where the writer is restating a statute rather than authoring one, the measure is not whether the text reads well. It is whether it says the same thing.

## The five refusals

These override fluency, brevity, and helpfulness. A restatement that is clear, short, and readable but breaks any of them has failed completely.

**1. Never paraphrase a legal standard, test, or threshold.**
*Good cause*, *abuse of discretion*, *clearly erroneous*, *material*, *willful*, *arbitrary and capricious*, *preponderance of the evidence*, *irreparable harm* — each names a body of case law. An ordinary-language substitute changes the governing law and hides the change.

> Source: "The court may suspend the rule for good cause."
> Wrong: The court may suspend the rule if it has a good reason.
> Right: The court may suspend the rule for good cause.

**2. Never resolve ambiguity that exists in the source.**
This one runs against your strongest habit. When a statute is silent or unclear, completing it is not helpful — it substitutes your reading for the law. Mark the gap instead.

> Source: "The record must be transmitted within 30 days."
> Wrong: The clerk must transmit the record within 30 days.
> Right: The record must be transmitted within 30 days. The rule does not state who must transmit it.

Never paper over a gap with a hedge. *Generally*, *typically*, *usually*, and *in most cases* disguise an unstated ambiguity as a tendency.

**3. Never add content the source does not state.**
No duty, condition, actor, deadline, purpose, consequence, definition, or form requirement that is not in the source. Adding a purpose narrows a power. Adding *reasonable* imposes a standard the text does not.

**4. Never drop content the source does state.**
Conditions, exceptions, qualifiers, cross-references, and consequences all survive. *On motion and for good cause* has two conditions; dropping either changes the rule.

**5. Never advise, predict, or apply.**
Describe what the source says. Do not say what the reader should do, what a court is likely to do, or how the text applies to particular facts.

## Operators

Every operative sentence carries exactly one of these seven. No others.

| Operator | Effect |
|---|---|
| **must** | Imposes a duty. Not acting is a violation. |
| **must not** | Imposes a prohibition. Acting is a violation. |
| **may** | Confers discretion. Neither acting nor not acting is a violation. |
| **may not** | Withholds authority. The actor has no power to act. |
| **is entitled to** | Confers a right another party must satisfy. |
| **need not** | Negates a duty. The actor may act but is not required to. |
| **will** | States a consequence that follows automatically. |

Never write *shall* in text you draft. Never write *should* at all — not in operative text, and not in explanatory text at any register.

**The negatives are not interchangeable.** `must not` forbids. `need not` merely releases from a duty. Writing one for the other inverts the provision, and it is the most common fidelity failure. `may not` withholds power; it never means "might not."

When the source uses *shall*, see `references/operators.md` before mapping it.

## Registers

Pick one before writing and hold it throughout.

| | Reader | Terms of art | Sentence cap |
|---|---|---|---|
| **R1** | Courts, bound parties | Used plainly. The text is the law. | 30 words |
| **R2** | Lawyers, judges, clerks | Preserved, no gloss | 30 words |
| **R3** | Self-represented litigants, public | Preserved, glossed at first use | 25 words |
| **R4** | No legal background | Preserved, then described | 20 words |

R1–R3 must be semantically equivalent to the source. R4 cannot be, so R4 output must carry a notice saying it is not the law, is not equivalent, and where the real text is.

Citations, quoted passages, case names, court names, dates, defined terms, and parenthetical asides each count as one word.

## Which workflow

- **Restating an authoritative source** (statute, rule, regulation, order, contract) → read `references/restate.md`. This is the common case.
- **Drafting new operative text** → read `references/draft.md`.
- **Checking someone else's restatement** → read `references/verify.md`.

## Reference files

| File | Read it when |
|---|---|
| `references/restate.md` | Restating an authoritative source |
| `references/draft.md` | Writing new operative text |
| `references/verify.md` | Auditing a restatement against its source |
| `references/operators.md` | Mapping *shall*, or unsure which negative applies |
| `references/preserved-terms.md` | Unsure whether a term may be replaced |
| `references/prohibited.md` | Checking wording before returning output |
| `references/examples.md` | Want a worked pair for a specific failure mode |

## Before returning anything

Read `references/prohibited.md` and scan your own output against it. The list is short and the failures are mechanical: archaic pointing words, Latin abbreviations, `and/or`, semicolons, missing serial commas, phrasal verbs, and the machine-prose tics that make a restatement look edited by nobody.

Then confirm each of the five refusals held. If you cannot confirm one, say so in the output rather than returning silently.

---

*Derived from MLP-1, Controlled Legal Writing (Michigan Legal Publishing Ltd.), licensed CC BY-NC-SA 4.0. This skill is a summary for working use and is not the standard. Refer to MLP-1 for the authoritative rules.*
