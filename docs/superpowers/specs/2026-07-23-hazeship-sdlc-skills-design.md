# Hazeship SDLC Skills Design

## Goal

Bring the 14 custom SDLC skills currently living in `~/sensor/.claude/skills/`
into the `hazeship` skills repository as a portable, project-agnostic "SDLC
kit" — genericized so any project can adopt the pipeline, not just sensor.

This builds on top of the existing `say-hello` foundation design
(`2026-07-18-hazeship-design.md`), which has not yet been implemented.

## Scope

### Phase A — Foundation (v0.1.0)

Execute the existing approved plan
(`docs/superpowers/plans/2026-07-18-hazeship-implementation.md`) as-is:
`skills/productivity/say-hello/`, `.claude-plugin/`, `.codex-plugin/`,
`.agents/plugins/marketplace.json`, `README.md`, `LICENSE`,
`tests/test_repository.py`. No changes to that design.

### Phase B — SDLC kit (v0.2.0)

Add `skills/sdlc/` with 14 skills ported from `~/sensor/.claude/skills/`:

- Pipeline stages: `feature-intake`, `tech-design`, `dev-plan`,
  `implement-slice`, `validate-feature`, `raise-pr`
- Helper skills: `review`, `retro`, `team-handoff`, `teach`,
  `to-technical-doc`, `checkpoint`, `qa-playwright`, `seed-data`

Excluded from this port: the 8 skills in `~/sensor/.claude/skills/` that are
already tracked in `~/sensor/skills-lock.json` as sourced from
`mattpocock/skills` on GitHub (`codebase-design`, `diagnosing-bugs`,
`grill-me`, `grill-with-docs`, `grilling`, `handoff`,
`improve-codebase-architecture`, `writing-great-skills`) — those are not new
and are not owned by this port.

## Genericizing sensor-specific content

Split the 14 skills into two buckets:

**Already generic (11)** — `feature-intake`, `tech-design`, `dev-plan`,
`implement-slice`, `validate-feature`, `retro`, `team-handoff`, `teach`,
`to-technical-doc`, `seed-data`, `checkpoint`. These describe a workflow, not
sensor specifics. Light edit pass only: strip any literal sensor
project/repo names, keep the SDLC logic unchanged.

**Need genericizing (3)**:

- **`review`** — the 3-lane review currently hardcodes a "PHI/HIPAA
  compliance" lane. Becomes a **configurable compliance lane**: off by
  default; a project enables it by supplying its own checklist at
  `_shared/compliance-checklist.md`. The skill checks for that file's
  existence before running the compliance lane.
- **`checkpoint` / `raise-pr`** — currently reference "the workspace's
  required format" for commit messages and branch naming. Becomes: read
  conventions from `_shared/branch-commit-conventions.md`, shipped with
  generic working defaults (branches `feat/*`/`bug/*`; commit subject
  `<type>: <imperative>`; body with `What we built` / `Why` / `How to test`
  sections). Projects override the file to change conventions; the skill
  logic itself doesn't change.
- **`qa-playwright`** — currently hardcodes a `tools/qa` runner path.
  Becomes: skill reads the test-runner command from `_shared/repo-map.md`
  instead of a hardcoded path; if absent, it asks the user for the command
  once and suggests recording it there.

## `_shared/` templates

`skills/sdlc/_shared/` ships four files:

- `repo-map.template.md` — placeholder structure (repo names, key paths,
  lint/test commands) with instructions for a project to fill in its own.
  Sensor's actual repo-map becomes the worked example referenced from
  comments, not shipped content.
- `compliance-checklist.template.md` — placeholder structure for an optional
  domain compliance lane (sensor's PHI/HIPAA checklist serves as the
  inspiration/example in a comment, not shipped verbatim).
- `branch-commit-conventions.md` — ships with generic, usable-out-of-the-box
  defaults (not a template — works as-is, overridable).
- `handoff-format.md` — already generic; ships as-is with minor sensor
  references stripped.

Any skill referencing `_shared/` docs points at these four files.

## Packaging

Same cross-agent pattern as `say-hello`: each of the 14 skills gets
`SKILL.md` + `agents/openai.yaml` under `skills/sdlc/<name>/`.
`.claude-plugin/plugin.json`'s `skills` array and the Codex/README
references are updated to include the full set. Repo version bumps from
`0.1.0` to `0.2.0` in `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`.
`README.md`'s "Available skills" section lists all 15 skills (say-hello +
14 SDLC skills).

## Testing

Extend `tests/test_repository.py`:

- One assertion per new skill: `SKILL.md` exists with `name:` and
  `description:` frontmatter, and `agents/openai.yaml` exists.
- A guard test that greps `_shared/*.template.md` and all 14 `SKILL.md`
  files for leaked sensor specifics (`Sensor`, `PHI`, `HIPAA` outside the
  templates' own placeholder/example comments) and fails if found outside
  the allowed template comment blocks.
- Version assertions updated to `0.2.0` where the foundation tests currently
  assert `0.1.0`.

## Non-goals

- Publishing or pushing the GitHub repository
- Installing the skill(s) globally on this machine
- Porting the 8 `mattpocock/skills`-sourced skills
- Adding new SDLC stages/skills beyond the 14 being ported
- Building a config-loading mechanism beyond "skill reads a `_shared/*.md`
  file if present" (no schema validation, no CLI)
