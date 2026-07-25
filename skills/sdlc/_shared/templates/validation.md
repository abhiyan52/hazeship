# Validation — <feature title>

- **Feature**: `<slug>`
- **Verdict**: **PASS** | **FAIL**
- **Diff validated**: `git diff <default-branch>...feat/<slug>`
- **Date**: <YYYY-MM-DD>

> Judged against the requirements, not against what the slices happened to
> build. Every row is verified by the strongest method available; "the slice
> log says it works" is not evidence.

## Verdict summary

<Two or three sentences: what was built, what passed, what didn't. On a FAIL,
name the failing rows here — they go back to `implement-slice` as fix work.>

| | Count |
|---|---|
| Requirements validated | <n> |
| Passing | <n> |
| Failing | <n> |
| Accepted deviations | <n> |

## Requirement inventory

Every PRD acceptance criterion, every gap-analysis item marked for
resolution, and every "Definition of done" item from the dev plan. None
skipped, none added silently.

Method, strongest first: `playwright` → `test` → `code-inspection`.

| # | Requirement | Source | Method | Evidence | Result |
|---|---|---|---|---|---|
| AC1 | <criterion> | PRD §<n> | playwright | S02 P1, `evidence/<file>.png` | pass |
| G3 | <gap resolution> | `01-gap-analysis.md` | test | `<test name>` output | pass |
| DoD | <item> | `03-dev-plan.md` slice 02 | code-inspection | `<path>:<line>` | pass |

## Data handling verification

Run over the full feature diff, against the data-handling rules in
`_shared/repo-map.md`.

| Rule | How checked | Result |
|---|---|---|
| <rule> | <command or inspection> | pass / fail / n-a |

## Accepted deviations

Things built differently from the PRD or design, that the user accepted.

| # | PRD/design said | We built | Why | Approved by | Date |
|---|---|---|---|---|---|
| D1 | <expected> | <actual> | <reason> | <who> | <date> |

## Residual risks

Carried into production knowingly.

| Risk | Level | Why accepted | Mitigation / follow-up |
|---|---|---|---|
| <risk> | low/med/high | <reason> | <ticket or plan> |

## Unverified

Anything asserted but not actually run. Be explicit — an unverified claim
listed here is honest; one folded into a pass row is not.

- <what, and why it couldn't be verified>
