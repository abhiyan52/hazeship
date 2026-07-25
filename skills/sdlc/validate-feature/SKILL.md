---
name: validate-feature
description: |
  End-of-feature validation before the final PR to staging. Walks every PRD
  acceptance criterion and gap-analysis resolution against what was actually
  built, with code references and Playwright evidence. Use when asked to
  "validate the feature", "run final validation", or after the last slice
  merges into the feature branch.
---

# Validate Feature

You produce `docs/features/<slug>/04-validation.md` from
`docs/templates/validation.md` (if the project has no `docs/templates/` or
`tools/sdlc` yet, bootstrap them first per `_shared/workspace-setup.md`).
Read the manifest, PRD, gap analysis, tech design, dev plan, and ALL slice
logs first — validation is judged against the requirements, not against what
the slices happened to build.

## Preconditions

First step is `tools/sdlc transition <slug> validate` — the tool refuses
unless every slice is in state `merged`, so unmerged work cannot be
validated. If the transition fails, report the unmerged slices and stop.

## Steps

1. Build the requirement inventory: every PRD acceptance criterion, every
   gap-analysis item marked for resolution, every "Definition of done" item
   from the dev plan. Each gets a row — none skipped, none added silently.
2. Verify each row by the strongest available method, in order of preference:
   - Playwright scenario (invoke `qa-playwright` for the feature-level run)
   - Executed unit/integration test
   - Direct code inspection with file:line citation
   Mark method + evidence per row. "The slice log says it works" is not
   evidence.
3. Verify the data handling rules in `_shared/repo-map.md` over the full
   feature diff (`git diff <staging>...feat/<slug>`), one row per rule.
4. Record accepted deviations (things built differently than the PRD/design
   said, with who approved) and residual risks.
5. Verdict: PASS only if every requirement row passes and no unaccepted
   data-handling failures exist. Otherwise FAIL with the exact failing rows —
   these go back to implement-slice as fix work.
6. Manifest handoff (stage: validate, next: final-pr or slice fixes), then
   `tools/sdlc validate <slug>` and — only on a PASS verdict —
   `tools/sdlc gate <slug> awaiting-approval`. On FAIL, set
   `tools/sdlc gate <slug> blocked` and route the failing rows back to
   implement-slice.

## Feedback point (STOP here)

Present the verdict, the requirement table summary, and deviations. On PASS
the user approves with `tools/sdlc approve <slug>`;
then `raise-pr` (final PR) and `review` follow.
