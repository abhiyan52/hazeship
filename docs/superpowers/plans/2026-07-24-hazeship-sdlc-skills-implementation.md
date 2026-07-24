# Hazeship SDLC Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. This plan assumes `skills/productivity/say-hello/`, `.claude-plugin/`, `.codex-plugin/`, `.agents/plugins/marketplace.json`, `README.md`, `LICENSE`, and `tests/test_repository.py` already exist (Phase A, tracked in `docs/superpowers/plans/2026-07-18-hazeship-implementation.md`).

**Goal:** Port the 14 SDLC skills from `~/sensor/.claude/skills/` into `hazeship` as a genericized, portable `skills/sdlc/` kit, dropping all PHI/HIPAA-specific content, with full cross-agent packaging.

**Source:** `~/sensor/.claude/skills/{feature-intake,tech-design,dev-plan,implement-slice,validate-feature,raise-pr,review,retro,team-handoff,teach,to-technical-doc,checkpoint,qa-playwright,seed-data}/SKILL.md` and `~/sensor/.claude/skills/_shared/*.md`.

**Design:** `docs/superpowers/specs/2026-07-23-hazeship-sdlc-skills-design.md`.

## Global Constraints

- Repository path: `/Users/mac/hazeship`.
- New category: `skills/sdlc/`.
- Each skill: `skills/sdlc/<name>/SKILL.md` + `skills/sdlc/<name>/agents/openai.yaml` (same shape as `skills/productivity/say-hello/`).
- Terms `Sensor`, `PHI`, `HIPAA` must not appear anywhere in `skills/sdlc/**` (not even in template placeholder text/comments) — grep must return zero matches.
- `review` is a 2-lane review (correctness/security/quality; design/requirements alignment) — no compliance lane, configurable or otherwise.
- `checkpoint`'s pre-commit gate has no PHI/log-scan step.
- `qa-playwright` reads its test-runner command from `_shared/repo-map.md` instead of a hardcoded path.
- `checkpoint` and `raise-pr` read commit/branch conventions from `_shared/branch-commit-conventions.md`.
- Bump version to `0.2.0` in `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`.
- `.claude-plugin/plugin.json`'s `skills` array lists all 15 skills (say-hello + 14 SDLC skills).
- `README.md`'s "Available skills" section lists all 15.
- Do not publish, push, or globally install anything.

---

### Task 1: Shared templates

**Files:**
- Create: `skills/sdlc/_shared/repo-map.template.md`
- Create: `skills/sdlc/_shared/branch-commit-conventions.md`
- Create: `skills/sdlc/_shared/handoff-format.md`

**Interfaces:**
- Consumes: `~/sensor/.claude/skills/_shared/repo-map.md`, `~/sensor/.claude/skills/_shared/branch-commit-conventions.md`, `~/sensor/.claude/skills/_shared/handoff-format.md` as source material.
- Produces: three generic `_shared/` docs consumed by the Task 2-4 skills.

- [ ] **Step 1:** Read all three source files at `~/sensor/.claude/skills/_shared/`.
- [ ] **Step 2:** Write `repo-map.template.md`: strip every real sensor repo name, path, and command; replace with a placeholder structure (repo name, purpose, key paths, lint/test/QA-runner commands) and inline instructions for a project to fill in its own. Zero sensor-specific content remains.
- [ ] **Step 3:** Write `branch-commit-conventions.md`: keep the shape (branch naming, commit subject format, body sections) but with generic defaults usable out of the box — `feat/*`/`bug/*` branches, `<type>: <imperative>` subject, body with `What we built` / `Why` / `How to test` sections. Drop any sensor-specific attribution/trailer; keep a generic `Co-Authored-By:` line as an example a project can change.
- [ ] **Step 4:** Write `handoff-format.md`: same content as source with sensor references genericized (e.g. project names, made-up example paths).
- [ ] **Step 5:** Grep the three new files for `Sensor`, `PHI`, `HIPAA` — expect zero matches.
- [ ] **Step 6:** Commit: `git add skills/sdlc/_shared && git commit -m "feat: add generic SDLC shared templates"`.

---

### Task 2: Port pipeline-stage skills (6)

**Files:**
- Create: `skills/sdlc/feature-intake/SKILL.md`, `skills/sdlc/feature-intake/agents/openai.yaml`
- Create: `skills/sdlc/tech-design/SKILL.md`, `skills/sdlc/tech-design/agents/openai.yaml`
- Create: `skills/sdlc/dev-plan/SKILL.md`, `skills/sdlc/dev-plan/agents/openai.yaml`
- Create: `skills/sdlc/implement-slice/SKILL.md`, `skills/sdlc/implement-slice/agents/openai.yaml`
- Create: `skills/sdlc/validate-feature/SKILL.md`, `skills/sdlc/validate-feature/agents/openai.yaml`
- Create: `skills/sdlc/raise-pr/SKILL.md`, `skills/sdlc/raise-pr/agents/openai.yaml`

**Interfaces:**
- Consumes: `~/sensor/.claude/skills/{feature-intake,tech-design,dev-plan,implement-slice,validate-feature,raise-pr}/SKILL.md`, and `skills/sdlc/_shared/*` from Task 1.
- Produces: 6 genericized SDLC-stage skills forming the main pipeline (intake → tech design → dev plan → implement → validate → raise PR).

- [ ] **Step 1:** For each of the 6 skills, read the sensor source `SKILL.md`.
- [ ] **Step 2:** Write the genericized `SKILL.md` to `skills/sdlc/<name>/SKILL.md`: keep the workflow/logic unchanged, strip literal sensor project/repo names, and repoint any `_shared/` reference at the Task 1 files (e.g. `_shared/repo-map.md` → `_shared/repo-map.template.md` where the skill is reading project-specific info, or leave as `_shared/repo-map.md` if the skill's instruction is "read the project's own repo-map, using the template as a starting point" — pick the phrasing that matches how the skill is actually used and be consistent across all 6). `raise-pr` must reference `_shared/branch-commit-conventions.md` for its PR/commit format instead of "the workspace's format".
- [ ] **Step 3:** Write `skills/sdlc/<name>/agents/openai.yaml` for each, following the `say-hello` shape: `interface.display_name`, `interface.short_description`, `interface.default_prompt`, `policy.allow_implicit_invocation: false`.
- [ ] **Step 4:** Grep all 6 new `SKILL.md` files for `Sensor`, `PHI`, `HIPAA` — expect zero matches.
- [ ] **Step 5:** Commit: `git add skills/sdlc/{feature-intake,tech-design,dev-plan,implement-slice,validate-feature,raise-pr} && git commit -m "feat: port SDLC pipeline-stage skills"`.

---

### Task 3: Port helper skills (5)

**Files:**
- Create: `skills/sdlc/retro/SKILL.md`, `skills/sdlc/retro/agents/openai.yaml`
- Create: `skills/sdlc/team-handoff/SKILL.md`, `skills/sdlc/team-handoff/agents/openai.yaml`
- Create: `skills/sdlc/teach/SKILL.md`, `skills/sdlc/teach/agents/openai.yaml`
- Create: `skills/sdlc/to-technical-doc/SKILL.md`, `skills/sdlc/to-technical-doc/agents/openai.yaml`
- Create: `skills/sdlc/seed-data/SKILL.md`, `skills/sdlc/seed-data/agents/openai.yaml`

**Interfaces:**
- Consumes: `~/sensor/.claude/skills/{retro,team-handoff,teach,to-technical-doc,seed-data}/SKILL.md`, and `skills/sdlc/_shared/*` from Task 1.
- Produces: 5 genericized helper skills usable at any point in the pipeline.

- [ ] **Step 1:** For each of the 5 skills, read the sensor source `SKILL.md`.
- [ ] **Step 2:** Write the genericized `SKILL.md` to `skills/sdlc/<name>/SKILL.md`: same treatment as Task 2 — logic unchanged, sensor specifics stripped, `_shared/` references repointed at Task 1's files. `team-handoff` references `_shared/handoff-format.md`.
- [ ] **Step 3:** Write `skills/sdlc/<name>/agents/openai.yaml` for each, same shape as Task 2.
- [ ] **Step 4:** Grep all 5 new `SKILL.md` files for `Sensor`, `PHI`, `HIPAA` — expect zero matches.
- [ ] **Step 5:** Commit: `git add skills/sdlc/{retro,team-handoff,teach,to-technical-doc,seed-data} && git commit -m "feat: port SDLC helper skills"`.

---

### Task 4: Port skills requiring genericization (review, checkpoint, qa-playwright)

**Files:**
- Create: `skills/sdlc/review/SKILL.md`, `skills/sdlc/review/agents/openai.yaml`
- Create: `skills/sdlc/checkpoint/SKILL.md`, `skills/sdlc/checkpoint/agents/openai.yaml`
- Create: `skills/sdlc/qa-playwright/SKILL.md`, `skills/sdlc/qa-playwright/agents/openai.yaml`

**Interfaces:**
- Consumes: `~/sensor/.claude/skills/{review,checkpoint,qa-playwright}/SKILL.md`, and `skills/sdlc/_shared/*` from Task 1.
- Produces: 3 skills with the design's specific behavioral changes applied (not just a mechanical port).

- [ ] **Step 1:** Read the sensor source `SKILL.md` for `review`, `checkpoint`, `qa-playwright`.
- [ ] **Step 2 (review):** Write `skills/sdlc/review/SKILL.md` as a **2-lane** review: (1) correctness, security & code quality — bugs, injection/trust-boundary safety, efficiency, structural quality; (2) design & requirements alignment. Remove the PHI/HIPAA compliance lane entirely — do not replace it with a configurable/optional compliance lane of any kind.
- [ ] **Step 3 (checkpoint):** Write `skills/sdlc/checkpoint/SKILL.md`: same steps as the source (repo identification, branch check, diff review, pre-commit gate, commit message composition per `_shared/branch-commit-conventions.md`) but drop the "No PHI in the diff's log statements" scan step from the pre-commit gate. Reference `_shared/branch-commit-conventions.md` for the message format instead of "the workspace's required format".
- [ ] **Step 4 (qa-playwright):** Write `skills/sdlc/qa-playwright/SKILL.md`: same Playwright-authoring/running logic, but the test-runner command comes from `_shared/repo-map.md` (a project fills this in from the template); if no runner command is recorded there, the skill asks the user once and suggests recording it. Remove the hardcoded `tools/qa` path.
- [ ] **Step 5:** Write `skills/sdlc/{review,checkpoint,qa-playwright}/agents/openai.yaml`, same shape as Task 2.
- [ ] **Step 6:** Grep all 3 new `SKILL.md` files for `Sensor`, `PHI`, `HIPAA` — expect zero matches.
- [ ] **Step 7:** Commit: `git add skills/sdlc/{review,checkpoint,qa-playwright} && git commit -m "feat: port and genericize review, checkpoint, qa-playwright skills"`.

---

### Task 5: Manifests, README, version bump

**Files:**
- Modify: `.claude-plugin/plugin.json`
- Modify: `.codex-plugin/plugin.json`
- Modify: `README.md`

**Interfaces:**
- Consumes: all 14 skills from Tasks 1-4 plus the existing `say-hello` skill.
- Produces: updated packaging metadata and documentation reflecting the full 15-skill set at version `0.2.0`.

- [ ] **Step 1:** In `.claude-plugin/plugin.json`, bump `"version"` to `"0.2.0"` and set `"skills"` to `["./skills/productivity/say-hello", "./skills/sdlc/feature-intake", "./skills/sdlc/tech-design", "./skills/sdlc/dev-plan", "./skills/sdlc/implement-slice", "./skills/sdlc/validate-feature", "./skills/sdlc/raise-pr", "./skills/sdlc/review", "./skills/sdlc/retro", "./skills/sdlc/team-handoff", "./skills/sdlc/teach", "./skills/sdlc/to-technical-doc", "./skills/sdlc/checkpoint", "./skills/sdlc/qa-playwright", "./skills/sdlc/seed-data"]`.
- [ ] **Step 2:** In `.codex-plugin/plugin.json`, bump `"version"` to `"0.2.0"` (its `"skills": "./skills/"` pointer already covers the new tree — no other change needed there).
- [ ] **Step 3:** In `README.md`, expand "Available skills" to list all 15 skills with a one-line description each, grouped as "Productivity" (say-hello) and "SDLC" (the 14 ported skills, in pipeline order followed by helpers).
- [ ] **Step 4:** Validate JSON: `python3 -m json.tool .claude-plugin/plugin.json` and `python3 -m json.tool .codex-plugin/plugin.json`.
- [ ] **Step 5:** Commit: `git add .claude-plugin/plugin.json .codex-plugin/plugin.json README.md && git commit -m "feat: package SDLC skills and bump to 0.2.0"`.

---

### Task 6: Test suite extension and full validation

**Files:**
- Modify: `tests/test_repository.py`

**Interfaces:**
- Consumes: the complete `skills/sdlc/` tree and updated manifests from Tasks 1-5.
- Produces: an extended, passing `tests/test_repository.py`.

- [ ] **Step 1:** Add a test that for each of the 14 SDLC skill names, asserts `skills/sdlc/<name>/SKILL.md` exists, contains `name: <name>` and a non-empty `description:` frontmatter field, and `skills/sdlc/<name>/agents/openai.yaml` exists.
- [ ] **Step 2:** Add a guard test that walks `skills/sdlc/**/*.md` and `skills/sdlc/**/*.yaml` and asserts none of the literal strings `Sensor`, `PHI`, `HIPAA` appear anywhere.
- [ ] **Step 3:** Update `test_claude_plugin` and any other version-`0.1.0` assertions to expect `0.2.0` and the full 15-entry `skills` array.
- [ ] **Step 4:** Run `python3 -m unittest discover -s tests -v` — expect all tests pass.
- [ ] **Step 5:** Run `python3 /Users/mac/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/sdlc/<name>` for each of the 14 skills — expect success for all.
- [ ] **Step 6:** Run `python3 /Users/mac/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .` — expect success.
- [ ] **Step 7:** Commit: `git add tests/test_repository.py && git commit -m "test: extend repository tests for SDLC skills"`.
