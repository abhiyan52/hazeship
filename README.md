# Hazeship

Reusable skills for Claude Code, Codex, and agents that support the Agent Skills format.

## Available skills

### Productivity

- `say-hello` — Return a deterministic greeting in Nepali.

### SDLC

- `feature-intake` — Stage 1: scaffold the feature folder and produce a gap analysis (PRD vs design vs codebase).
- `tech-design` — Stage 2: turn a resolved gap analysis into a Tech Design Document (markdown + Mermaid diagrams).
- `dev-plan` — Stage 3: turn the tech design into a phased development plan of vertical slices.
- `implement-slice` — Stage 4: implement one vertical slice from the dev plan and keep the slice log.
- `validate-feature` — End-of-feature validation of every PRD acceptance criterion and gap-analysis resolution before the final PR.
- `raise-pr` — Raise PRs via `gh` following branch/commit/PR conventions and record merges in the manifest.
- `review` — Two-lane PR review: correctness/security/quality, and design/requirements conformance.
- `retro` — Post-merge retrospective that processes feedback, drives fixes, and captures SDLC lessons.
- `team-handoff` — Create or close a question handoff to the human team (PM, design, eng, QA).
- `teach` — Generate short lessons explaining what's being built, grounded in the feature's actual artifacts and code.
- `to-technical-doc` — Produce the shareable Technical Design document (+ DOCX) for stakeholders.
- `checkpoint` — Create a commit in the project's required format, validating branch naming first.
- `commit-pr` — One-shot commit + push + PR: runs `checkpoint`, pushes, then `raise-pr`.
- `qa-playwright` — Automated browser verification of a slice or feature via the project's Playwright QA runner.
- `seed-data` — Generate synthetic seed scripts/data for a feature and populate the local dev database.
- `persistent-memory` — Store and retrieve durable project context for other skills in a resolved memory store.
- `ssh-readonly-investigation` — Investigate a remote host over SSH strictly read-only, with connection facts from `repo-map.md`.

## Per-project setup

The SDLC skills read project-specific facts from `skills/sdlc/_shared/repo-map.md`.
Copy `skills/sdlc/_shared/repo-map.template.md` to that path and fill it in once
per project.

`persistent-memory` additionally needs a store root. It resolves one in this
order: `$HAZESHIP_MEMORY_DIR`, then the nearest `.hazeship/` marker directory
found walking up from the current directory (honouring `HAZESHIP_MEMORY_DIR` in
its `config.env`), and otherwise proposes `<repo root>/.hazeship/memory`. To
create the default store explicitly:

```bash
skills/sdlc/persistent-memory/scripts/resolve-memory-root.sh --init --why
```

## Generic Agent Skills installation

```bash
npx skills@latest add abhiyanhaze/hazeship
```

## Claude Code installation

```bash
claude plugin marketplace add abhiyanhaze/hazeship
claude plugin install hazeship@abhiyanhaze
```

Invoke the skill with `/say-hello`.

## Codex installation

```bash
codex plugin marketplace add abhiyanhaze/hazeship
codex plugin add hazeship@hazeship
```

Invoke the skill with `$say-hello`.

## Local validation

```bash
python3 -m unittest discover -s tests -v
python3 /Users/mac/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/productivity/say-hello
```

## License

MIT
