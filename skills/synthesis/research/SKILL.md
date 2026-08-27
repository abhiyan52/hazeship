---
name: research
description: Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, reading legwork delegated to a background agent, or when another skill needs grounding before it designs.
---

Spin up a **background agent** to do the research, so you keep working while it reads.

Its job:

1. Investigate the question against **primary sources** — official docs, source code, specs, first-party APIs — not a secondary write-up of them. Follow every claim back to the source that owns it.
2. Write the findings to a single Markdown file, citing each claim's source.
3. Save it where the repo already keeps such notes; match the existing convention, and if there is none, put it somewhere sensible and say where.

## Primary sources in this workspace

Ranked by trust, highest first. A claim from a lower tier that contradicts a
higher one is a **finding**, not a fact — record the contradiction.

1. **The five sub-repos' own code and migrations** — `_shared/repo-map.md` maps
   them. The code is the only authority on what the system does today.
2. **`docs/adr/`** — the decisions behind the code, and the reason a surprising
   implementation is deliberate.
3. **`CONTEXT.md`** (workspace root, when it exists) — the canonical term for
   each domain concept.
4. **Prior features' artifacts** — `docs/features/*/02-tech-design.md`,
   `05-retro.md`, and `bugs/` carry hard-won constraints that no external doc
   knows.
5. **First-party vendor docs and specs** — for anything external (payer APIs,
   HL7/FHIR, Django and Celery behaviour). Prefer the version the repo actually
   pins over the latest release.

## Rules

- **No PHI in the findings file.** Quote schemas, field names, and synthetic
  values — never a real patient record, and never a production identifier, even
  one pasted into the question. See `_shared/phi-hipaa-checklist.md`.
- **Never read `.env.qa`** or any credential file to answer a research question.
- **Cite as you go.** A file path with a line number, an ADR number, or a URL
  against each claim. An uncited claim reads as fact and is the failure mode
  this skill exists to prevent.
- **Separate the known from the inferred.** Findings the sources state
  outright, and conclusions you drew, belong under different headings — a
  reader must be able to tell which is which without re-reading the sources.
- **Say what you could not establish.** An open question named explicitly is
  worth more than a confident guess, because the next stage can route it to a
  human. Unanswerable questions become `team-handoff` items.

## Where the findings land

- **Inside a feature's SDLC run** — `docs/features/<slug>/00-research.md`, the
  numbered artifact preceding `01-gap-analysis.md`. Read `_shared/handoff-format.md`
  §2 for the subagent contract before dispatching.
- **Outside a feature** — `docs/research/<topic-slug>.md`, and say where you
  put it.

`00-research.md` is **not** a gate artifact: `tools/sdlc` approves the intake
stage on `01-gap-analysis.md`. Research grounds that document; it does not
replace it.
