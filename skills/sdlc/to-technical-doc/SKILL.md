---
name: to-technical-doc
description: |
  Produces the shareable Technical Design document (+ DOCX) for a feature —
  the stakeholder-facing deliverable that gets attached to the PRD. Run
  explicitly after (or late in) tech-design. Use when asked for "the
  technical doc", "the DOCX", "the document for the PRD", or after a tech
  design is approved.
---

# To Technical Doc (stakeholder deliverable)

You produce `docs/features/<slug>/technical-doc.md` + `technical-doc.docx`
from `docs/templates/technical-doc.md`. This is a TRANSLATION of the
engineering tech design for PRD readers — not a second design. If you find
yourself making a design decision here, stop: it belongs in
`02-tech-design.md` first.

## Inputs (read all before writing)

- `02-tech-design.md` — the source of truth for the content.
- `01-gap-analysis.md` + manifest — feature context, decisions, and
  `open_questions`.
- Open team-handoffs for this feature: `docs/team-handoff/<slug>/` with
  `status: open`.
- The PRD (for tone and to avoid restating it).

## Writing rules (this is where it differs from the tech design)

- **No repo internals**: no file names, paths, module/class names, table or
  field lists. Describe the technical workflow, components and their
  responsibilities, architectural decisions, and state lifecycles at
  concept level — the sample structure in the template (summary → golden
  flow → architecture + invariants → states → failure behavior → decisions
  → sequence → open questions) is the contract.
- **Diagrams**: reuse/adapt the tech design's Mermaid sources
  (`diagrams/*.mmd`); add a golden-flow diagram and a state diagram if the
  tech design lacks them (a state diagram is expected whenever the central
  entity has a lifecycle). Every figure gets a numbered caption.
- **Don't restate the PRD** (it will sit next to this document) — one
  "Related requirement" pointer is enough.
- **§8 Open questions** (always last): merge the tech design's open
  questions and every open team-handoff. Each question is one short
  paragraph — context sentence, the question, what it affects — referencing
  team-handoff ids like `(team-handoff <slug>#003)`. Drop questions that
  have since been resolved; check the handoff docs' status first.
- Sensitive data appears only as the one-paragraph protection statement in
  §4, per the project's own compliance/data-handling rules — no real or
  synthetic examples in a document that leaves the building.

## Steps

1. Read the inputs; confirm the tech design is approved (or the user
   explicitly wants a draft from work-in-progress — mark **Status:
   Proposed** in that case).
2. Write `technical-doc.md` from the template. Render diagrams and build
   the DOCX: `tools/docx/build-docx.sh docs/features/<slug>/technical-doc.md`
   → verify `technical-doc.docx` exists.
3. Append a manifest handoff entry (stage: technical-doc helper —
   informational; this skill never touches stage/gate/slice state).
4. Show the user: where both files are, the design summary paragraph, and
   §8 so they can sanity-check the questions going to stakeholders.
   Suggest `/checkpoint` (the `.md` is committed; the `.docx` is gitignored
   and regenerable).

## Keeping it fresh

If the tech design changes after this document was produced (retro,
team-handoff resolutions), re-run this skill — it regenerates from the
current sources rather than patching the old output.
