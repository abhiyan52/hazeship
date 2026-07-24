---
name: raise-pr
description: |
  Raises PRs via gh following the project's branch/commit/PR conventions and
  records slice/final merges in the manifest. Slice PRs target the feature
  branch; the final feature PR targets the repo's staging branch. Use when
  asked to "raise a PR", "open the slice PR", "PR to staging", or to record
  that a PR merged.
---

# Raise PR

Read `_shared/branch-commit-conventions.md` (PR body format, targets,
risk-based PR policy) and the project's `_shared/repo-map.md` (staging
branch per repo; copy it from `_shared/repo-map.template.md` if it doesn't
exist yet). One PR per repo per invocation-target; cross-repo slices
get one PR in each affected repo, opened in the merge order from the dev
plan's compatibility matrix.

## Determine the target

- **Slice PR**: head `feat/<slug>-slice-<NN>` → base `feat/<slug>`.
  Requires slice state `user-approved` (`tools/sdlc show <slug>`). If the
  dev plan waived this slice's PR (low-risk policy), skip PR creation: merge
  the slice branch into `feat/<slug>` locally, push, and record
  `tools/sdlc slice <slug> <NN> merged`.
- **Final feature PR**: head `feat/<slug>` → base repo's staging branch
  (`staging` / `main` / `development` per repo-map). Requires stage
  `validate` with gate `approved`; first step is
  `tools/sdlc transition <slug> final-pr` (the tool refuses if validation
  wasn't approved).
- **Bug fix PR**: head `bug/<desc>` → base staging branch (no manifest).

## Steps

1. Preconditions: working tree clean, branch pushed (`git push -u origin
   HEAD` — confirm with user if not yet pushed), slice log/validation doc
   up to date.
2. Build the body from the slice log (slice PR) or validation report (final
   PR) using the commit/PR template in `_shared/branch-commit-conventions.md`:
   What / Why / How to test / Compliance checklist. Link
   `docs/features/<slug>/` and the manifest commit in the meta repo. Check
   the compliance boxes only if actually verified — otherwise leave
   unchecked and say why.
3. `gh pr create --base <base> --head <head> --title "..." --body-file <tmp>`
   (write the body to the scratchpad, not the repo), following the title and
   body format defined in `_shared/branch-commit-conventions.md`. Ask the
   user before creating — a PR is outward-facing.
4. Record state: slice PR → `tools/sdlc slice <slug> <NN> pr-raised --pr <url>`;
   final PR → append a manifest handoff entry (stage: final-pr, outputs: PR
   URLs, next: review). Update the slice log.
5. Suggest running the `review` skill on the fresh PR.

## Recording merges (this skill owns them)

When asked to record a merge (or after the user merges):
- Confirm via `gh pr view <url> --json state,mergedAt` — never record a
  merge you haven't verified.
- Slice PR merged → `tools/sdlc slice <slug> <NN> merged` and delete the
  slice branch.
- Final PR merged (all repos) → the `retro` skill runs
  `tools/sdlc transition <slug> retro`; remind the user.
