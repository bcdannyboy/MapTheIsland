# Concurrency Protocol

This file defines how multiple contributors or agents work in parallel without corrupting shared state or planning artifacts.

## Task Claiming

- Claim one primary task at a time unless the second task is explicitly parallelizable and non-overlapping.
- Check the backlog, dashboard, and current session log before treating a task as unclaimed.
- If claim state is unclear, pause and escalate rather than creating duplicate work.

## Edit-Lock Etiquette

- Shared-contract files, schema files, and system-of-record docs are high-coordination surfaces.
- If work touches one of those surfaces, state that explicitly in the work package and handoff.
- Avoid simultaneous edits to the same shared contract surface unless the integration boundary is already agreed.

## Stale-Task Recovery

- If a task appears abandoned, verify via the session log and dashboard before resuming it.
- If no continuity record exists, resume only after documenting the takeover in the current session log.

## Partial Handoffs

- Partial work is acceptable only if it leaves:
  - exact files changed
  - exact validations run
  - exact blockers still open
  - exact PM files needing update
- “Almost done” is not an acceptable handoff description.

## Conflict Resolution

- If the backlog and dashboard disagree, reconcile them before continuing.
- If the implementation and the dependency map disagree, treat the dependency map as canonical until the PM workspace is updated.
- If a local code change would require re-sequencing multiple workstreams, stop and escalate.

## Timeout Rule

- If a contributor or subagent cannot complete the assigned work inside the current session or package scope, they must leave a handoff instead of silently holding the task.

## Shared-Contract Rule

- Contract changes require:
  - explicit mention in the handoff
  - downstream impact note
  - relevant PM updates if the contract changed materially
