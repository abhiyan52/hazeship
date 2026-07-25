---
name: review
description: |
  Two-lane PR review: (1) correctness, security & code quality — bugs,
  injection/trust-boundary safety, efficiency, structural quality; (2)
  design & requirements conformance. Both lanes validate against the PRD
  and the technical docs from earlier stages. Use when asked to "review
  this PR", "review my diff", or before merging anything.
---

# PR Review

Reviews a PR (`gh pr diff`) or a local diff against a base branch. Applies to
slice PRs (→ feature branch) AND final PRs (→ staging) — the final PR review
re-runs every lane over the whole feature diff, not just the last slice.

## Order of operations: deterministic checks first

Before any model review, run the repo's own checks on the head branch
(lint, typecheck, tests — commands in `_shared/repo-map.md`) if CI hasn't
already. A failing deterministic check is reported first and blocks merge on
its own; model review supplements reproducible checks, never substitutes for
them.

## Setup

1. Identify repo, PR/diff, and base. Get the diff:
   `gh pr diff <n>` or `git diff <base>...HEAD`. Record the exact head commit
   SHA reviewed — it goes in the handoff entry so findings actioned in a later
   session can be re-checked against drift (a finding may already be fixed at
   HEAD by the time someone acts on it).
2. Load the intent sources if this is feature work: `docs/features/<slug>/`
   — the PRD, `01-gap-analysis.md`, `02-tech-design.md` (incl. the
   acceptance criteria), the dev plan slice spec, and the slice log. Both
   lanes judge the diff against what was *required and designed*, not
   merely against what looks reasonable in isolation. A slice PR is
   validated against its slice spec; a final PR against the whole feature's
   acceptance criteria.

## Requirements validation (mandatory, spans both lanes)

Before ranking findings, each reviewer answers, with evidence:
- Does the code do what the PRD / tech design says it should? Cite the
  requirement (PRD § or acceptance criterion) and the code path that
  satisfies it — or flag it unmet.
- Did anything get built that ISN'T in the design (undocumented scope /
  drift)? That is a finding, not a bonus.
- Are claimed behaviors actually verified? Do not assert a test passed
  unless it was run (see deterministic checks above); explicitly list what
  remains unverified.
Unmet acceptance criteria are blockers; silent drift is at least major.

## The two lanes

Scale to the diff: for small diffs (< ~150 lines) run both lanes yourself
sequentially; otherwise dispatch the named agents in parallel, each with the
subagent contract from `_shared/handoff-format.md` §2 and the exact diff +
context paths.

1. **Correctness, security & code quality** (`code-reviewer` agent):
   - *Correctness*: logic errors, edge cases, error handling, races, broken
     cross-repo contracts.
   - *Security & data*: raw SQL/injection, N+1s, missing tenant/ownership
     scoping,
     unsafe migrations (index add/remove without `CONCURRENTLY`, or a
     backfill in one transaction on an existing large table); unvalidated
     input crossing trust boundaries (client → backend, LLM output →
     anything), secrets handling, conditional side effects; hot-path
     efficiency only (no micro-nitpicks).
   - *Structural code quality* (thermo-nuclear lens — reframing-first, judge
     what the diff could DELETE, not just whether it works):
     - Structural simplification: is there a "code judo" move that removes a
       whole branch/concept rather than rearranging it?
     - Complexity growth: new conditionals bolted onto unrelated paths;
       one-off booleans/nullable modes muddying control flow; orchestration
       made more sequential/less atomic than needed.
     - Decomposition: a file pushed past ~1000 lines is a presumptive
       blocker — extract before expanding.
     - Directness & boundaries: thin/identity wrappers, unnecessary casts /
       `any` / optional params obscuring contracts; "magic" hidden
       assumptions.
     - Canonical discipline: feature logic leaking into general-purpose
       modules; duplicating an existing helper instead of reusing it.
     Behavior is assumed preserved — these findings are about restructuring,
     not changing what the code does. Rank the biggest missed simplification
     as major, not nit, when it would delete real complexity.
2. **Design & requirements** (`design-reviewer` agent): implementation vs
   tech design (modules, contracts, data-flow) and vs Figma (states, copy,
   layout) when UI changed; undocumented drift is a finding.

## Verify, then report

- Every finding must be **verified before reporting**: re-read the actual
  code (not just the diff hunk), confirm the failure scenario is reachable,
  and attach file:line. Drop anything you can't substantiate — a review full
  of maybes trains people to ignore it.
- Rank: blocker → major → minor → nit.
- Output: findings table in chat (severity, lane, file:line, failure
  scenario, suggested fix). If the user wants, post to the PR via
  `gh pr review` / `gh pr comment` — ask first.
- Append a manifest handoff entry (stage: review-PR#, inputs: the reviewed
  head commit SHA, outputs: finding count by severity, next: fixes or merge).
  Reviews never change stage/gate/slice state.
- Before acting on findings from an earlier review (e.g. from a handoff doc),
  re-verify each against current HEAD first — restructuring since the review
  can make a finding already-fixed or moot. Don't "fix" what's gone.

## After fixes

Re-review only the deltas plus any lane that had blockers. Merge happens only
on the user's say-so; `raise-pr` records the merge in the manifest.
