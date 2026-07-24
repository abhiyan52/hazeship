---
name: dev-plan
description: |
  Stage 3 of the feature SDLC. Turns the tech design into a phased development
  plan of vertical slices with dependencies and per-slice test strategies. Use
  when asked to "create the dev plan", "break this into slices/tasks", or
  after the tech design is approved.
---

# Development Plan (phases → vertical slices)

You produce `docs/features/<slug>/03-dev-plan.md`. Read
`_shared/handoff-format.md`, `_shared/branch-commit-conventions.md`, and the
project's `_shared/repo-map.md` (copy it from `_shared/repo-map.template.md`
if it doesn't exist yet) first.

## Preconditions

`tools/sdlc show <slug>` reports stage `tech-design` with gate `approved`;
first step is `tools/sdlc transition <slug> dev-plan` (the tool refuses if
the tech design wasn't approved).

## Core rules for slicing

- **Vertical, not horizontal**: a slice is "user can do X end-to-end (maybe
  behind a flag)", never "all the models" then "all the APIs" then "the UI".
  Each slice ends demoable and testable by the user.
- Prefer 2–5 slices; a slice should be roughly a day-or-less of agent work.
- Slice 1 is the walking skeleton: the thinnest end-to-end path through every
  layer the feature touches (including cross-repo contracts), so integration
  risk dies first.
- Mark task dependencies honestly: `blocking` (next task cannot start) vs
  `non-blocking` (parallelizable — these are candidates for parallel
  subagents in implement-slice).
- Migrations/contract changes that multiple slices need land in the earliest
  slice that needs them.

## Steps

1. Read tech design + gap analysis. List every concrete change from the
   "Modules changed" table and assign each to a slice.
2. Write `03-dev-plan.md` from `docs/templates/dev-plan.md`, including per
   slice: tasks with dependency column, test strategy (unit / integration /
   numbered Playwright scenarios with preconditions-steps-expected — these are
   executed verbatim by qa-playwright later), demo script, compliance notes,
   and a **PR policy** (slice PR required vs waived — see the risk rules in
   `_shared/branch-commit-conventions.md`; required is the default).
3. For any slice spanning repos, fill the **cross-repo compatibility matrix**
   in the template: merge order, deploy order, backward compatibility between
   producer/consumer versions, feature flag, and rollback path. Contract
   tests are required at every API/message boundary the slice crosses.
4. Fill the branch plan table (feature branch per affected repo, target
   staging branch from repo-map). Do NOT create or push any branches —
   branches are created by `implement-slice` after this plan is approved.
5. **Handoff**: manifest entry (stage: dev-plan, next: implement), then
   `tools/sdlc validate <slug>` and `tools/sdlc gate <slug> awaiting-approval`.

## Feedback point (STOP here)

Present the phase/slice table, PR policy per slice, and any compatibility
matrices. The user confirms slicing and sequencing with
`tools/sdlc approve <slug>` before any
implementation or branch creation happens.
