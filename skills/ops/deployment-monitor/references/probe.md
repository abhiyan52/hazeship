# Building the probe

One script, run once per sweep, whose output you can diff against the previous
sweep. It takes the log offsets from the last sweep as arguments and prints the
new offsets as its last line, so the next sweep reads only what arrived since.

## Why offsets

A busy service writes tens of megabytes of log per day. `tail -n 500` gives you
an arbitrary slice that overlaps the last sweep and misses a burst; `grep -c`
over the whole file re-counts history and reports a rising number that says
nothing about the last 15 minutes. Byte offsets make each sweep's window exact
and its counts genuinely per-sweep.

```bash
SIZE=$(stat -c%s app.log)                 # record for the next sweep
tail -c +$((OFFSET+1)) app.log            # only what arrived since
```

Guard the arithmetic: when the stored offset exceeds the current size, the file
rotated. Fall back to reading the whole file and say the sweep spans a rotation,
rather than reporting a silent zero.

## Shape

Print one labelled section per concern, in a fixed order, one fact per line —
a stable layout is what makes two sweeps diffable by eye. Keep it to a single
SSH invocation; twelve sweeps of a chatty script is a lot of round trips.

Cover the baseline's concerns: deployed commit and host drift, service state
with restart counters, load/memory/disk, queue depths, scheduled jobs fired
since the last sweep, error counts grouped by logger and exception class, task
outcomes, and request status codes.

End with the new offsets on their own line so the next sweep can parse them.

## Aggregate on the host

Group and count remotely; bring back the summary. A structured log parses more
reliably with a few lines of `python3` on the host than with a regex over JSON,
and it keeps raw records — which is where sensitive data lives — out of your
context entirely.

Normalize before counting, or every message with an id or a duration in it
becomes its own unique "type":

```bash
sed 's/[0-9a-f-]\{8,\}/<id>/g; s/[0-9]\+/<n>/g' | sort | uniq -c | sort -rn
```

## Cheap, then deep

The probe stays cheap enough to run every sweep. When it surfaces something
odd, follow up with separate bounded commands scoped to that one question —
rather than growing the probe until every sweep pays for a check that mattered
once.

Record the probe's path in the host blueprint. A probe that a later run can
re-run as-is is most of what makes run two fast.
