---
name: retro
description: |
  Post-merge retrospective. Processes feedback (QA/PM/production), drives the
  fixes, brings documentation back in line with reality, and captures lessons
  that improve the SDLC loop itself. Use when asked to "do a retro", "handle
  this feedback", or after post-merge feedback arrives.
---

# Retrospective

You produce/extend `docs/features/<slug>/05-retro.md` from
`docs/templates/retro.md`. A retro can run multiple times per feature (each
feedback batch appends).

**Pre-merge variant.** The default framing is post-merge, but this skill also
handles a **still-open final PR** whose review produced findings to drive
(the review skill owns the review itself; retro owns driving the fixes +
docs + lessons). In that case: process the batch and capture lessons now, but
SKIP the manifest transitions in step 5 — the `retro`/`done` transitions
require the merged final PR (confirmed via `gh pr view`). Append the handoff
entry noting the batch ran pre-merge, and land fixes as follow-up commits on
the feature branch (not a new bug branch) so they merge with the PR.

## Steps

1. **Collect feedback** from the user (paste, issue links, QA notes) and
   classify each item: bug / design gap / doc gap / works-as-intended.
   Reproduce bugs before classifying them (or note "could not reproduce").
2. **Drive actions**:
   - Bugs → `bug/<desc>` branch off the staging branch, fixed via the normal
     checkpoint → raise-pr → review path (small loop, same rigor).
   - Design gaps → either a new slice on the feature (if pre-GA) or a new
     mini-feature intake (if scope actually changed). Don't silently absorb
     scope changes.
   - Doc gaps → fix now, in this skill.
3. **Make the docs truthful**: update the tech design to as-built (diagrams
   too; if a `technical-doc.md` exists, regenerate it via
   `/to-technical-doc`), annotate the dev plan, correct the project's
   `_shared/repo-map.md` where commands/URLs proved wrong.
4. **Capture loop lessons**: for every feedback item, ask "which pipeline
   stage should have caught this?" and record the concrete edit to that
   skill/template/checklist in the lessons table. Propose the edits to the
   user; apply approved ones immediately — this is how the loop improves.
   Architectural lessons become ADRs in `docs/adr/`.
5. Manifest bookkeeping: on first run after the final PR merges (verify via
   `gh pr view` — raise-pr owns merge recording for slices, retro owns the
   feature-level transition), run `tools/sdlc transition <slug> retro`
   (requires the final-pr stage gate approved). Append the retro handoff
   entry. When the feedback batch is fully processed:
   `tools/sdlc gate <slug> awaiting-approval`, and after the user's sign-off
   (`tools/sdlc approve <slug>`),
   `tools/sdlc transition <slug> done`.
