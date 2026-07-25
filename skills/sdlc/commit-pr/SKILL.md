---
name: commit-pr
description: |
  One-shot "ship this": turns the current working tree into a formatted
  commit, pushes the branch, and opens the PR — by running `checkpoint` then
  `raise-pr`, adding only the push step itself. Use when asked to "commit and
  open a PR", "ship this", or "commit, push, PR".
---

# Commit + PR

This skill owns nothing except the **push** step and the ordering. It is a
front door, not a third implementation.

| Step | Owned by |
|---|---|
| Branch check, diff review, pre-commit gate, commit message format | `checkpoint` |
| Push the branch with upstream tracking | this skill |
| PR target, PR body, `gh pr create`, manifest/state recording | `raise-pr` |

Which to invoke: **`checkpoint`** to commit only. **`raise-pr`** when the
work is already committed and pushed. **`commit-pr`** for the whole hop in
one go. Never re-derive a commit message or PR body here — read
`_shared/branch-commit-conventions.md` through those two skills.

## Steps

1. Run `git status` and `git diff` in the repo. If there are changes you
   weren't asked about, name them and ask before staging — never fold
   unrelated work into the commit, and never discard or rewrite it.
2. Invoke `checkpoint` for the commit (it validates the branch name, runs the
   pre-commit gate, and formats the message). If it stops — wrong branch,
   failing checks, forbidden files staged — stop here and report; do not push
   a commit that gate rejected.
3. Push: `git push -u origin HEAD`. If the branch already tracks a remote,
   plain `git push`. Report the failure as-is if it's rejected (diverged
   branch, protected branch) rather than forcing anything — `--force` and
   `--force-with-lease` are out of scope for this skill.
4. Invoke `raise-pr` for the PR. It decides the base branch, builds the body,
   confirms with the user before creating, and records state.
5. Report the commit hash, the branch, and the PR URL.

## Rules

- One repo per invocation. A change spanning repos runs this once per repo,
  in the merge order the dev plan's compatibility matrix gives.
- One logical change per commit; if the tree holds two, run `checkpoint`
  twice before pushing rather than committing a blob.
- The PR is outward-facing: `raise-pr` asks the user before creating it, and
  that confirmation is not something this skill may skip or pre-answer.
