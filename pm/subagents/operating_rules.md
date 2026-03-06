# Subagent Operating Rules

## Rule 1: Respect The Constraints

Do not implement around [`../01_architecture_constraints.md`](../01_architecture_constraints.md). If the assigned task conflicts with a constraint, stop and escalate.

## Rule 2: Confirm Dependencies Before Work

Read the assigned task and confirm all `blocking` predecessors are complete. If not, mark the task blocked instead of proceeding speculatively.

## Rule 3: Stay Inside The Work Package

Do not broaden scope. If additional work is required, record a follow-up task or escalate.

## Rule 4: Avoid Ownership Conflicts

Do not overwrite or revert adjacent work from other contributors. If the task touches a shared contract or schema, coordinate through the PM workspace before editing.

## Rule 4A: Claim Work Explicitly

- Confirm the task in the backlog before starting.
- If the dashboard and backlog disagree, trust the backlog for task detail and update the dashboard before proceeding.
- If another contributor appears to own the same task, stop and escalate instead of assuming abandonment.

## Rule 5: Record Research And Decisions

If you rely on new external documentation, add it to [`../08_research_register.md`](../08_research_register.md). If you make a new architecture or delivery decision, log it in [`../07_decision_log.md`](../07_decision_log.md).

If you introduce a new artifact class, change a system of record, or change a promotion rule, update [`../14_artifact_inventory.md`](../14_artifact_inventory.md). If you change a cross-cutting operational requirement, update [`../15_non_functional_requirements.md`](../15_non_functional_requirements.md).

## Rule 6: Report Validation Honestly

State exactly what was tested or not tested. Do not imply a validation step passed if it was not run.

## Rule 7: Leave A Usable Handoff

Always provide completed work, files changed, validations run, risks found, next steps, and the PM files that were updated.

## Rule 8: Shared-Contract Changes Need Extra Coordination

- If a task touches a shared schema, API contract, event contract, or system-of-record rule, record that in the handoff.
- Do not make breaking contract changes without checking decision boundaries and dependency impact.

## Rule 9: Timeouts And Partial Progress Must Be Reported

- If you cannot finish a task, leave a partial handoff instead of disappearing from the queue.
- Report exactly what is complete, what is partial, and what remains blocked.
