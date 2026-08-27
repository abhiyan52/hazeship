---
name: grill-with-docs
description: A relentless interview that sharpens a plan or design and captures the domain language and decisions as it goes. Use when the user wants to stress-test thinking and keep the glossary and ADRs current, or when another skill needs a grounded interview before it writes its artifact.
---

Run a `/grilling` session, using the `/domain-modeling` skill.

The two halves are load-bearing together: `grilling` drives the questions one at
a time and refuses to act before shared understanding is reached, while
`domain-modeling` captures each resolved term into `CONTEXT.md` and each
qualifying decision into an ADR **the moment it crystallises** — not batched at
the end, where the reasoning has already faded.

Done when every question raised has an answer the user confirmed, and every term
sharpened or decision taken during the interview is written down.
