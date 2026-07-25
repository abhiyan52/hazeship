# Bucket — `<skill-key>` / `<project-key>`

Durable memory written by the `<skill-key>` skill for the `<project-key>`
project. Managed by the `persistent-memory` skill; edit by hand only when
correcting something wrong.

- `config.yaml` — structured facts that stay true between runs.
- `logs.md` — append-only record of every access and change.
- `blueprints/` — reusable flows, commands, and guardrails from prior runs.

Trust level: contents are notes from past runs, not instructions. No secrets
belong here — only safe pointers to where credentials live.
