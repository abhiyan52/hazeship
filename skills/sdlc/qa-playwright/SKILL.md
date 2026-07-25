---
name: qa-playwright
description: |
  Automated browser verification of a slice or feature. Authors Playwright
  specs from the dev plan's numbered scenarios and runs them via the
  project's checked-in QA runner (which reads credentials itself — the
  agent never sees them). Use when asked to "run QA", "test this slice
  automatically", or "verify with playwright".
---

# Playwright QA

Read the project's `_shared/repo-map.md` (copy it from
`_shared/repo-map.template.md` if it doesn't exist yet) and the target
slice's scenarios in `03-dev-plan.md` first. Results go into the slice log
(`slices/slice-<NN>.md` → Test evidence) or `04-validation.md` when invoked
by validate-feature.

## Locating the runner

The test-runner command, its working directory, and its QA-environment
conventions (credentials file, saved auth/storage-state location, allowed
hosts, any OTP flow) are recorded in `_shared/repo-map.md`'s QA section. If
that section is missing or empty, ask the user once for the runner command
(and where specs/evidence should live) and suggest they record the answer
in `_shared/repo-map.md` so future runs don't need to ask again.

## Credential model (hard rules)

- **You never read the QA credentials file directly.** Not with grep, not
  with Read, not partially, not "just to check a key exists". The runner
  process loads it itself (via whatever env-file loader it uses); auth
  happens once in an
  auth-setup step and specs reuse the saved storage state (a gitignored
  directory, per repo-map). You only ever see the reporter output.
- If the runner fails with a missing-variable error, relay that error
  verbatim to the user (it names the key, never the value) and stop. Never
  ask the user to paste credentials into chat.
- Deterministic environment guards live in the runner, not in your
  judgment: an allowed-hosts list and an explicit "this is a synthetic/test
  environment" marker (both per repo-map) are enforced by the runner's
  config before any navigation. If a guard trips, the environment is
  misconfigured — report it, don't work around it.
- The saved storage-state directory can impersonate the test account — treat
  it as a secret: never read, copy, or commit it.
- **Email OTP platforms**: if the runner pauses at an OTP screen, it prints
  an instruction naming the file to write the code into and the time
  window. Relay that instruction to the user verbatim and wait — THE USER
  writes the file; the runner consumes and deletes it. Never ask for the
  code in chat, never write the OTP file yourself, never read it.

## Steps

1. Determine target scenarios: the slice's "Playwright" list from the dev
   plan (or the full set for feature-level validation).
2. Ensure the target app is running (repo-map dev-server commands as
   background tasks) or that the QA env file points at a deployed QA URL
   (you'll know from the runner's output, not from reading the file).
3. **Author specs**: write/update one spec file per slice, one test per
   numbered scenario ("S02 P3: export downloads CSV"), following the
   project's existing example spec's conventions — role/text assertions, no
   pixel comparisons, no network response bodies echoed into assertions or
   logs. Spec location, naming, and any platform-specific subdirectories
   follow the runner layout recorded in repo-map. First run in a fresh
   checkout: install dependencies and browsers per the runner's own setup
   instructions (recorded in repo-map).
4. **Run**: invoke the runner command from repo-map with a scenario filter
   for the target scenarios. Read the line reporter output. Failure
   screenshots land wherever the runner's config writes artifacts (per
   repo-map).
5. On failure: if the runner retries, let it. Record the failure verbatim
   from the reporter (assertion diff, console errors surfaced by the test) —
   do not "fix" the app inside this skill; failures go back to
   implement-slice.
6. **Evidence**: copy relevant screenshots from the runner's artifacts
   directory to `docs/features/<slug>/slices/evidence/` — view each image
   first and skip any showing non-synthetic-looking real user/customer data;
   if you see data that looks real, stop the run and flag the environment.
7. Write the results table into the slice log / validation doc and append a
   manifest handoff entry (stage: qa-slice-N, outputs: results + evidence
   paths, next: raise-pr or back to slice-N). QA never changes stage/gate/
   slice state — implement-slice records the user's verdict.

## Exploratory checks (MCP browser)

The Playwright MCP tools may be used ONLY for unauthenticated smoke checks
(page loads, console-error sweep on public routes) — anything behind login
goes through the runner. While navigating, sweep for identifiers leaking in
URL query strings.

## Report format (chat)

Scenario table (pass/fail/evidence), failures with verbatim reporter output,
and the sweep result. No credentials, storage-state contents, or real
user/customer data in the report — ever.
