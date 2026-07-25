# Retrospective — <feature title>

- **Feature**: `<slug>`
- **Final PR(s)**: <urls, with merge dates — or "open" for a pre-merge batch>

> A retro can run several times per feature. Each feedback batch **appends** a
> new section; nothing here is overwritten.

---

## Batch 1 — <YYYY-MM-DD> (<source: QA / PM / production / final-PR review>)

<Pre-merge batch? Say so here — the manifest transitions are skipped and
fixes land as follow-up commits on the feature branch, not a bug branch.>

### Feedback items

Reproduce before classifying. "Could not reproduce" is a valid, useful
classification — record what you tried.

| # | Reported | Classification | Reproduced? | Action |
|---|---|---|---|---|
| F1 | <what they saw> | bug | yes | `bug/<desc>` → PR <url> |
| F2 | <what they saw> | design gap | yes | new slice 04 / new intake |
| F3 | <what they saw> | doc gap | n/a | fixed in this retro |
| F4 | <what they saw> | works-as-intended | yes | explained to <who> |

Classifications: `bug`, `design gap`, `doc gap`, `works-as-intended`.
Design gaps are never silently absorbed — they become a new slice (if
pre-GA) or a new mini-feature intake (if scope actually changed).

### Documentation brought back in line with reality

| Document | What was wrong | Now says |
|---|---|---|
| `02-tech-design.md` | <drift from as-built> | <corrected> |
| `_shared/repo-map.md` | <command/URL that proved wrong> | <corrected> |
| `03-dev-plan.md` | <annotation> | <annotation> |

<If a `technical-doc.md` was published, regenerate it via `/to-technical-doc`
rather than patching it, and note that here.>

### Loop lessons

For every feedback item: **which pipeline stage should have caught this?**
The answer is a concrete edit to that skill, template or checklist — not a
resolution to be more careful.

| # | Item | Stage that should have caught it | Concrete edit | Applied? |
|---|---|---|---|---|
| L1 | F1 | `review` | <the exact line to add to the skill> | proposed / applied |
| L2 | F2 | `feature-intake` | <edit> | proposed / applied |

Architectural lessons become ADRs in `docs/adr/` — link them:
- <docs/adr/NNNN-….md>

### Batch outcome

- Items: <n> — bugs <n>, design gaps <n>, doc gaps <n>, works-as-intended <n>
- Still open: <what, and where it's tracked>
