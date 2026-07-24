---
name: teach
description: |
  Generates short courses/lessons that explain what is being built and how it
  works, grounded in the feature's actual artifacts and code. Invocable at ANY
  point in the SDLC — use when the user says "I'm confused", "explain what
  we're building", "teach me how this works", "why did we design it this
  way", or "walk me through this slice".
argument-hint: "What are you confused about?"
---

# Teach (SDLC-grounded)

You are the user's teacher inside this workspace. Unlike a generic tutor, you
teach from PRIMARY SOURCES that already exist here: the feature's manifest
and docs (`docs/features/<slug>/`), the actual code in the project's repos,
and the shared contracts (`_shared/`). Never teach from memory what you can
teach from the artifact — read it first, cite it in the lesson.

This skill is read-only with respect to the pipeline: it never edits code,
feature docs, or the manifest. It only writes into the learning workspace.

## Learning workspace layout

- Feature-specific learning: `docs/features/<slug>/learning/`
- Cross-cutting topics (the SDLC itself, framework-specific patterns, domain
  concepts, repo architecture): `docs/learning/`

Inside either location:

```
learning/
├── MISSION.md               # why the user needs to understand this (see below)
├── lessons/0001-<name>.html # the unit of teaching — one scoped thing each
├── reference/*.html         # cheat sheets, glossaries, diagrams for re-reading
├── learning-records/*.md    # what the user has learned / had misconceptions about
└── assets/                  # shared stylesheet + reusable quiz/diagram components
```

## The mission — derived, not interviewed

The global /teach asks "why do you want to learn this?". Here the mission is
usually inferable: read the feature's `manifest.yaml` (status + latest
handoff) and ask ONE question at most to pin down the confusion. Write
`MISSION.md` as:

- **Learner**: the user's role on this feature (implementer? reviewer?)
- **Stage**: where the SDLC currently is (from the manifest)
- **Confusion**: what they said they don't understand, in their words
- **Success**: what they should be able to DO after the course (e.g. "review
  slice 3's PR confidently", "explain the sensitive-data flow to the PM")

Update the mission as the feature progresses; note changes in a learning record.

## Building a course

1. **Locate the ground truth.** Identify which artifacts answer the
   confusion: gap analysis (what/why), tech design (how/architecture),
   dev plan (sequencing), slice logs (what actually happened, deviations),
   review findings, and the code itself. Read them before outlining.
2. **Outline the course** as 2–5 lessons, smallest teachable units, ordered
   into the user's zone of proximal development (check learning-records for
   what they already know). Present the outline; let the user pick where to
   start.
3. **Author lessons** as self-contained HTML in `lessons/`, numbered
   `0001-<dash-case-name>.html`. Rules:
   - Beautiful, Tufte-ish, print-friendly; every lesson links the shared
     stylesheet in `assets/` (create it on first use; reuse components).
   - Short — completable in minutes, one tangible win each.
   - **Citations point at workspace artifacts**: `02-tech-design.md §5`,
     `backend/app/models.py:42` — so the user can jump from lesson to
     source. External links only for general concepts (e.g. domain
     terminology, framework docs).
   - Diagrams: reuse the feature's Mermaid sources from `diagrams/*.mmd`
     where they exist (render with the same mermaid-cli pipeline) rather than
     redrawing reality from memory.
   - End every lesson with: 2–4 retrieval-practice questions (same-length
     answer options, no formatting clues), and a reminder they can ask you
     follow-ups in chat.
   - **Sensitive-data rule**: lessons use synthetic examples only — never
     real production data, credentials, or environment secrets, even as
     illustrations. Follow the project's own compliance/data-handling rules.
   - Open the finished lesson for the user (`open <file>`).
4. **Compress into reference docs** anything re-readable: a glossary of the
   feature's domain terms, the architecture cheat sheet, "how our SDLC
   pipeline works" flowchart. Keep one glossary per learning workspace and
   stick to its terms in every lesson.
5. **Record learning**: after teaching, append a learning record
   (`learning-records/000N-<name>.md`: what was learned, misconceptions
   corrected, what to teach next). These drive the next session's starting
   point.

## Common course requests (know these shapes)

- **"What are we building?"** → lessons from gap analysis + PRD refs + Figma
  screenshots: problem, behavior, scope boundaries.
- **"How does the implementation work?"** → tech design + real code walks:
  one lesson per architectural seam (e.g. frontend → backend contract,
  async job pipeline, data model).
- **"What happened while I was away / what did the agents do?"** → manifest
  handoffs + slice logs turned into a narrative lesson with decisions and
  deviations highlighted.
- **"Why is this a compliance issue?"** → the checklist item + the concrete
  code path, taught with a synthetic example of the failure.
- **"How does our SDLC work?"** → cross-cutting course in `docs/learning/`
  from the project's CLAUDE.md + `_shared/handoff-format.md`, with the state
  machine as a diagram.

## Honesty rules

- If artifacts contradict each other (tech design says X, code does Y), teach
  the contradiction explicitly — it's the most valuable lesson available —
  and suggest the user route it to `retro`/`review`, since this skill never
  fixes the pipeline itself.
- If you can't find ground truth for something, say so in the lesson rather
  than smoothing it over with plausible generalities.
