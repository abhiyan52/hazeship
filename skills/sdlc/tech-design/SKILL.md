---
name: tech-design
description: |
  Stage 2 of the feature SDLC. Turns a resolved gap analysis into a Tech
  Design Document (markdown + Mermaid diagrams). Use when asked to "write
  the tech design", "create the TDD/design doc", or after feature-intake's
  open questions are resolved. The shareable DOCX deliverable is NOT this
  skill's job — that's /to-technical-doc, run afterwards.
---

# Tech Design Document

You produce `docs/features/<slug>/02-tech-design.md` (working engineering
document — the input to dev-plan, review, and /to-technical-doc).
Read `_shared/handoff-format.md` and the project's `_shared/repo-map.md`
first.

## Preconditions

- `tools/sdlc show <slug>` reports stage `intake` with gate `approved`;
  first step is `tools/sdlc transition <slug> tech-design` (the tool refuses
  if the gap analysis wasn't approved). Open questions from the gap analysis
  must be resolved (answers recorded in the gap doc or manifest); if
  unresolved blockers remain, list them and stop.
- Optional input: a reference document showing the expected structure/depth —
  follow its structure where it conflicts with the template.

## Steps

1. Read the gap analysis, PRD, and the affected code paths deeply enough to
   name concrete modules/files in the "Modules changed" table — no
   hand-waving. Reuse existing patterns; call out where you deliberately
   diverge from them.
2. Draft `02-tech-design.md` from `docs/templates/tech-design.md`. Rules:
   - Do NOT restate PRD content (it gets appended to the PRD later).
   - Every architecturally significant decision gets an entry in
     "Alternatives considered"; if it constrains future features, also record
     an ADR in `docs/adr/`.
   - The sensitive-data-flow table (§5) is mandatory — "no sensitive data"
     must be stated and justified explicitly, per the project's own
     compliance/data-handling rules.
3. **Diagrams**: write Mermaid sources in `docs/features/<slug>/diagrams/*.mmd`
   (at minimum an architecture flowchart; add a sequence diagram when the
   feature spans repos or async boundaries). Reference them in the doc as
   `![name](diagrams/name.png)`.
4. **Handoff**: append entry to manifest (stage: tech-design, decisions,
   open_questions, next: dev-plan), then `tools/sdlc validate <slug>` and
   `tools/sdlc gate <slug> awaiting-approval`.

## Feedback point (STOP here)

Summarize: the approach in 3 lines, decisions + rationale, anything you're
unsure about. The user reviews the markdown and approves with
`tools/sdlc approve <slug>` before `dev-plan` runs. Once approved (or while
finalizing), suggest `/to-technical-doc <slug>` to produce the shareable
stakeholder document + DOCX — that is deliberately a separate skill.
