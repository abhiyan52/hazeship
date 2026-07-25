# Gap Analysis — <feature title>

- **Feature**: `<slug>`
- **PRD**: <path or URL, with the sections read>
- **Design**: <authoritative Figma link from the manifest — never the PRD's embedded link>
- **Repos touched (expected)**: <from _shared/repo-map.md>
- **Date**: <YYYY-MM-DD>

## 1. Shared understanding

<One or two paragraphs, in your own words: the user problem, who has it, and
what "done" looks like behaviourally. If you cannot write this without
hedging, the gaps below are bigger than they look — say so.>

## 2. Scope

**In scope** (from the PRD):
- <behavior>

**Explicitly out of scope**:
- <behavior, and where it's deferred to>

## 3. Acceptance criteria (verbatim from the PRD)

| # | Criterion | Source |
|---|---|---|
| AC1 | <criterion as written in the PRD> | PRD §<n> |

> Copy these verbatim — `validate-feature` walks this list at the end and
> paraphrasing here becomes a moved goalpost there.

## 4. Design coverage

One row per screen/flow in the design. A missing state is a gap, not a detail.

| Screen / flow | Figma node | States covered | States missing |
|---|---|---|---|
| <name> | <node-id> | default, loading, empty, error, permission-denied | <e.g. error> |

## 5. Codebase findings

| Repo | Module / path | Relevance | Reuse or conflict |
|---|---|---|---|
| <repo> | `<path>` | <what it does today> | <pattern to reuse / assumption it breaks> |

## 6. Gaps

Every gap gets a row. `Owner` is who can answer it, not who will code it.

| # | Type | Gap | Impact if unresolved | Owner | Status |
|---|---|---|---|---|---|
| G1 | PRD↔Figma | <mismatch> | <consequence> | PM | open |
| G2 | PRD ambiguity | <what's underspecified> | <consequence> | PM | open |
| G3 | Design↔code | <conflict> | <consequence> | Eng | open |
| G4 | PRD↔code | <conflict> | <consequence> | Eng | open |

Types: `PRD↔Figma`, `PRD ambiguity`, `design state missing`, `design↔code`,
`PRD↔code`, `data handling`.

## 7. Data handling

Anything this feature will store, log, display, export or send to a third
party, judged against the data-handling rules in `_shared/repo-map.md`.
State "no sensitive data" explicitly and say why, rather than omitting the
section — the tech design has to answer this either way.

| Data | Where it flows | Sensitivity | What the tech design must address |
|---|---|---|---|
| <field/entity> | <path through the system> | <none/low/medium/high> | <requirement> |

## 8. Open questions (blocking)

Numbered, each with the options you can see — a question with concrete
options gets answered far faster than an open one.

1. <question> — options: (a) <…> (b) <…>. Blocks: <stage>.

> These go to humans. Route anything that needs tracking through
> `/team-handoff`, and record the id here.

## 9. Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| <risk> | low/med/high | low/med/high | <mitigation> |
