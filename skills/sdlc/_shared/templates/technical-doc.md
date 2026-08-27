# <Feature title> — Technical Design

- **Status**: Proposed | Approved
- **Related requirement**: <PRD link — one pointer, do not restate the PRD>
- **Date**: <YYYY-MM-DD>

> Stakeholder-facing translation of the engineering tech design. **No repo
> internals**: no file names, paths, module or class names, table or field
> lists. Describe components by responsibility and behaviour at concept
> level. If you find yourself making a design decision here, stop — it
> belongs in `02-tech-design.md` first.
>
> Section numbers are part of the contract (§4 carries the data-protection
> statement, §8 is always last). Every figure gets a numbered caption.

## 1. Summary

<What this feature does and what it changes for the user, in one short
paragraph a non-engineer can read without stopping.>

## 2. Golden flow

The main path, end to end, in the language of the product.

1. <The user does X.>
2. <The system does Y.>
3. <The user sees Z.>

![Figure 1. Golden flow.](diagrams/golden-flow.png)

*Figure 1 — The golden flow from <start> to <finish>.*

## 3. Architecture & invariants

<The components involved and what each is responsible for. Name them by
role ("the export worker"), never by module path.>

![Figure 2. Subsystem map.](diagrams/architecture.png)

*Figure 2 — Components and the direction data moves between them.*

**What always holds true**

- <invariant, in plain language>

## 4. Data handling & protection

One paragraph. What categories of data the feature touches, how they are
protected, and who can reach them — per the project's data-handling rules.
No real or synthetic data examples: this document leaves the building.

<Paragraph.>

## 5. States

<The lifecycle of the central entity. A lifecycle diagram is expected
whenever that entity has states.>

![Figure 3. Lifecycle diagram.](diagrams/states.png)

*Figure 3 — Lifecycle of <entity>.*

| State | Means | Who can move it on |
|---|---|---|
| <state> | <meaning to the user> | <role or system> |

## 6. Failure behaviour

What the user experiences when things go wrong — the section stakeholders
most often find missing.

| If this fails | The user sees | The system does |
|---|---|---|
| <failure> | <message or state> | <retry / queue / abort> |

## 7. Decisions

Decisions a stakeholder would want to know about, with the trade-off named.

| Decision | Chosen because | Trade-off accepted |
|---|---|---|
| <decision> | <reason> | <cost> |

## 8. Open questions

Always last. Merges the tech design's open questions with every **open**
team-handoff for this feature — check their status first and drop anything
since resolved. One short paragraph each: context, the question, what it
affects.

1. <Context sentence. The question? What it affects.> (team-handoff `<slug>#003`)
