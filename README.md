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
