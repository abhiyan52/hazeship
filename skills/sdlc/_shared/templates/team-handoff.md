---
id: <project>#<NNN>
title: <one-line question topic>
audience: PM | Design | Eng | QA
status: open
blocks: <slice NN / stage name / non-blocking>
raised: <YYYY-MM-DD>
closed:
sources:
  - <PRD §n / Figma node / file path / test evidence you actually read>
---

# <project>#<NNN> — <title>

## Detailed explanation (for us, not for them)

This section is for the reader who has to act on the answer. Local paths,
code references and internal reasoning all belong **here** — never in the
paste-ready comment below.

**What the gap is**

<The contradiction or ambiguity, stated precisely.>

**Why it matters**

<What breaks or stalls if it stays unanswered.>

**Already checked and ruled out**

- <what you read, and what it did or didn't say>

**Hypotheses and consequences**

| If the answer is | Then | Cost |
|---|---|---|
| <option a> | <what we build> | <effort / rework> |
| <option b> | <what we build> | <effort / rework> |

## Paste-ready comment

Must survive being pasted into Slack, Discord or a doc comment on its own:
self-contained, ≤120 words, numbered questions, options inline, shareable
URLs only. **Never** local paths (`/Users/…`, `docs/…`), internal ids, or
sensitive data.

```
<Context in one sentence.>

1. <Question?> Options: (a) <…> (b) <…>
2. <Question?>

<What it blocks, and by when you need it.>
```

## References

<Links and paths for us — kept out of the comment above so it stays clean.>

- <path or URL>

## Resolution

- **Answer**: <quote the decision verbatim>
- **Decided by**: <name/role>
- **Where**: <link to the thread, or "verbally on <date>">
- **Date**: <YYYY-MM-DD>

### Close checklist

The handoff stays **open** until every applicable box is genuinely checked.

- [ ] Resolution recorded verbatim (decision quoted, decider named)
- [ ] Affected artifacts updated (gap analysis / tech design / dev plan /
      slice log — whichever the answer changes; regenerate the technical doc
      via `/to-technical-doc` if one was published)
- [ ] Manifest `open_questions` entry removed; decision recorded in the
      manifest handoff `decisions` if it changed scope or approach
- [ ] Architectural implications → ADR in `docs/adr/` (linked)
- [ ] Follow-up work routed (new slice task / bug branch / backlog) — not
      silently absorbed
- [ ] Header `status: open` → `closed`, `closed: <date>` filled in
