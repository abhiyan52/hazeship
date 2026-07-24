# Branch, Commit & PR Conventions

## Branches

| Purpose | Pattern | Created from | Merges into |
|---|---|---|---|
| Feature (integration) branch | `feat/<feature-slug>` | repo's default/staging branch | default/staging branch via final PR |
| Slice/work branch | `feat/<feature-slug>-slice-<NN>` | `feat/<feature-slug>` | `feat/<feature-slug>` via slice PR |
| Bug fix | `bug/<short-desc>` | repo's default/staging branch | default/staging branch |

Default/staging branch per repo: see `repo-map.md`.

Flow: when implementation starts (first slice, after the dev plan is
approved), create the empty `feat/<slug>` branch from the default/staging
branch and push it. Each slice branches off it and lands back into it; at
feature completion one final PR goes `feat/<slug>` → default/staging branch
(full review, always).

## Risk-based slice PR policy

The dev plan sets a PR policy per slice; `raise-pr` enforces it.

- **Slice PR + review REQUIRED** when the slice touches any of: more than one
  repo, sensitive-data-bearing code paths, authn/authz, DB migrations,
  external integrations, or anything the tech design's risk table marks
  medium+.
- **Slice PR may be WAIVED** for small, single-repo, low-risk slices: after
  the user approves the demo, the slice branch merges directly into
  `feat/<slug>` (recorded via `tools/sdlc slice <slug> <NN> merged`). The
  final PR review still covers this code — waiving the slice PR defers
  review, it never skips it.
- Default when unsure: required.

## Commit message format

```
<type>: <imperative subject ≤ 72 chars>

What we built:
- <concrete change 1>
- <concrete change 2>

Why:
<1–3 lines tying the change to the PRD/tech design/slice>

How to test:
- <exact command or click-path>
- <expected result>

Co-Authored-By: <agent name> <noreply@example.com>
```

`<type>`: feat | fix | refactor | test | docs | chore.
One logical change per commit; a slice typically lands as 1–4 commits.
Never commit: `.env*`, credentials, real user/customer data, generated
binaries unless asked.

## PR format

Title: `<type>: <feature title> — slice <NN>: <slice name>` (or without the
slice suffix for the final PR).

Body:

```
## What
<what this PR delivers — the vertical slice in one paragraph>

## Why
<link to feature docs: docs/features/<slug>/, PRD reference>

## How to test
1. <step>
2. <expected>

## Compliance
- [ ] No sensitive data in logs/fixtures/screenshots (checked against project data-handling rules)
- [ ] New endpoints have authn + object-level authz
- [ ] Synthetic/test data only

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

Slice PRs target `feat/<slug>`; final PR targets the repo's default/staging
branch.
