# Workspace Setup — what this kit needs in a project, and how to create it

The SDLC skills read and write files in the project they're run against.
This is the one-time bootstrap that puts those files in place. It is
idempotent: never overwrite a file the project already has — a project's own
`repo-map.md`, templates and `tools/sdlc` may have been customised on
purpose.

## The workspace

"Workspace root" is the directory the SDLC artifacts live in — the **meta
repo** if the project spans several repos, otherwise the repo itself. It is
the directory containing `docs/features/`.

```
<workspace-root>/
├── _shared/
│   └── repo-map.md            # this project's repos, commands, data rules
├── docs/
│   ├── adr/                   # architecture decision records
│   ├── bugs/<slug>/           # one folder per bug (report.md, by /bugfix)
│   ├── features/<slug>/       # one folder per feature (manifest + artifacts)
│   ├── learning/              # cross-cutting lessons from /teach
│   ├── team-handoff/<project>/# tracked questions to humans
│   ├── templates/             # the document templates below
│   └── triage/                # dated triage reports (by /triage)
├── seeds/                     # synthetic fixtures (created by seed-data)
└── tools/
    ├── sdlc                   # the feature state machine
    └── docx/build-docx.sh     # markdown → DOCX (optional, /to-technical-doc)
```

Belong in the workspace's `.gitignore`: `.worktrees/` (used by
`implement-slice`), `*.docx` (regenerable from the markdown), and
`seeds/**/output/` (generated dumps and exports).

## First-run bootstrap

Run this from the workspace root. `<kit>` is this skill kit's `skills/sdlc`
directory — the same place the file you're reading now lives.

```bash
mkdir -p _shared docs/templates docs/features docs/adr tools/docx

# The state machine and the DOCX builder.
cp -n <kit>/_shared/tools/sdlc            tools/sdlc
cp -n <kit>/_shared/tools/build-docx.sh   tools/docx/build-docx.sh
chmod +x tools/sdlc tools/docx/build-docx.sh

# The document templates.
cp -n <kit>/_shared/templates/*           docs/templates/

# The project's own repo map, from the template.
cp -n <kit>/_shared/repo-map.template.md  _shared/repo-map.md
```

`cp -n` is what makes this safe to re-run: existing files are left alone.

Then **fill in `_shared/repo-map.md`** before running any other skill. Every
skill reads it instead of rediscovering the repos, so an unfilled repo-map is
the single most common cause of a skill guessing wrong.

## Templates and the documents they produce

| Template | Produces | Written by |
|---|---|---|
| `manifest.yaml` | `docs/features/<slug>/manifest.yaml` | feature-intake |
| `gap-analysis.md` | `01-gap-analysis.md` | feature-intake |
| `tech-design.md` | `02-tech-design.md` | tech-design |
| `dev-plan.md` | `03-dev-plan.md` | dev-plan |
| `slice-log.md` | `slices/slice-<NN>.md` | implement-slice |
| `validation.md` | `04-validation.md` | validate-feature |
| `retro.md` | `05-retro.md` | retro |
| `team-handoff.md` | `docs/team-handoff/<project>/<NNN>-<topic>.md` | team-handoff |
| `technical-doc.md` | `technical-doc.md` + `.docx` | to-technical-doc |
| `bug-report.md` | `docs/bugs/<slug>/report.md` | bugfix |

## `tools/sdlc`

The feature state machine. It owns every state field in the manifest and
refuses illegal transitions, so no skill has to re-implement the rules.

```
tools/sdlc show <slug>                        # current stage, gate, slices
tools/sdlc validate <slug>                    # check the manifest
tools/sdlc transition <slug> <stage>          # advance (needs an approved gate)
tools/sdlc gate <slug> <in-progress|awaiting-approval|blocked>
tools/sdlc approve <slug> [--artifact F]      # the USER runs this
tools/sdlc slice <slug> <NN> <state> [--pr U]
```

- Requires Python 3 and PyYAML (`python3 -m pip install pyyaml`).
- Finds the workspace root by walking up from the current directory looking
  for `docs/features/`; pass `--root <path>` to be explicit.
- Every write bumps `revision`, so a stale copy of a manifest is detectable.
- Writes are targeted line edits, so hand-written `handoffs:` entries,
  comments and key order survive untouched.
- `approved` cannot be set with `gate` — only `approve` records it, together
  with who approved, when, which artifact, and the artifact's commit SHA.
  That's what makes an approval auditable later.

## If the project already has its own tooling

A project may already have a `tools/sdlc` with different commands, or its own
templates. Use what's there — do not overwrite it, and do not silently fall
back to this kit's copy. If a command a skill needs doesn't exist, say so and
ask, rather than guessing at an equivalent.
