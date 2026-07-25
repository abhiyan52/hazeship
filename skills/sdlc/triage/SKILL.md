---
name: triage
description: |
  Turns a support ticket or client-reported issue into an evidence-backed
  diagnosis with a verdict: data/config issue, code bug, not-a-bug, or
  needs-info. Drives ssh-readonly-investigation for production evidence and
  never changes any system. Use when asked to "triage this ticket",
  "investigate this client issue", or "what's going on with <client>".
---

# Triage (ticket → evidence-backed diagnosis)

Diagnosis only. This skill reads systems and produces a verdict; it never
fixes anything. Fixes happen through `bugfix` (code) or through explicit,
user-approved runbook steps outside this skill (data/config).

Read `_shared/handoff-format.md` §0 (first-run bootstrap) and the project's
`_shared/repo-map.md` first. If the project uses `persistent-memory`, read
the bucket for this client/host before connecting anywhere — prior triages
often already hold the wrapper commands, known quirks, and past verdicts.

## Inputs (ask for whatever is missing)

- The ticket: pasted text, a tracker link, or a client email. Extract: who
  reported it, what they saw, what they expected, when it started, which
  environment/client/tenant.
- The client/host label — it must resolve to a repo-map **Remote hosts**
  entry or an explicit SSH target from the user. Never guess a hostname.

## Work ledger first

Run the `work-log` dedup gate before investigating: if this ticket (or its
symptom) is already an open or done item, report that instead of
re-triaging. Otherwise open an item (`--source clickup` with the ticket URL
as `--ref`, or `telegram`/`direct`), and on the verdict: `link` the triage
report, note the verdict, and either close the item (`done`) or keep the
SAME item open for the `bugfix` handoff.

## Steps

1. **Restate the symptom** as one falsifiable sentence ("client X's export
   has produced 0 rows since <date>") and confirm it with the user if the
   ticket is vague. A triage that starts from a fuzzy symptom ends in a
   fuzzy verdict.
2. **Check the code path first, locally.** Read the relevant code in the
   project repos and form 2–3 ranked hypotheses (data, config, code, or
   external dependency) *before* touching production. Each hypothesis must
   name the evidence that would confirm or kill it.
3. **Gather production evidence** via `ssh-readonly-investigation` — one
   bounded question per hypothesis (counts, log excerpts, config values,
   job/queue state). Read-only, always; that skill's guardrails apply
   verbatim. Stop collecting when one hypothesis is confirmed and the
   others are dead — don't keep fishing.
4. **Write the triage report** to `docs/triage/<YYYY-MM-DD>-<slug>.md`:
   symptom, hypotheses with the evidence for/against each (exact commands
   and dates included), and the verdict.
5. **Hand off by verdict**:
   - **Code bug** → scaffold the `bugfix` intake: reproduction steps, the
     suspected files/paths, and the confirming evidence. Offer to start
     `bugfix` now.
   - **Data/config issue** → exact corrective steps for a human to run (or
     for the user to approve running), never executed from this skill.
   - **Not a bug** → a client-facing explanation the user can forward,
     grounded in the evidence, with no internal hostnames/paths in it.
   - **Needs info** → the specific missing facts, phrased as questions the
     support team can send back to the client.
6. **Record what you learned** in the `persistent-memory` bucket for the
   client (wrapper shapes, log locations, recurring patterns) so the next
   triage starts warm. Never store customer data in the bucket — the
   repo-map's data-handling rules apply to triage notes too.

## Report shape (chat)

Verdict first, one line. Then: evidence table (hypothesis → command →
result → confirmed/killed), the handoff produced, and anything observed but
unconfirmed — flagged, not smoothed over.
