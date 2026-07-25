---
name: feature-intake
description: |
  Stage 1 of the feature SDLC. Given a PRD and Figma design, scaffold the
  feature folder, build shared understanding, and produce a gap analysis
  (PRD vs design vs codebase). Use when starting a new feature, when asked to
  "analyze this PRD", "do intake", or "find gaps between the PRD and design".
---

# Feature Intake & Gap Analysis

You produce `docs/features/<slug>/01-gap-analysis.md`. Read
`_shared/handoff-format.md` and the project's `_shared/repo-map.md` first
(copy it from `_shared/repo-map.template.md` if it doesn't exist yet).

## Inputs (ask for whatever is missing)

- PRD: local file, pasted text, or Google Drive doc (Drive MCP tools available)
- Figma link(s): read designs through the **Figma desktop MCP server**
  (`use_figma` / `get_metadata` for structure, `get_screenshot` per screen,
  `get_design_context` for detailed specs of key frames). It resolves against
  the file open in the running Figma desktop app.
  **Link authority rule**: Figma links embedded in the PRD often point to the
  ORIGINAL file, while the user usually works from a LOCAL COPY. Before
  pulling any design context, ask the user which link/file is authoritative
  (default: the user's copy, typically the one open in Figma desktop).
  Record the authoritative link in the manifest `figma:` field and cite node
  IDs from it — the manifest link is what every later stage (tech-design,
  design-reviewer) uses, never the PRD's embedded links.
- Feature slug (kebab-case) — propose one from the title if not given

## Steps

1. **Scaffold**: create `docs/features/<slug>/` with `manifest.yaml` from
   `docs/templates/manifest.yaml` (fill feature/title/prd/figma). Copy the PRD
   into the folder (as `prd.md`/`prd.pdf`) if it's not already link-stable.
2. **Read the PRD fully.** Extract: user problem, in-scope behaviors,
   acceptance criteria, roles/permissions, non-functional requirements.
3. **Read the design.** For every screen: states covered (default, loading,
   empty, error, permission-denied), fields shown, interactions. Note Figma
   node IDs for later reference.
4. **Read the code.** Identify affected repos/modules (use repo-map; dispatch
   one Explore subagent per candidate repo for anything non-obvious, using the
   subagent contract in handoff-format.md §2). Find: existing patterns to
   reuse, code that conflicts with the PRD/design assumptions.
5. **Cross-examine** the three sources pairwise and record every gap in the
   template's gap table: PRD↔Figma mismatches, PRD ambiguities, design states
   missing, design↔code conflicts, PRD↔code conflicts.
6. **Data handling scan**: anything the feature will store, log, display,
   export or send to a third party gets checked against the data handling
   rules in `_shared/repo-map.md` and the repo-map's sensitive-data-exposure
   notes, and flagged now so the tech design has to address it. "No sensitive
   data" is a valid finding — record it explicitly rather than omitting the
   section.
7. **Write** `01-gap-analysis.md` from `docs/templates/gap-analysis.md`.
8. **Handoff**: append the handoff entry to `manifest.yaml`
   (stage: intake, next: tech-design), then run
   `tools/sdlc validate <slug>` and `tools/sdlc gate <slug> awaiting-approval`.

## Feedback point (STOP here)

Present in chat: the shared-understanding paragraph, the gap table summary,
and the open questions. The user resolves questions (with PM/design) and,
when satisfied, approves: `tools/sdlc approve <slug>`.
Do not proceed to design in the same invocation.
