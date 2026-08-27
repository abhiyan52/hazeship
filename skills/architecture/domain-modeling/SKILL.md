---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when the user wants to pin down domain terminology or a ubiquitous language, record an architectural decision, or when another skill needs to maintain the domain model.
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline — challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely *reading* `CONTEXT.md` for vocabulary is not this skill — that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## File structure

This workspace is **single-context**, as recorded in `docs/agents/domain.md` —
that file is the authority on layout; read it before writing either artifact.

- `CONTEXT.md` at the workspace root — one glossary covering all five
  sub-repos, since they share one domain language. Create it lazily, when the
  first term is resolved. Format: [`CONTEXT-FORMAT.md`](./CONTEXT-FORMAT.md).
- `docs/adr/` at the workspace root — already populated; scan it for the
  highest number and increment. Format: **`docs/templates/adr.md`**, the
  workspace template, which every ADR here uses.

`CONTEXT.md` and ADRs are committed to the meta-repo and carry **no PHI** — a
glossary defines concepts (progress note, cap window), never patient
instances. Use synthetic examples if an example is needed at all.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account' — do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

Which code to check is in `_shared/repo-map.md` — the five sub-repos are
independent repositories, so the same concept may be named differently on each
side of an API boundary. That divergence is itself a finding worth a glossary
entry with the losing names under `_Avoid_`.

### Update CONTEXT.md inline

When a term is resolved, update `CONTEXT.md` right there. Don't batch these up — capture them as they happen. Use the format in [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

`CONTEXT.md` should be totally devoid of implementation details. Do not treat `CONTEXT.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. [`ADR-WHEN.md`](./ADR-WHEN.md)
lists what qualifies — architectural shape, cross-context integration
patterns, lock-in technology choices, boundary decisions, deliberate deviations,
constraints invisible in the code — when a decision sits near the line.

Write it from
`docs/templates/adr.md` — the workspace template, with its Context / Decision /
Consequences sections and `Feature:` field — numbered one above the highest in
`docs/adr/`.

When a term or decision **contradicts an existing ADR**, surface the conflict
explicitly instead of silently overriding it, and put the resolution to the
user as its own question.
