---
name: checkpoint
description: |
  Creates a commit in the project's required format (What we built / Why /
  How to test). Use when asked to "checkpoint", "commit this", or when
  implement-slice completes a task. Validates branch naming before
  committing.
---

# Checkpoint (formatted commit)

Read `_shared/branch-commit-conventions.md` for the full commit message
format. This skill commits in ONE repo at a time; if the working set spans
repos, run once per repo.

## Steps

1. Identify the repo (`git -C <repo> status`). Verify the current branch
   matches `feat/*` or `bug/*` (or a slice branch `feat/*-slice-*`). If on a
   staging/default branch, STOP — never commit directly to staging branches.
2. Review the diff (`git diff` + `git status`), and split unrelated changes
   into separate commits rather than one blob.
3. **Pre-commit gate** (all must pass before committing):
   - Repo's lint/typecheck/test commands for touched areas (repo-map has the
     commands; don't skip because "it's a small change").
   - No forbidden files staged: `.env*`, credentials, dumps, `.docx` (unless
     explicitly requested), files with plausible real user/customer data.
4. Compose the message exactly per `_shared/branch-commit-conventions.md`:
   subject `<type>: <imperative ≤72 chars>`, body with `What we built:` /
   `Why:` / `How to test:` sections, and the trailer that convention
   specifies. "How to test" must be executable — a command or a click-path
   with expected result, not "run the tests".
5. Commit. Update the slice log's commit table. Push only if the user asked
   or the flow (raise-pr) requires it.
