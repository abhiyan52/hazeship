---
name: implement
description: "Implement a piece of work from a spec or set of tickets — test-first at the agreed seams, typechecked as you go, reviewed before it's called done. Use when a ticket or spec is ready to build, or when another skill needs one unit of work implemented."
---

Implement the work described by the user in the spec or tickets.

Use `/tdd` where possible, at pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Commit your work to the current branch with the `checkpoint` skill — the commit
format in `_shared/branch-commit-conventions.md` is required for every commit in
this workspace.

## Review, in this workspace

Once done, review with the workspace's **`review`** skill, not `/code-review`
(which is not installed here). `review` runs three lanes — correctness +
security, PHI/HIPAA, and design-vs-spec — and the PHI lane is not optional on
any diff that touches patient data.

Inside a feature slice, the caller (`implement-slice`) owns dispatching review
after the task's own review has passed. Do not dispatch it yourself when you
were dispatched as an implementer subagent: return your report and let the
controller review you. Reviewing your own work in the same context is how a
missed requirement gets confirmed twice.

## Seams and tests

The seams were agreed with the user at the dev-plan stage (`/to-spec`) and are
recorded in `03-dev-plan.md`'s per-slice test strategy. Test at those seams.
A behaviour you cannot reach from an agreed seam is a signal the slice is cut
wrong — say so rather than inventing a new seam or testing internals.

Compliance applies while coding, not after: `_shared/phi-hipaa-checklist.md`
§B–§E bind every diff. Synthetic patient data only, and no PHI in logs,
exception messages, URLs, or test fixtures.
