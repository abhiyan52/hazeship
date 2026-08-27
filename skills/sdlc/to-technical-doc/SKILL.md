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
from `docs/templates/technical-doc.md` (if the project has no
`docs/templates/` or `tools/docx/build-docx.sh` yet, bootstrap them first per
`_shared/workspace-setup.md`). This is a TRANSLATION of the engineering tech
design for PRD readers — not a second design. If you find yourself making a
design decision here, stop: it belongs in `02-tech-design.md` first.

## Communication format: ASD-STE100 Simplified Technical English

Every sentence you write in `technical-doc.md`, and every question or
explanation you give the user about it in chat, uses ASD-STE100 Simplified
Technical English:

- One instruction or fact per sentence. Keep sentences under ~20 words.
- Active voice, simple present ("The gateway checks the token"), not
  passive ("The token is checked by the gateway").
- One word per meaning — pick a simple word and reuse it, never a synonym
  swapped in for variety.
- Define any jargon or domain term the first time you use it; a PRD reader
  does not know your internal vocabulary.
- No noun strings longer than three words; split any sentence joined by
  "and"/"which"/"but" into separate sentences.

## Short and sweet: a hard length ceiling

This document is stakeholder-facing, not a second tech design — length is a
defect, not thoroughness. Enforce these caps; a draft that breaks one is not
done:

- Each numbered section (§1–§7; §8 follows its own per-question rule below)
  is **one short paragraph** (3–6 sentences) plus its table/diagram — no
  sub-narratives, no walkthroughs of what the diagram already shows.
- The whole document's prose (every section combined, tables and captions
  excluded) stays **under ~900 words**. Count it before calling the draft
  done; over budget means cut restated tech-design content, not shrink font.
- If a sentence's information already lives in a table, diagram, or another
  section, delete the sentence — do not say the same fact twice in two
  forms.

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
  concept level — the section structure in the template (§1 summary → §2
  golden flow, with the sequence diagram → §3 architecture + invariants →
  §4 data handling → §5 states → §6 failure behaviour → §7 decisions → §8
  open questions) is the contract. Keep the numbering: §4 and §8 are
  referenced by name below.
- **Diagrams**: every figure is generated with the `archify` skill, never
  Mermaid — read the tech design's diagrams for topology and meaning, then
  author a fresh Archify JSON spec; do not mechanically port Mermaid
  styling. Pick the type from archify's router (golden flow → `workflow` or
  `sequence`; architecture → `architecture`; state diagram → `lifecycle`).
  Add a golden-flow diagram and a lifecycle diagram if the tech design lacks
  them (a lifecycle diagram is expected whenever the central entity has
  states). Every figure gets a numbered caption. Per-diagram steps, each
  ending on a checkable result:
  1. Author `diagrams/<name>.json` (fresh spec — see archify's fast
     authoring path). Omit `meta.visual_preset` and `meta.animation`; this
     document only ever ships the static default.
  2. Locate the installed `archify` skill directory (its `bin/archify.mjs`);
     `node bin/archify.mjs` below is run from inside it, with absolute paths
     for `diagrams/<name>.json`/`.html` since the feature folder is
     elsewhere:
     `node bin/archify.mjs deliver <type> <abs-path-to>/diagrams/<name>.json <abs-path-to>/diagrams/<name>.html --quality showcase --json`
     — must exit 0 with 0 composition errors before you move on.
  3. **Light mode, PNG only**: open `diagrams/<name>.html?theme=light` (the
     `theme=light` query param forces the light palette regardless of system
     preference), click the export toolbar button (`#btn-export`) then the
     PNG item (`button[data-format="png"]`), and save the download as
     `diagrams/<name>.png`. Confirm the saved image is light-background
     before moving on — a dark capture is a failed step, not a style choice.
  4. Embed `diagrams/<name>.png` in `technical-doc.md` with a real image
     reference — never a Mermaid fence, never the `.html`. The delivered
     `.html` and the authoring `.json` are build artifacts, gitignored like
     `technical-doc.docx`, kept only for regeneration.
- **Don't restate the PRD** (it will sit next to this document) — one
  "Related requirement" pointer is enough.
- **§8 Open questions** (always last): merge the tech design's open
  questions and every open team-handoff. Each question is one short
  paragraph — context sentence, the question, what it affects — referencing
  team-handoff ids like `(team-handoff <slug>#003)`. Drop questions that
  have since been resolved; check the handoff docs' status first.
- Sensitive data appears only as the one-paragraph protection statement in
  §4, per the data handling rules in `_shared/repo-map.md` — no real or
  synthetic examples in a document that leaves the building.

## Steps

1. Read the inputs; confirm the tech design is approved (or the user
   explicitly wants a draft from work-in-progress — mark **Status:
   Proposed** in that case).
2. Generate every figure's `diagrams/<name>.png` per the Diagrams rule above,
   done before you write a word of prose — you reference each PNG by name as
   you write.
3. Write `technical-doc.md` from the template, under the length ceiling
   above. Build the DOCX:
   `tools/docx/build-docx.sh docs/features/<slug>/technical-doc.md` → verify
   `technical-doc.docx` exists. (The script's own Mermaid step is a no-op
   here — there are no `.mmd` files to find.)
4. Append a manifest handoff entry (stage: technical-doc helper —
   informational; this skill never touches stage/gate/slice state).
5. Show the user: where both files are, the design summary paragraph, and
   §8 so they can sanity-check the questions going to stakeholders.
   Suggest `/checkpoint` (`.md` and `diagrams/*.png` are committed; `.docx`,
   `diagrams/*.html`, and `diagrams/*.json` are gitignored and regenerable).

## Keeping it fresh

If the tech design changes after this document was produced (retro,
team-handoff resolutions), re-run this skill — it regenerates from the
current sources rather than patching the old output.
