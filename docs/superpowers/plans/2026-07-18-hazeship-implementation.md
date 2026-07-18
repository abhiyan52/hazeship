# Hazeship Cross-Agent Skill Repository Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `~/hazeship` as an installable skills repository whose first skill returns one deterministic Nepali greeting across generic agents, Claude Code, and Codex.

**Architecture:** Keep `skills/productivity/say-hello/` as the single canonical implementation. Thin Claude and Codex manifests point to that tree, while repository tests verify the exact greeting contract, metadata, references, and documented installation commands.

**Tech Stack:** Agent Skills `SKILL.md`, YAML UI metadata, JSON plugin manifests, Python `unittest`, Git, `npx skills`.

## Global Constraints

- Repository path: `/Users/mac/hazeship`.
- Canonical skill name: `say-hello`.
- Exact output: `नमस्ते! तपाईंलाई हार्दिक अभिवादन।`
- Initial plugin version: `0.1.0`.
- Author and marketplace owner: `abhiyanhaze`.
- Repository URL: `https://github.com/abhiyanhaze/hazeship`.
- License: MIT.
- Category: Productivity.
- Maintain one skill implementation; manifests must not duplicate its instructions.
- Do not publish, push, globally install, or add connectors, MCP servers, hooks, scripts, or graphical assets.

---

### Task 1: Establish the greeting contract and canonical skill

**Files:**
- Create: `tests/test_repository.py`
- Create: `skills/productivity/say-hello/SKILL.md`
- Create: `skills/productivity/say-hello/agents/openai.yaml`

**Interfaces:**
- Consumes: Explicit `/say-hello` or `$say-hello` invocation.
- Produces: Exactly one line, `नमस्ते! तपाईंलाई हार्दिक अभिवादन।`.

- [ ] **Step 1: Run the baseline without the skill**

Dispatch a fresh agent without providing the future skill:

```text
/say-hello
```

Record the raw response. The baseline fails unless it is exactly
`नमस्ते! तपाईंलाई हार्दिक अभिवादन।` with no additional text.

- [ ] **Step 2: Write the failing repository test**

Create `tests/test_repository.py`:

```python
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "productivity" / "say-hello"
GREETING = "नमस्ते! तपाईंलाई हार्दिक अभिवादन।"


class HazeshipRepositoryTests(unittest.TestCase):
    def test_skill_contract(self):
        content = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: say-hello", content)
        self.assertIn(
            "description: Use when the user explicitly invokes /say-hello or "
            "$say-hello, or asks for the Hazeship sample Nepali greeting.",
            content,
        )
        self.assertIn(GREETING, content)
        self.assertIn("Respond with exactly this single line", content)

    def test_openai_metadata(self):
        content = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn('display_name: "Say Hello"', content)
        self.assertIn('$say-hello', content)
        self.assertIn("allow_implicit_invocation: false", content)

    def test_codex_plugin(self):
        manifest = json.loads(
            (ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["name"], "hazeship")
        self.assertEqual(manifest["version"], "0.1.0")
        self.assertEqual(manifest["skills"], "./skills/")

    def test_codex_marketplace(self):
        marketplace = json.loads(
            (ROOT / ".agents" / "plugins" / "marketplace.json").read_text(
                encoding="utf-8"
            )
        )
        plugin = marketplace["plugins"][0]
        self.assertEqual(marketplace["name"], "hazeship")
        self.assertEqual(plugin["name"], "hazeship")
        self.assertEqual(plugin["source"]["source"], "url")
        self.assertEqual(
            plugin["source"]["url"],
            "https://github.com/abhiyanhaze/hazeship.git",
        )

    def test_claude_plugin(self):
        manifest = json.loads(
            (ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        marketplace = json.loads(
            (ROOT / ".claude-plugin" / "marketplace.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(manifest["name"], "hazeship")
        self.assertEqual(
            manifest["skills"], ["./skills/productivity/say-hello"]
        )
        self.assertEqual(marketplace["plugins"][0]["source"], "./")

    def test_readme_documents_all_installers(self):
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("npx skills@latest add abhiyanhaze/hazeship", content)
        self.assertIn("claude plugin marketplace add abhiyanhaze/hazeship", content)
        self.assertIn("claude plugin install hazeship@abhiyanhaze", content)
        self.assertIn("codex plugin marketplace add abhiyanhaze/hazeship", content)
        self.assertIn("codex plugin add hazeship@hazeship", content)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Verify the skill-contract test fails**

Run:

```bash
python3 -m unittest tests.test_repository.HazeshipRepositoryTests.test_skill_contract -v
```

Expected: `ERROR` with `FileNotFoundError` for `skills/productivity/say-hello/SKILL.md`.

- [ ] **Step 4: Initialize the skill with the official scaffold**

Run:

```bash
python3 /Users/mac/.codex/skills/.system/skill-creator/scripts/init_skill.py say-hello \
  --path /Users/mac/hazeship/skills/productivity \
  --interface 'display_name=Say Hello' \
  --interface 'short_description=Return a deterministic Nepali greeting' \
  --interface 'default_prompt=Use $say-hello to greet me in Nepali.'
```

- [ ] **Step 5: Replace the generated skill with the minimal contract**

Set `skills/productivity/say-hello/SKILL.md` to:

````markdown
---
name: say-hello
description: Use when the user explicitly invokes /say-hello or $say-hello, or asks for the Hazeship sample Nepali greeting.
---

# Say Hello

Respond with exactly this single line:

```text
नमस्ते! तपाईंलाई हार्दिक अभिवादन।
```

Do not add a translation, transliteration, explanation, or additional greeting
unless the user explicitly requests one.
````

Set `skills/productivity/say-hello/agents/openai.yaml` to:

```yaml
interface:
  display_name: "Say Hello"
  short_description: "Return a deterministic Nepali greeting"
  default_prompt: "Use $say-hello to greet me in Nepali."
policy:
  allow_implicit_invocation: false
```

- [ ] **Step 6: Validate the skill and verify GREEN**

Run:

```bash
python3 /Users/mac/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/productivity/say-hello
python3 -m unittest tests.test_repository.HazeshipRepositoryTests.test_skill_contract tests.test_repository.HazeshipRepositoryTests.test_openai_metadata -v
```

Expected: validator reports success and both tests pass.

- [ ] **Step 7: Commit the canonical skill**

```bash
git add tests/test_repository.py skills/productivity/say-hello
git commit -m "feat: add Nepali greeting skill"
```

---

### Task 2: Add native Claude and Codex packaging

**Files:**
- Create: `.codex-plugin/plugin.json`
- Create: `.agents/plugins/marketplace.json`
- Create: `.claude-plugin/plugin.json`
- Create: `.claude-plugin/marketplace.json`
- Create: `LICENSE`

**Interfaces:**
- Consumes: The canonical `./skills/` tree from Task 1.
- Produces: Native Claude and Codex plugin metadata for `hazeship` version `0.1.0`.

- [ ] **Step 1: Verify packaging tests fail**

Run:

```bash
python3 -m unittest \
  tests.test_repository.HazeshipRepositoryTests.test_codex_plugin \
  tests.test_repository.HazeshipRepositoryTests.test_codex_marketplace \
  tests.test_repository.HazeshipRepositoryTests.test_claude_plugin -v
```

Expected: `ERROR` because the manifest files do not exist.

- [ ] **Step 2: Create the Codex plugin manifest**

Create `.codex-plugin/plugin.json`:

```json
{
  "name": "hazeship",
  "version": "0.1.0",
  "description": "Reusable cross-agent skills from abhiyanhaze.",
  "author": {
    "name": "abhiyanhaze",
    "email": "abhiyan.timilsina@doctustech.com",
    "url": "https://github.com/abhiyanhaze"
  },
  "homepage": "https://github.com/abhiyanhaze/hazeship",
  "repository": "https://github.com/abhiyanhaze/hazeship",
  "license": "MIT",
  "keywords": ["agent-skills", "nepali", "productivity"],
  "skills": "./skills/",
  "interface": {
    "displayName": "Hazeship",
    "shortDescription": "Reusable cross-agent skills",
    "longDescription": "Install reusable skills maintained by abhiyanhaze.",
    "developerName": "abhiyanhaze",
    "category": "Productivity",
    "capabilities": [],
    "defaultPrompt": "Use $say-hello to greet me in Nepali."
  }
}
```

- [ ] **Step 3: Create the Codex repository marketplace**

Create `.agents/plugins/marketplace.json`:

```json
{
  "name": "hazeship",
  "interface": {
    "displayName": "Hazeship"
  },
  "plugins": [
    {
      "name": "hazeship",
      "source": {
        "source": "url",
        "url": "https://github.com/abhiyanhaze/hazeship.git",
        "ref": "main"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

- [ ] **Step 4: Create the Claude plugin manifests**

Create `.claude-plugin/plugin.json`:

```json
{
  "name": "hazeship",
  "version": "0.1.0",
  "description": "Reusable cross-agent skills from abhiyanhaze.",
  "author": {
    "name": "abhiyanhaze"
  },
  "repository": "https://github.com/abhiyanhaze/hazeship",
  "license": "MIT",
  "skills": ["./skills/productivity/say-hello"]
}
```

Create `.claude-plugin/marketplace.json`:

```json
{
  "name": "abhiyanhaze",
  "owner": {
    "name": "abhiyanhaze"
  },
  "description": "Reusable skills from abhiyanhaze.",
  "plugins": [
    {
      "name": "hazeship",
      "source": "./",
      "description": "Cross-agent skills including a Nepali greeting.",
      "category": "productivity",
      "keywords": ["skills", "nepali", "greeting"]
    }
  ]
}
```

- [ ] **Step 5: Add the MIT license**

Create `LICENSE`:

```text
MIT License

Copyright (c) 2026 Abhiyan Timilsina

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 6: Validate plugin packaging and verify GREEN**

Run:

```bash
python3 /Users/mac/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
python3 -m json.tool .codex-plugin/plugin.json
python3 -m json.tool .agents/plugins/marketplace.json
python3 -m json.tool .claude-plugin/plugin.json
python3 -m json.tool .claude-plugin/marketplace.json
python3 -m unittest \
  tests.test_repository.HazeshipRepositoryTests.test_codex_plugin \
  tests.test_repository.HazeshipRepositoryTests.test_codex_marketplace \
  tests.test_repository.HazeshipRepositoryTests.test_claude_plugin -v
```

Expected: all validators and tests pass.

- [ ] **Step 7: Commit packaging**

```bash
git add .codex-plugin .agents/plugins .claude-plugin LICENSE
git commit -m "feat: package hazeship for Claude and Codex"
```

---

### Task 3: Document, install-test, and finish the repository

**Files:**
- Create: `README.md`
- Modify: none

**Interfaces:**
- Consumes: Generic, Claude, and Codex packaging from Tasks 1 and 2.
- Produces: Complete installation and invocation documentation.

- [ ] **Step 1: Verify the README test fails**

Run:

```bash
python3 -m unittest tests.test_repository.HazeshipRepositoryTests.test_readme_documents_all_installers -v
```

Expected: `ERROR` with `FileNotFoundError` for `README.md`.

- [ ] **Step 2: Create the README**

Create `README.md` with:

````markdown
# Hazeship

Reusable skills for Claude Code, Codex, and agents that support the Agent Skills format.

## Available skills

- `say-hello` — Return a deterministic greeting in Nepali.

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
````

- [ ] **Step 3: Run the complete deterministic validation suite**

Run:

```bash
python3 -m unittest discover -s tests -v
python3 /Users/mac/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/productivity/say-hello
python3 /Users/mac/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
```

Expected: six unit tests pass; both validators report success.

- [ ] **Step 4: Test local generic skill discovery**

Run:

```bash
npx skills@latest add /Users/mac/hazeship --list
```

Expected: output discovers `say-hello`. Do not complete a global or project installation.

- [ ] **Step 5: Forward-test the completed skill**

Dispatch a fresh agent with the completed skill and this task:

```text
Use $say-hello at /Users/mac/hazeship/skills/productivity/say-hello to respond to this invocation: /say-hello
```

Expected response exactly:

```text
नमस्ते! तपाईंलाई हार्दिक अभिवादन।
```

- [ ] **Step 6: Rename the branch, inspect the diff, and commit**

Run:

```bash
git branch -M main
git status --short
git diff --check
git add README.md
git commit -m "docs: add cross-agent installation guide"
```

Expected: no whitespace errors, then a clean worktree after the commit.
