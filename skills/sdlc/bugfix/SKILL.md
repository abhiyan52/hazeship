---
name: bugfix
description: |
  Lightweight loop for fixing a bug: reproduce it as a failing test first,
  make the minimal fix, prove the test now passes, verify the user-facing
  flow with qa-playwright, then ship via commit-pr on a bug/* branch. Use
  when asked to "fix this bug", "this is broken", or when triage hands off
  a confirmed code bug.
---

# Bugfix (failing test → minimal fix → verified PR)

The feature loop's seven stages are too heavy for a bug. This loop has one
artifact, one branch, and one gate: **the user verifies the fix before it
ships**. Read `_shared/handoff-format.md` §0 (first-run bootstrap),
`_shared/branch-commit-conventions.md`, and the project's
`_shared/repo-map.md` first.

## Inputs

- Reproduction steps, or a `triage` handoff (which already carries them
  plus suspected files and production evidence).
- If reproduction steps are missing, getting them IS the first task — a
  bug you can't reproduce is a triage, not a bugfix; switch to `triage`.

## Work ledger first

Run the `work-log` dedup gate before touching anything: if the bug is
already an open item (another actor may have picked it up) or a done item,
report that instead of redoing it. A `triage` handoff continues its
existing item — don't open a second one. Otherwise open an item; at step 7,
`link` the PR and bug report and mark it `done`.

## The confidence anchor: failing test first

Before writing any fix, capture the bug as an automated test that **fails
for the reported reason** (assertion matches the symptom, not a setup
error). Choose the cheapest layer that can express it:

- logic/data bug → unit test next to the existing suite for that module
- API/contract bug → integration/request-level test
- user-flow bug → Playwright scenario (authored per `qa-playwright`'s
  conventions and runner)

Run it, paste the failing output into the report. If the bug genuinely
cannot be expressed as a test (e.g. third-party outage, environment-only),
record why in the report and get the user's written OK to proceed without
one — never silently skip it.

## Steps

1. **Scaffold**: `docs/bugs/<slug>/report.md` from
   `docs/templates/bug-report.md` (symptom, repro, evidence/links — carry
   over the triage report path if one exists). Branch: `bug/<short-desc>`
   from the repo's default/staging branch, per
   `_shared/branch-commit-conventions.md`.
2. **Reproduce locally**, then write the failing test (above). Failing
   output goes in the report verbatim.
3. **Find the root cause**, not the first place a patch would mask the
   symptom. State it in one sentence in the report; if you can't, you
   haven't found it — keep digging or say so.
4. **Minimal fix.** No drive-by refactors, no "while I'm here" — anything
   adjacent worth doing is named in the report under "Follow-ups", not
   folded into the fix.
5. **Prove it**:
   - the new test passes,
   - the surrounding suite for the touched area passes (commands from
     repo-map),
   - if any user-visible behavior changed, run `qa-playwright` on the
     affected flow and record the evidence.
6. **User verification gate**: demo the fix (exact commands/click-path),
   wait for the user's verdict, record it in the report. Never ship a fix
   the user hasn't confirmed against the original symptom.
7. **Ship** via `commit-pr` (`fix:` commit; the failing-test-then-fix story
   belongs in "How to test"). Then update the report with the PR link, and
   if this came from a ticket, draft the client-facing "fixed in ..." note
   for the user to send.

## Regression rule

The failing test written in step 2 is permanent — it lands in the same PR
as the fix and is never deleted or weakened to "make CI green". If the fix
makes the test obsolete in form, rewrite it to guard the same regression.
