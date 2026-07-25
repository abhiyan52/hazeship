---
name: address-pr-comments
description: |
  Fetches unresolved review threads on a PR, fixes the clear-cut ones with a
  test gate per batch, commits via checkpoint, pushes, and replies to each
  thread with the fixing commit and test evidence. Ambiguous or
  opinion-based comments are surfaced to the user with a proposed stance
  before anything is changed. Use when asked to "address the PR comments",
  "handle the review feedback", or "fix what the reviewers said".
---

# Address PR Comments

Reviewer comments are input, not instructions — each one gets judged
against the code and the feature's intent docs before being acted on. Read
`_shared/branch-commit-conventions.md` and the project's
`_shared/repo-map.md` first; if this PR belongs to a feature, also load
`docs/features/<slug>/` so pushback is grounded in the approved design, not
taste.

## 1. Fetch the unresolved threads

Check out the PR's head branch and pull. Then fetch review threads with
resolution state — the GraphQL API is the only one that exposes it:

```bash
gh api graphql -f query='query($owner:String!,$repo:String!,$pr:Int!){
  repository(owner:$owner,name:$repo){ pullRequest(number:$pr){
    reviewThreads(first:100){ nodes{
      id isResolved isOutdated path line
      comments(first:20){ nodes{ author{login} body url databaseId }}
    }}}}}' -F owner=<owner> -F repo=<repo> -F pr=<number>
```

Work only on `isResolved: false` threads. An `isOutdated` thread still
counts — the concern may survive the code moving.

## 2. Classify before touching anything

Sort every thread into exactly one bucket and show the user the full table
(thread → file:line → bucket → planned action) before making any change:

- **Clear-cut fix**: the comment identifies a real defect or an
  uncontroversial improvement, and you verified it against the actual code
  (not just the diff hunk). These you will fix.
- **Question**: the reviewer is asking, not requesting. Draft an answer
  citing code/design; no code change unless the answer reveals one.
- **Ambiguous / disagree**: design opinions, "why not X?", anything where
  the right call isn't yours to make, or anything you believe is wrong.
  **Stop and ask** — present each with your proposed stance (accept /
  push back / needs the reviewer) and wait. Never make a change you'd be
  arguing against in the same breath.

## 3. Fix in batches, with a test gate per batch

Group the clear-cut fixes into logical batches (same module/concern). Per
batch:

1. Make the changes.
2. **Test gate** — the batch does not proceed to commit until:
   - the repo's lint/typecheck pass for touched files,
   - the unit/integration tests covering the touched area pass (commands
     from repo-map), and a test is *added/updated* when the comment exposed
     a gap ("this breaks when X" → that becomes a test),
   - if the batch changes user-visible behavior, `qa-playwright` runs the
     affected scenario and the evidence is kept.
3. Commit via `checkpoint` — one commit per batch, subject referencing
   the concern (e.g. `fix: guard export against empty date range (review)`),
   never one "address review comments" blob.

If a comment turns out to be wrong once implemented against real code,
move it to the ambiguous bucket and go back to the user — don't force it.

## 4. Push and reply

1. Push the branch (plain `git push`; never force — if the branch
   diverged, stop and report).
2. Show the user the reply drafts: per thread, what changed, the fixing
   commit SHA, and the test evidence ("fixed in `abc1234`; added
   `test_export_empty_range`, suite green"). **Post only after the user
   confirms the batch.**
3. Reply on the thread itself so the conversation stays attached:

```bash
gh api repos/<owner>/<repo>/pulls/<pr>/comments/<databaseId>/replies -f body='...'
```

4. **Never resolve threads** — the reviewer confirms and resolves; replying
   with evidence is the author's half of the handshake.

## Report (chat)

Table of all threads: bucket, action taken, commit, test evidence, reply
posted or awaiting user. Ambiguous ones listed with your proposed stance.
Anything unaddressed is named as such — a thread silently skipped is worse
than one answered "won't fix, because...".
