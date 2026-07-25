---
name: team-handoff
description: |
  Create or close a question handoff to the human team (PM, design, eng,
  QA). Use when an open gap, doubt, or contradiction in the PRD, Figma,
  tech design, development, or testing needs a human answer — "raise a team
  handoff", "I need to ask the PM/design about X". Close with
  "/team-handoff close" plus the handoff id. List with "/team-handoff list".
---

# Team Handoff (questions to humans)

## Usage

```
/team-handoff <project> <what's unclear>
/team-handoff close <id>
/team-handoff list
```

Read `_shared/handoff-format.md` first — this skill produces a different
kind of handoff than the agent-to-agent one described there: unlike a
context transfer to a fresh agent, a team handoff is a durable, tracked
question to HUMANS, stored in the meta repo at:

```
docs/team-handoff/<project>/<NNN>-<topic-slug>.md
```

`<project>` is the feature slug (or `workspace` for non-feature gaps);
`<NNN>` increments per project; the handoff id is `<project>#<NNN>`.
Use the template at `docs/templates/team-handoff.md`.

## Mode: create (default)

1. **Pin the gap down before writing.** Re-read the relevant sources (PRD
   section, authoritative Figma link from the manifest — never PRD-embedded
   links, tech design, code, test evidence) so the question is grounded in
   evidence, not vibes. If you can answer it yourself from the artifacts,
   say so instead of creating a handoff.
2. Determine: audience (PM / Design / Eng / QA), what SDLC
   stage it blocks (or "non-blocking"), and options if the answer is a
   choice — a question with concrete options gets answered 10x faster.
3. Write the doc from the template. The two load-bearing rules:
   - **§ Detailed explanation** is for the USER's own understanding: what
     the gap is, why it matters, what was already checked and ruled out,
     hypotheses, and consequences of each plausible answer. Local file
     paths, code refs, internal reasoning all belong HERE.
   - **§ Paste-ready comment** must survive being pasted into
     Discord/Slack/a Google Doc comment on its own: self-contained, ≤120
     words, numbered questions, options inline, shareable URLs only (Figma/
     PRD links) — NEVER local paths (`/Users/...`, `docs/...`), internal
     ids, or sensitive data. Keep it inside a fenced block so it's one clean
     copy. References stay in their own section — do not bloat the comment.
4. If the handoff belongs to a feature: add it to the manifest's latest
   handoff `open_questions` as `team-handoff <project>#<NNN>: <one-liner>`,
   so the pipeline's gate summaries surface it.
5. Show the user: the id, the paste-ready comment (verbatim, ready to
   copy), and where the doc lives. Suggest `/checkpoint` to commit it.

## Mode: close (`/team-handoff close <project>#<NNN>` or close <id> words)

Fill § Resolution (the answer, who answered, where — link the thread if
one exists, date), then walk the close checklist IN the doc, checking each
item off for real:

- [ ] Resolution recorded verbatim (quote the decision, name the decider)
- [ ] Affected artifacts updated (gap analysis / tech design / dev plan /
      slice log — whichever the answer changes; regenerate the technical
      doc via /to-technical-doc if one was published)
- [ ] Manifest `open_questions` entry removed; decision recorded in the
      manifest handoff `decisions` if it changed scope/approach
- [ ] Architectural implications → ADR in `docs/adr/` (link it)
- [ ] Follow-up work routed (new slice task / bug branch / backlog) — not
      silently absorbed
- [ ] Header `status: open` → `closed`, `closed: <date>` added

Only when every applicable box is checked, report closure and suggest
`/checkpoint`. If a box can't be checked yet, the handoff STAYS open —
say what's missing.

## Mode: list

`grep -r "^status: open" docs/team-handoff/` and present: id, title,
audience, blocking, age. Nag gently about stale blockers (>3 days old).

## Rules

- One question-cluster per handoff — unrelated doubts get separate docs
  (they close at different times).
- These docs are committed to the meta repo: no sensitive data, no
  credentials, no real production examples — synthetic illustrations only,
  per the data handling rules in `_shared/repo-map.md`.
- A blocking handoff does not stop the pipeline mechanically, but the
  blocked stage's skill should surface it (it's in `open_questions`) and
  the user decides whether to proceed at risk.
