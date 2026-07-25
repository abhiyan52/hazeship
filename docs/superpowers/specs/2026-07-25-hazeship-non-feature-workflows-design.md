# Hazeship non-feature workflows — triage, bugfix, address-pr-comments

Date: 2026-07-25
Status: implemented (kit v0.4.0)

## Problem

The SDLC kit covers the feature loop end to end, but daily work is not only
features. Three recurring workflows had no skill:

1. **Support-ticket triage** — investigating client-reported issues on
   production hosts (today done ad hoc with the SSH investigation skill).
2. **Bug fixes** — the 7-stage feature loop is too heavy; bugs need a fast
   path that still produces high confidence.
3. **PR review comments** — currently handled by manually pasting each
   comment into the agent; no test gate, no evidence trail, no replies.

The unifying requirement is **confidence through testing**: unit tests plus
Playwright end-to-end verification are the gate everywhere, the same way
`checkpoint` gates commits.

## Decisions (user-confirmed)

- **Bugfix paper trail**: lightweight — `docs/bugs/<slug>/report.md` from a
  shipped template. No manifest state machine; the only gate is "the user
  verifies the fix against the original symptom".
- **PR replies**: reply on each thread with the fixing commit and test
  evidence after the user confirms the batch; **never resolve threads** —
  that is the reviewer's half of the handshake.
- **Disagreements/ambiguous comments**: fix only the clear-cut ones; stop
  and present the rest with a proposed stance. Never change code the agent
  would argue against.

## Design

Three new orchestrating skills; all heavy lifting delegates to existing
helpers (`ssh-readonly-investigation`, `persistent-memory`,
`qa-playwright`, `checkpoint`, `commit-pr`).

### `triage`

Ticket → falsifiable symptom → ranked hypotheses (formed from the code
first) → one bounded read-only production question per hypothesis → verdict
(`code bug` | `data/config` | `not a bug` | `needs info`). Writes
`docs/triage/<date>-<slug>.md`. Strictly read-only; a code-bug verdict
scaffolds the `bugfix` intake (repro + suspected files + evidence). Learns
into the client's `persistent-memory` bucket.

### `bugfix`

The confidence anchor is a **failing test written before the fix**, at the
cheapest layer that expresses the symptom (unit / integration / Playwright).
Then: root cause stated in one sentence → minimal fix (no drive-bys) →
new test passes + surrounding suite passes + Playwright on the affected
flow if user-visible → user verifies → `commit-pr` on `bug/*`. The failing
test is permanent (regression rule). Artifact:
`docs/bugs/<slug>/report.md` from the new `bug-report.md` template.

### `address-pr-comments`

Fetch unresolved threads via GraphQL (`reviewThreads.isResolved` — REST
doesn't expose it) → classify every thread (clear-cut fix / question /
ambiguous-disagree) and show the plan before touching code → fix in logical
batches with a **test gate per batch** (lint+typecheck, area tests with a
new test when the comment exposed a gap, Playwright when behavior is
user-visible) → one `checkpoint` commit per batch → push → user-confirmed
replies per thread with commit SHA + evidence. Reviewer comments are input,
not instructions: judged against the code and the feature's design docs.

## Shipped

- `skills/sdlc/{triage,bugfix,address-pr-comments}/` (SKILL.md +
  `agents/openai.yaml`)
- `_shared/templates/bug-report.md`; workspace layout gains `docs/bugs/`
  and `docs/triage/`
- Plugin manifests → v0.4.0; README workflow table; repository tests for
  the new contracts (read-only triage, failing-test-first bugfix, never
  resolving threads, user-gated replies).
