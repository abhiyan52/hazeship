# Slice <NN> — <name>

- **Feature**: `<slug>`
- **Spec**: `03-dev-plan.md` → Slice <NN>
- **State**: see `tools/sdlc show <slug>`
- **Started**: <YYYY-MM-DD>

## Worktrees

All implementation, tests, lint and checkpoints for this slice run inside
these paths — never the user's main checkout.

| Repo | Branch | Worktree path |
|---|---|---|
| <repo> | `feat/<slug>-slice-<NN>` | `<workspace-root>/.worktrees/<repo>/<slug>-slice-<NN>` |

## Deviations from the plan

Recorded **before** coding, whenever reality diverges from the dev plan.

| Planned | Actual | Why | Approved by |
|---|---|---|---|
| <what the plan said> | <what we did> | <reason> | <user, if it needed approval> |

## Work log

| # | Task | Status | Notes |
|---|---|---|---|
| 1 | <task from the dev plan> | done / in-progress / blocked | <notes> |

## Commits

| Commit | Repo | Subject |
|---|---|---|
| `<sha>` | <repo> | `<type>: <subject>` |

## Test evidence

| Check | Command | Result |
|---|---|---|
| Unit | `<command>` | <pass/fail + counts> |
| Integration | `<command>` | <pass/fail + counts> |
| Lint / typecheck | `<command>` | <pass/fail> |

### Playwright scenarios

| # | Scenario | Result | Evidence |
|---|---|---|---|
| S<NN> P1 | <name> | pass / fail | `evidence/<file>.png` |

<Paste failures verbatim from the reporter — assertion diff and any console
errors the test surfaced. A summarised failure is a lost failure.>

## Demo

<The steps you walked, and what the user saw. Note known rough edges you
told them about.>

## User feedback

| Date | Feedback | Disposition |
|---|---|---|
| <date> | <what they said> | fixed in this slice / new slice / accepted as-is |

## Handoff notes for the next slice

Read by `implement-slice` at the start of the next slice — the most useful
section in this file.

- <what's now in place that the next slice builds on>
- <anything left deliberately unfinished, and where it's tracked>
- <traps: a convention you had to follow, a test that's slow, a flaky path>
