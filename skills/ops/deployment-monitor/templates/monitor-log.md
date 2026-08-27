# Deployment monitor — <host label> / <project>

Target: <ssh target as approved>          App path: <path>
Depth approved: <shell+logs | shell+logs+read-only DB aggregates>
Probe: <path to probe script> `<usage>`
Window: <start UTC> → <END_AT UTC>, sweep every <interval>, <N> sweeps
Opened from: <handoff or notes path, if any>

## STATE (update every sweep)
OFFSETS=<name>:<bytes> <name>:<bytes>
SWEEPS_DONE=0
LAST_SWEEP=<UTC>
END_AT=<UTC>

## Baseline — sweep 0, <UTC>

<What deployed, service state, resources, queues, scheduled jobs and their
cadence, error profile, request health. One line per fact. This is the reference
every later delta is measured against.>

## Ledger

### Watchlist
<!-- F<N> — one entry per open finding. Observation, evidence with its exact
     time range, whether it predates the window, what it rests on, and what
     the next sweep should check. Mark a hypothesis as a hypothesis. -->

### Settled
<!-- F<N> — resolved, or confirmed not-a-defect, with the evidence that
     settled it. Never re-investigated; confirmed cheaply. -->

### Blind spots
<!-- Watch items whose trigger falls outside the window: the job's cadence,
     the next time it fires, and the window's end. Their absence is evidence
     of nothing. -->

## Sweep log

<!-- Newest row directly under the header. -->

| # | UTC | Verdict | Delta |
|---|---|---|---|
| 0 | <UTC> | baseline | <findings on arrival> |

## Closing summary

<!-- Written at END_AT or the final sweep:
     1. Verdict for the window, with its exact bounds.
     2. Every finding by number and final state; for anything still open, what
        the next run should do with it.
     3. Blind spots restated — what the window could not see, and when it could.
     4. What was written back to the memory bucket. -->
