---
name: implement-slice
description: |
  Stage 4 of the feature SDLC. Implements ONE vertical slice from the dev
  plan, keeps the slice log, and stops for user testing when the slice is
  demoable. Use when asked to "implement slice N", "start the next slice", or
  "continue implementation".
---

# Implement a Vertical Slice

Read `_shared/handoff-format.md`, `_shared/branch-commit-conventions.md`,
and the project's `_shared/repo-map.md` first.

## Preconditions

- If stage is `dev-plan` with gate `approved`, first step is
  `tools/sdlc transition <slug> implement`. Otherwise `tools/sdlc show <slug>`
  must report stage `implement`.
- Determine which slice is next from `tools/sdlc show` (slice states).
  Confirm the slice number with the user if ambiguous.

## Hard dependency & blocker gate (STOP if any check fails)

Run ALL of these before touching code. Each is a hard stop — if one fails,
report exactly what is unresolved and do not proceed. The user may override
in writing per item (recorded in the slice log), but you never self-clear.

1. **Manifest not blocked**: `tools/sdlc show <slug>` gate must not be
   `blocked`. If blocked, surface the reason and stop.
2. **Previous slice resolved**: the prior slice is `merged` (or
   `user-approved` with a waived PR, merge pending). `tools/sdlc slice`
   also enforces this — never stack untested slices.
3. **Upstream slice dependencies merged**: read this slice's "depends on"
   entry in `03-dev-plan.md` (slice table + "Cross-slice risks & sequencing
   notes"). Every slice this one depends on must be in state `merged`
   (`tools/sdlc show`). List any that aren't and stop.
4. **No open blocking team-handoff**: check `docs/team-handoff/<slug>/` for
   any doc with `status: open` whose `blocks:` names this slice or the
   implement stage. If one exists, surface its id + question and stop —
   building on an unanswered blocker is how rework happens.
5. **In-slice task blockers**: confirm the slice's own task dependency
   column has no task marked blocked by unfinished external work. Blocking
   task chains are sequenced during implementation (Step 4 below).

## Steps

1. **Setup**: run `tools/sdlc slice <slug> <NN> in-progress` and create
   `docs/features/<slug>/slices/slice-<NN>.md` from
   `docs/templates/slice-log.md`.
   - **Branches**: if this is the first slice, create and push the empty
     feature branch `feat/<slug>` from each affected repo's staging branch
     (the dev plan's branch table — plan approval covered this; record in
     manifest `branches:`).
   - **Always work in a dedicated worktree — never the main checkout.** For
     each affected repo, create an isolated git worktree on a fresh slice
     branch off `feat/<slug>`:
     ```
     git -C <repo> worktree add -b feat/<slug>-slice-<NN> \
       <workspace-root>/.worktrees/<repo>/<slug>-slice-<NN> feat/<slug>
     ```
     `.worktrees/` is gitignored in the meta repo. This keeps the user's
     main checkout of each repo clean and untouched while the slice is in
     flight, and lets parallel `repo-implementer` agents work without
     colliding on a shared working tree. Record each worktree path in the
     slice log. ALL implementation, tests, lint, and checkpoints for this
     slice run inside these worktree paths — pass the worktree path (not the
     repo root) to any subagent you dispatch.
2. **Re-read the slice spec** in the dev plan AND the previous slice's
   "handoff notes for next slice". Where reality has diverged from the plan,
   note the deviation in the slice log before coding.
3. **Implement task by task**, respecting the dependency column:
   - Blocking chains run sequentially; non-blocking tasks in different repos
     may be delegated to parallel `repo-implementer` subagents (contract in
     handoff-format.md §2) — one repo per agent, never two agents in one repo.
   - Write tests alongside code per the slice's test strategy (test-first
     where the behavior is precisely specified).
   - Match each repo's existing conventions (see repo-map: lint/typecheck
     commands) and run them before considering a task done.
   - Compliance is in scope while coding: follow the project's own
     compliance/data-handling checklist for every diff.
4. **Checkpoint**: after each completed task (or coherent group), invoke the
   `checkpoint` skill to commit in the required format. Keep the work log
   table in the slice log current.
5. **Slice-complete gate**: all tasks done, unit/integration tests green,
   demo script from the dev plan walked through once by you (or via
   `qa-playwright` if scenarios are automatable). Record evidence in the
   slice log, then `tools/sdlc slice <slug> <NN> awaiting-user-test`.

## Feedback point (STOP here)

Give the user: the demo script steps, what to look at, known rough edges.
Options you offer next: run `qa-playwright` for the automated scenarios,
and/or user tests manually. Record their verdict:
- Issues found → `tools/sdlc slice <slug> <NN> changes-requested`, log the
  feedback in the slice log, fix in this slice (back to `in-progress`), and
  return to the gate above.
- Satisfied → `tools/sdlc slice <slug> <NN> user-approved`, then hand off to
  `raise-pr` (or, if the dev plan waived this slice's PR, merge the slice
  branch into `feat/<slug>` and let raise-pr record `merged`).

## Worktree cleanup

Once the slice is `merged` (raise-pr records it), remove the worktrees so
they don't accumulate:
```
git -C <repo> worktree remove <workspace-root>/.worktrees/<repo>/<slug>-slice-<NN>
```
Do NOT remove a worktree with uncommitted changes — commit or checkpoint
first. Leave worktrees in place while the slice is `changes-requested` (you
return to them to fix). `git -C <repo> worktree prune` clears stale entries.
