# Development Plan — <feature title>

- **Feature**: `<slug>`
- **Inputs**: `02-tech-design.md`, `01-gap-analysis.md`
- **Slices**: <n>
- **Date**: <YYYY-MM-DD>

## Slice overview

A slice is "the user can do X end-to-end", never "all the models" then "all
the APIs". Slice 01 is the walking skeleton: the thinnest path through every
layer the feature touches, so integration risk dies first.

| Slice | Name | Outcome the user can see | Repos | Depends on | PR policy |
|---|---|---|---|---|---|
| 01 | <name> | <demoable outcome> | <repos> | — | required |
| 02 | <name> | <demoable outcome> | <repos> | 01 | required / waived |

**PR policy** comes from the risk rules in
`_shared/branch-commit-conventions.md`. `required` is the default; `waived`
is only for small, single-repo, low-risk slices, and defers review to the
final PR — it never skips it.

## Branch plan

Created by `implement-slice` **after this plan is approved** — do not create
branches now.

| Repo | Feature branch | Target (default/staging) branch |
|---|---|---|
| <repo> | `feat/<slug>` | <from _shared/repo-map.md> |

## Cross-slice risks & sequencing notes

`implement-slice` reads this section as a hard gate before starting a slice.

- <what must land before what, and why>
- Migrations and contract changes that several slices need land in the
  **earliest** slice that needs them: <which>

---

## Slice 01 — <name>

**Outcome**: <what the user can do at the end of this slice.>

**Tasks**

`Dependency` is `blocking` (the next task cannot start) or `non-blocking`
(parallelizable — these are the candidates for parallel subagents).

| # | Task | Repo | Dependency | Notes |
|---|---|---|---|---|
| 1 | <task> | <repo> | — | <notes> |
| 2 | <task> | <repo> | blocking on 1 | <notes> |

**Test strategy**

- *Unit*: <what, where>
- *Integration*: <what, where>
- *Contract* (required at every API/message boundary this slice crosses):
  <which boundary, which test>
- *Playwright scenarios* — executed verbatim by `qa-playwright`, so write
  them as runnable steps, not intentions:

  | # | Scenario | Preconditions | Steps | Expected |
  |---|---|---|---|---|
  | S01 P1 | <name> | <seeded state, role> | 1. <step> 2. <step> | <observable result> |

**Demo script** (what you walk the user through at the feedback point)

1. <step> → <what they should see>

**Data handling notes**

<Which data-handling rules from `_shared/repo-map.md` apply to this slice's
diff, or "none — this slice touches no sensitive data".>

**Definition of done**

- [ ] Tasks complete, unit/integration tests green
- [ ] Playwright scenarios above pass (or are recorded as not-yet-automatable)
- [ ] Demo script walked through once
- [ ] <slice-specific criterion>

### Cross-repo compatibility matrix (only if this slice spans repos)

| Aspect | Decision |
|---|---|
| Merge order | <repo A before repo B, and why> |
| Deploy order | <order> |
| Backward compatibility | <can the old consumer talk to the new producer, and for how long> |
| Feature flag | <name, default, who flips it> |
| Rollback path | <exact steps> |

---

## Slice 02 — <name>

<Same structure as above.>
