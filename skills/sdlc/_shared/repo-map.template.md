# Repo Map — template

> Copy this file to `_shared/repo-map.md` in your project and fill in every
> `<placeholder>`. Maintained by hand thereafter: correct commands/URLs here
> as you discover drift; every skill reads this file instead of
> rediscovering the repos each run. Delete any section (a whole repo entry,
> the ports table, the QA section) that doesn't apply to your project, and
> add more repo entries if you have more than shown here.

## `<repo-name-1>` — `<stack, e.g. "Django + Celery (Python)">`

- Path: `<absolute or workspace-relative path to the repo>`
- Remote: `<git remote URL>`
- Default/staging branch: `<branch PRs target>`
- Setup: `<commands to get a fresh checkout runnable — env files, deps, etc.>`
- Tests: `<test command and where it's configured, e.g. "pytest (pytest.ini) — run `pytest` from repo root">`
- Notable modules/directories: `<key paths a contributor should know about>`
- Sensitive-data exposure: `<none|low|medium|high — what kind, if any, and where>`

## `<repo-name-2>` — `<stack, e.g. "React + TypeScript + Vite">`

- Path: `<path>`
- Remote: `<git remote URL>`
- Default/staging branch: `<branch PRs target>`
- Dev server: `<command>` · Build: `<command>` · Lint: `<command>`
- Local URL: `<http://localhost:<port>>` (note how/where the port is set, if not the framework default)
- Tests: `<test command, or "none configured yet">`
- Sensitive-data exposure: `<none|low|medium|high>`

<!--
Add one entry per repo/sub-repo in the project, following the shape above.
Minimum fields per repo: path, remote, default branch, how to run tests,
how to run lint/typecheck, and dev server command + URL if it's a service.
-->

## Local dev services, ports & logs

<!--
If your project runs multiple services locally, document how to start the
full stack and where each service's logs land. Delete this section if not
applicable.
-->

The full local stack is launched from `<path to your dev-launch config,
e.g. a Warp/tmux layout file or a docker-compose.yml>` (edit that file to
change how a service starts). Each service writes its own logfile under
`<logs directory>`.

| Service | Repo | Port | Logfile |
|---|---|---|---|
| `<service-name>` | `<repo-name>` | `<port>` | `<logfile path>` |
| `<service-name>` | `<repo-name>` | `<port>` | `<logfile path>` |

Notes:
- `<any env vars that wire services together, e.g. frontend → backend URL>`
- `<any platform-specific quirks needed to run a service, e.g. worker pool settings>`
- To read logs, `tail`/`grep` the files above — follow your project's data
  handling rules for anything sensitive that may appear in log output.

## Remote hosts & read-only investigation

<!--
Read by `ssh-readonly-investigation`. One row per environment an agent may be
asked to inspect. Delete this section if no remote hosts are in scope.
-->

| Host label | SSH target | App path | App shell command | Secret wrapper | Logs |
|---|---|---|---|---|---|
| `<staging>` | `<user@host or ssh_config alias>` | `<path on host>` | `<command that opens the app's shell, e.g. a framework shell/REPL>` | `<secret-injection prefix, e.g. "<tool> run -p <project> -c <config> --command">` | `<log paths, or how to tail them>` |
| `<production>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |

Notes:
- `<bastion/jump host and the hop syntax, if any>`
- `<who may access which host, and what approval a production read needs>`
- `<data-handling rule for anything read off these hosts — what may be pasted
  into notes/docs and what may not>`
- Investigation is read-only by default; widening that scope is an explicit,
  per-request decision by the user.

## Persistent memory store

<!--
Read by `persistent-memory`. Delete if the project uses the default
`<repo root>/.hazeship/memory/`.
-->

- Store root: `<absolute path, or "default — <repo root>/.hazeship/memory/">`
- Configured via: `<HAZESHIP_MEMORY_DIR in the shell env | HAZESHIP_MEMORY_DIR
  in <path>/.hazeship/config.env | default marker location>`
- Project key: `<slug used as <project-key> in bucket paths>`
- Committed or gitignored: `<which, and why — buckets hold project context, so
  this is a deliberate call>`

## QA credentials & environments

<!--
If your project has an automated QA/E2E runner with its own test
credentials, document the guardrails here. Delete this section if not
applicable.
-->

- Test credentials: `<path to a gitignored, user-maintained credentials file>`.
  Decide and record here whether agents may read it directly, or whether
  only the test runner process may load it (agents see reporter output only).
- Key reference + sample values: `<path to a tracked example/template file>`.
  Note any guard env vars the runner enforces (e.g. an "allowed hosts" list,
  an explicit "this is a synthetic/test environment" marker).
- `<any manual-step-in-the-loop auth flow, e.g. OTP>`: describe how it's
  handled and who is allowed to see the code, if applicable.
- Test accounts: `<describe scope — least-privilege, dedicated test tenant, etc.>`
- `<path to saved login/session state, if any>` is secret material — never
  read, copy, or commit it.
- State your project's rule for what test data QA runs may use (e.g.
  synthetic data only) and where that rule is documented in full.
