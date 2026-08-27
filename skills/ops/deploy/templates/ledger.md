# Deployment ledger

Append-only. Newest entry at the bottom. One entry per deployment or
rollback — including failed ones.

Format:

```
## <YYYY-MM-DD HH:MM TZ> — <environment> — <deployed|rolled back|failed>
- Ref: <sha/branch/tag deployed>
- Changes: <commits/PRs included since the previous entry for this env>
- Go given by: <user>
- Verification: <what was checked, and the result>
- Issues: <anything unexpected, or "none">
- Rollback point: <ref/state to return to>
```
