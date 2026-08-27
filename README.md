# Hazeship

Reusable skills for Claude Code, Codex, and agents that support the Agent Skills format.

The SDLC kit is an end-to-end feature loop — intake → design → plan →
implement → validate → PR → retro — with a human approval gate at every
stage. It is stack-agnostic: what it needs to know about your project (repos,
commands, data-handling rules) it reads from one file you fill in.

## Available skills

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
- `explain-me` — Generate short lessons explaining what's being built, grounded in the feature's actual artifacts and code (wraps a generic `teach` skill for lesson mechanics, if installed).
- `to-technical-doc` — Produce the shareable Technical Design document (+ DOCX) for stakeholders.
- `checkpoint` — Create a commit in the project's required format, validating branch naming first.
- `commit-pr` — One-shot commit + push + PR: runs `checkpoint`, pushes, then `raise-pr`.
- `qa-playwright` — Automated browser verification of a slice or feature via the project's Playwright QA runner.
- `seed-data` — Generate synthetic seed scripts/data for a feature and populate the local dev database.
- `persistent-memory` — Store and retrieve durable project context for other skills in a resolved memory store.
- `ssh-readonly-investigation` — Investigate a remote host over SSH strictly read-only, with connection facts from `repo-map.md`.
- `triage` — Turn a support ticket into an evidence-backed diagnosis (data/config, code bug, not-a-bug, or needs-info) without changing any system.
- `bugfix` — Lightweight bug loop: failing test first, minimal fix, Playwright on the affected flow, ship via `commit-pr` on a `bug/*` branch.
- `address-pr-comments` — Fetch unresolved review threads, fix the clear-cut ones behind a per-batch test gate, and reply with commit + test evidence.
- `work-log` — System of record for all work: dedup gate before starting anything, then status/actor/source (clickup, telegram, direct) and PR + ClickUp links per item, via `tools/worklog`.

### Diagnostics

- `diagnosing-bugs` — Diagnosis loop for hard bugs and performance regressions.

### Architecture

- `codebase-design` — Shared vocabulary for designing deep modules and finding deepening opportunities.
- `domain-modeling` — Build and sharpen a project's domain model and ubiquitous language.
- `improve-codebase-architecture` — Scan a codebase for deepening opportunities and present them as a visual report.

### Interview

- `grill-me` — A relentless interview to sharpen a plan or design.
- `grill-with-docs` — Grilling that also keeps the domain glossary and ADRs current as it goes.
- `grilling` — Base grilling trigger skill; use when the user wants their thinking stress-tested.
- `wait-what` — Re-pitch the last message in plain, ASD-STE100 Simplified Technical English.

### Implementation

- `handoff` — Compact the current conversation into a handoff document for another agent to pick up.
- `implement` — Implement one piece of work from a spec/ticket, test-first at the agreed seams.
- `subagent-driven-development` — Execute an implementation plan by dispatching a fresh implementer subagent per task.
- `tdd` — Test-driven development: red-green-refactor, integration tests.

### Synthesis

- `meeting-thread` — Pull one thread out of an AI-generated meeting note and write it up as its own doc.
- `research` — Investigate a question against high-trust primary sources and capture the findings as a doc.
- `to-spec` — Synthesize the current conversation into a spec, with no interview.
- `to-tickets` — Break a plan/spec into tracer-bullet tickets with blocking edges, published to the configured tracker.

### Ops

- `deploy` — Deploy workflow for the project's environments.
- `deployment-monitor` — Monitor a deployment and surface issues as they appear.

### Authoring

- `setup-matt-pocock-skills` — One-time bootstrap for the engineering-skills issue tracker, triage labels, and domain doc layout.
- `writing-for-agents` — Writing documents for agents to read (specs, plans, ADRs).
- `writing-great-skills` — Reference for writing and editing skills well.

### Diagramming

- `archify` — Create polished, validated architecture/workflow/sequence/dataflow/lifecycle diagrams as explorable HTML with light/dark themes and PNG/JPEG/WebP/SVG/WebM export.

### Communication

- `humanizer` — Rewrite AI-sounding text so it reads naturally, without changing what it says. Vendored from [blader/humanizer](https://github.com/blader/humanizer) (MIT).
- `instant-message-reply` — Draft a short, natural-sounding reply to a chat message, grounded in the surrounding thread. Combines `wait-what`'s directness with `humanizer`'s AI-pattern check.

### Productivity

- `say-hello` — Return a deterministic greeting in Nepali.

## What ships alongside the skills

The SDLC skills read and write real files, so the kit ships the pieces they
depend on under `skills/sdlc/_shared/`:

- `tools/sdlc` — the feature state machine. Owns every state field in a
  feature's `manifest.yaml` and refuses illegal transitions, so approvals
  can't be skipped and untested slices can't stack. Python 3 + PyYAML.
- `tools/build-docx.sh` — markdown → DOCX for the stakeholder document.
- `templates/` — the nine document templates the skills write from.
- `repo-map.template.md` — the one file you fill in per project: repos,
  commands, ports, QA credentials, and your data-handling rules.
- `workspace-setup.md` — the one-time, idempotent bootstrap that copies the
  above into a project.
- `handoff-format.md`, `branch-commit-conventions.md` — the contracts every
  skill and subagent communicates through.

## Using the SDLC kit in a project

Once installed, run any SDLC skill from your project's workspace root. On the
first run it will bootstrap `tools/`, `docs/templates/` and
`_shared/repo-map.md` per `workspace-setup.md` — then **fill in
`_shared/repo-map.md`** before going further; every skill reads it instead of
guessing at your repos.

```bash
python3 -m pip install pyyaml   # tools/sdlc reads manifests with it
```

Per-project facts live in the **project's** `_shared/repo-map.md`, not inside
the kit — the installed kit is shared across projects. If you vendor the kit
into a single repo instead, keep the map next to the template.

`persistent-memory` additionally needs a store root. It resolves one in this
order: `$HAZESHIP_MEMORY_DIR`, then the nearest `.hazeship/` marker directory
found walking up from the current directory (honouring `HAZESHIP_MEMORY_DIR` in
its `config.env`), and otherwise proposes `<repo root>/.hazeship/memory`. To
create the default store explicitly:

```bash
skills/sdlc/persistent-memory/scripts/resolve-memory-root.sh --init --why
```

The feature loop, and who moves it:

| Stage | Skill | Gate |
|---|---|---|
| intake | `/feature-intake` | user approves the gap analysis |
| tech-design | `/tech-design` | user approves the design |
| dev-plan | `/dev-plan` | user approves the slicing |
| implement | `/implement-slice` | user tests each slice |
| validate | `/validate-feature` | user approves the verdict |
| final-pr | `/raise-pr` → `/review` | user merges |
| retro | `/retro` | user signs off |

`/checkpoint`, `/commit-pr`, `/qa-playwright`, `/seed-data`, `/explain-me`,
`/team-handoff`, `/to-technical-doc`, `/persistent-memory` and
`/ssh-readonly-investigation` are helpers, usable at any point.

Not everything is a feature. Three standalone workflows cover the rest of
the daily work, reusing the same helpers and gates:

| Work | Skill | Chain |
|---|---|---|
| Support ticket | `/triage` | `persistent-memory` → `ssh-readonly-investigation` → verdict (may hand off to `/bugfix`) |
| Bug | `/bugfix` | failing test → minimal fix → `qa-playwright` → user verifies → `commit-pr` |
| Review feedback | `/address-pr-comments` | fetch threads → classify → fix + test gate per batch → `checkpoint` → reply with evidence |

Every workflow above starts with the `work-log` dedup gate (don't redo work
already picked up) and records its item — status, actor, source, PR and
ClickUp links — in the project's `worklog/` ledger via `tools/worklog`.

## Keeping installed projects up to date

`bin/hazeship-sync` propagates the kit into every registered project — the
project-level `.claude/skills/` copies, per-subrepo symlinks (kept out of
git via each repo's local `.git/info/exclude`), and any new document
templates. Skills a project added itself are never touched; skills removed
from the kit are pruned from the projects.

```bash
bin/hazeship-sync add <project-root>   # register once (also syncs)
bin/hazeship-sync                      # after any change to the kit
bin/hazeship-sync list                 # what's registered
```

Put it on your PATH so it works from anywhere:

```bash
ln -sfn "$(pwd)/bin/hazeship-sync" ~/.local/bin/hazeship-sync
```

## Generic Agent Skills installation

```bash
npx skills@latest add abhiyan52/hazeship
```

## Claude Code installation

```bash
claude plugin marketplace add abhiyan52/hazeship
claude plugin install hazeship@abhiyan52
```

Invoke a skill with `/<name>` — e.g. `/feature-intake`, `/review`, `/checkpoint`.

## Codex installation

```bash
codex plugin marketplace add abhiyan52/hazeship
codex plugin add hazeship@hazeship
```

Invoke a skill with `$<name>` — e.g. `$feature-intake`, `$review`, `$checkpoint`.

## Local validation

```bash
python3 -m unittest discover -s tests -v
```

## License

MIT
