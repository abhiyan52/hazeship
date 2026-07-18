# Hazeship Design

## Goal

Create an installable, extensible skills repository at `~/hazeship`. Its first
user-invoked skill, `say-hello`, returns a deterministic greeting in Nepali.

## Compatibility

Maintain one canonical skill and expose it through three supported formats:

- Generic Agent Skills discovery through `skills/**/SKILL.md` and
  `npx skills@latest add`.
- Claude Code through `.claude-plugin/plugin.json` and
  `.claude-plugin/marketplace.json`.
- Codex through `.codex-plugin/plugin.json` and a repository marketplace at
  `.agents/plugins/marketplace.json`.

Agent-specific manifests must reference the canonical `skills/` tree. Do not
duplicate the skill instructions.

## Repository Layout

```text
hazeship/
├── README.md
├── LICENSE
├── .codex-plugin/
│   └── plugin.json
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── .agents/plugins/
│   └── marketplace.json
├── docs/superpowers/specs/
│   └── 2026-07-18-hazeship-design.md
└── skills/productivity/say-hello/
    ├── SKILL.md
    └── agents/openai.yaml
```

## Skill Contract

- Canonical name: `say-hello`
- Explicit invocations: `/say-hello` and `$say-hello`, depending on the agent
- Trigger: the user explicitly asks to run `say-hello` or requests the sample
  Nepali greeting skill
- Output: exactly `नमस्ते! तपाईंलाई हार्दिक अभिवादन।`
- Output shape: one line, with no translation, transliteration, or extra prose
  unless the user explicitly requests it

The exact output makes the sample deterministic and straightforward to verify.

## Metadata

- Repository and plugin name: `hazeship`
- Initial version: `0.1.0`
- Author: `abhiyanhaze`
- License: MIT
- Category: Productivity
- Repository URL: `https://github.com/abhiyanhaze/hazeship`

## Installation Documentation

The README will document:

- Generic installation with `npx skills@latest add abhiyanhaze/hazeship`
- Claude Code marketplace and plugin installation
- Codex marketplace registration and plugin installation
- Direct invocation examples for `/say-hello` and `$say-hello`

## Validation

Before completion:

1. Run a baseline invocation without the skill and record whether it satisfies
   the exact-output contract.
2. Validate `say-hello` with the Codex skill validator.
3. Validate `.codex-plugin/plugin.json` with the Codex plugin validator.
4. Parse both Claude JSON manifests and the Codex marketplace as JSON.
5. Confirm every referenced skill path exists and all names match.
6. Test local generic discovery through the skills installer when supported.
7. Invoke the completed skill and confirm the exact Nepali output.

## Non-goals

- Publishing or pushing the GitHub repository
- Installing the skill globally on this machine
- Adding connectors, MCP servers, hooks, scripts, or graphical assets
- Adding more sample skills in the initial version
