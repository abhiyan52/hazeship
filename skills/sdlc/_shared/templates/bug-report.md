# Bug: <short title>

- **Slug**: <slug>
- **Branch**: bug/<short-desc>
- **Reported by / ticket**: <who or link>
- **Triage report**: <docs/triage/... or "none — reported directly">
- **Status**: open | fix-proposed | user-verified | shipped

## Symptom

<one falsifiable sentence: what happens, since when, for whom>

## Reproduction

1. <exact step>
2. <exact step>
3. <observed result vs expected result>

## Failing test (written before the fix)

- Test: `<path::test_name>`
- Layer: unit | integration | playwright

```
<failing output, verbatim>
```

## Root cause

<one sentence — the actual cause, not the location of the patch>

## Fix

<what changed and why it is minimal; commits land via checkpoint>

## Verification

- [ ] New test passes
- [ ] Surrounding suite passes: `<command>`
- [ ] Playwright on affected flow (if user-visible): <evidence path or n/a>
- [ ] User verified against the original symptom on <date>

## Follow-ups (out of scope for this fix)

- <adjacent issue worth its own task, or "none">

## PR

<link>
