# Delivery Operating Model

## Operating Principle

Execution follows agile principles, but with stronger traceability and dependency discipline than a typical feature backlog. Work progresses in small, inspectable increments, each increment must create a shippable improvement in evidence fidelity, policy safety, or analyst utility, and every increment must preserve architectural constraints. Iteration is encouraged; undocumented divergence is not.

## Default Cadence

- Planning cadence: weekly planning cycle anchored to the current highest-priority ready tasks on the critical path.
- Daily coordination: asynchronous status updates in the PM workspace and synchronous escalation only for blockers, policy issues, or architecture conflicts.
- Risk review cadence: weekly.
- Decision review cadence: at the moment a choice would cause code or schema divergence.
- Release review cadence: at the end of each phase gate or milestone candidate.

This cadence may be tightened or relaxed later, but it is the default until the team records a replacement in the decision log.

## Delivery Unit Hierarchy

- Program: the full platform described in the architecture.
- Phase: a major delivery slice with entry criteria and exit criteria.
- Task: a bounded piece of work that produces a durable output and can be owned by a senior contributor or subagent.
- Subtask: a concrete execution step required to complete a task.
- Work package: the handoff wrapper used to assign a task to a contributor or subagent.

## Team Topology

The plan assumes dedicated ownership lanes, not a single undifferentiated queue:

- Platform and infrastructure
- Data plane and orchestration
- Document processing and evidence modeling
- Policy, security, and review systems
- NLP, entity, event, and resolution pipelines
- Retrieval, graph, and analytics
- Backend-for-frontend and service contracts
- Web application and analyst experience
- Validation, evaluation, observability, and release engineering

One person or one subagent may cover more than one lane, but the lane model remains useful for dependency management and conflict avoidance.

## Work Selection Rules

Use this order of operations when selecting work:

1. Prefer tasks on the explicit critical path in [`04_dependency_map.md`](./04_dependency_map.md).
2. If the critical path is blocked, pull the highest-value parallelizable task whose prerequisites are complete.
3. Do not start a task marked `blocking` if any hard predecessor is incomplete.
4. Do not start implementation work when the needed architectural decision is still tracked as open.
5. If a task can begin only against mocks or provisional contracts, record the dependency as `soft_dependency` and document the provisional status.

## Definition Of Ready

A task is ready only when all of the following are true:

- the task exists in a phase backlog file with an ID, objective, dependencies, and acceptance criteria
- relevant architecture constraints are identified
- upstream hard dependencies are complete or explicitly waived in the decision log
- required inputs, schemas, or interface contracts exist
- required external decisions are recorded and resolved or isolated
- validation expectations are known
- local, integration, and coverage obligations are known, including the standing requirement for 100% handwritten-code coverage and 100% passing local and integration suites
- ownership is clear and no conflicting file ownership is active

## Definition Of Done

A task is done only when all of the following are true:

- all required subtasks are complete
- code, documents, schemas, or infrastructure outputs exist in version control
- local automated tests pass at 100 percent
- integration tests pass at 100 percent
- handwritten code touched by the task is covered at 100 percent before the task is closed
- relevant validation checks or evaluations have passed
- policy, provenance, and observability obligations are satisfied
- required docstrings, inline rationale comments, and operational documentation are present for non-trivial additions
- downstream documentation has been updated:
  - relevant phase backlog file
  - [`11_status_dashboard.md`](./11_status_dashboard.md)
  - [`06_risk_register.md`](./06_risk_register.md) if risk changed
  - [`07_decision_log.md`](./07_decision_log.md) if a design choice was made
  - current session log

## Dependency Management Rules

- Hard dependencies are never implied. They must be written explicitly in the task.
- If two tasks can run concurrently but may touch adjacent interfaces, record them as `parallelizable` and specify the integration boundary.
- If a task depends on research rather than implementation, link the open research question and keep the task blocked until resolved.
- If a task depends on policy signoff, legal clarification, or role definition, treat that dependency as hard until resolved.
- If implementation uncovers a missing upstream task, create the missing task in the appropriate backlog before proceeding.

## Agile Slice Strategy

The program should deliver through vertical slices, not only horizontal infrastructure completion. The recommended slicing pattern is:

1. make evidence immutable and inspectable
2. make evidence policy-safe
3. turn evidence into structured analytical objects
4. make structured objects searchable and reviewable
5. expose them through an evidence workbench
6. add controlled QA only after citation, support, and policy controls exist

This pattern is consistent with the architecture’s insistence that model-driven features are downstream of evidence and review.

## Parallelization Strategy

The default parallel lanes are:

- infra/platform
- docproc/evidence
- policy/security
- semantics/extraction
- analytics/retrieval
- BFF/UI
- validation/release

Parallel execution is allowed only when:

- dependencies permit it
- the tasks do not create conflicting ownership over the same file set or interface surface
- integration expectations are documented in the work package

## Task Sizing And WIP Discipline

- A single contributor or subagent should normally own:
  - one critical-path task
  - optionally one smaller parallelizable task
- If a task cannot be explained clearly in one work package, split it before assignment.
- If a task touches more than one workstream owner, define the integration boundary before work starts.
- Long-running work must leave intermediate acceptance evidence in the relevant backlog and session log.

## Backlog Refinement Procedure

Use this procedure when adding, splitting, or clarifying work:

1. identify the affected phase and workstream
2. confirm whether the work changes the critical path or only a parallel lane
3. assign or update explicit dependencies
4. record required artifacts, open questions, and signoff roles
5. update the dependency map if cross-task sequencing changes
6. update the dashboard if active or next-ready work changes

## Planning Agenda

Each planning cycle should explicitly cover:

1. active critical-path tasks
2. blocked tasks and blocker age
3. ready parallel work
4. open decisions and deadlines
5. active risks and contingency triggers
6. milestone evidence still missing

## Blocked-Work SLA

- If a task becomes blocked, update the backlog and dashboard in the same session.
- If a block affects the critical path, escalate immediately.
- If a block lasts more than one planning cycle, add an explicit mitigation or workaround task.
- If a block depends on external governance or budget, link the open question and stop inferring local answers.

## Defer Or Cancel Rules

- Defer a task when the scope remains valid but prerequisites or release priority do not.
- Cancel a task only when scope has changed and the decision log records the change.
- Never silently stop tracking a task that once existed on the critical path.

## Hotfix Or Emergency Change Flow

- Confirm whether the issue is local, release-scoped, or program-scoped.
- Contain the issue first.
- Record the exception in the session log and, if durable, in the decision log.
- Create follow-up work to restore the normal architecture, promotion, or policy model.

## Retro And Demo Cadence

- Demo cadence: at each phase gate or milestone candidate.
- Retrospective cadence: at least once per milestone, or immediately after a failed release gate or major incident.
- Retro outputs must produce either:
  - a backlog update
  - a risk update
  - a decision-log entry
  - a process-rule update

## Documentation Maintenance Matrix

- Scope change:
  - update charter if program scope changes
  - update phase plan, dependency map, and release strategy
- New artifact class:
  - update artifact inventory
  - update quality gates if verification changes
- New policy rule:
  - update architecture constraints, risk register, and affected backlog files
- New external dependency:
  - update research register and decision boundaries
- New blocker:
  - update dashboard, backlog status, and session log

## Documentation Rules

- Stable planning context lives in the root `pm/` files.
- Detailed execution detail lives in `pm/backlog/`.
- Session continuity lives in `pm/logs/`.
- External citations live in `pm/08_research_register.md` and `pm/research/source-catalog.md`.
- Subagent instructions live in `pm/subagents/`.
- Terminology lives in `pm/13_glossary.md`.
- Artifact ownership and systems of record live in `pm/14_artifact_inventory.md`.
- Cross-cutting non-functional requirements live in `pm/15_non_functional_requirements.md`.
- Signoff and escalation boundaries live in `pm/16_decision_boundaries.md`.
- Phase handoff expectations live in `pm/17_phase_interlocks.md`.

## Subagent Execution Protocol

Every subagent must:

1. read [`11_status_dashboard.md`](./11_status_dashboard.md)
2. read [`01_architecture_constraints.md`](./01_architecture_constraints.md)
3. read [`13_glossary.md`](./13_glossary.md)
4. read [`14_artifact_inventory.md`](./14_artifact_inventory.md)
5. read [`16_decision_boundaries.md`](./16_decision_boundaries.md)
6. read [`04_dependency_map.md`](./04_dependency_map.md)
7. read the assigned phase backlog file
8. confirm dependencies and ownership boundaries
9. execute only the bounded work package
10. report validation, risks, and documentation updates in the handoff format

## Escalation Rules

Escalate immediately when any of the following occur:

- a required constraint cannot be satisfied
- a policy or legal interpretation is ambiguous
- a datastore or interface choice would diverge from the architecture
- a task requires a new external dependency with security or licensing implications
- a blocked dependency would idle multiple workstreams
- a research finding invalidates an existing plan assumption or threshold

## Release Discipline

- No milestone advances solely because code was merged.
- Every milestone requires the quality gates defined in [`09_quality_gates.md`](./09_quality_gates.md).
- Pilot and production milestones require explicit release criteria from [`10_release_strategy.md`](./10_release_strategy.md).

## References

- Agile principles: https://agilemanifesto.org/principles.html
- Scrum Guide: https://scrumguides.org/scrum-guide.html
- Architecture basis: [`Architecture_Plan.md`](../Architecture_Plan.md), especially lines 11-18, 89-95, 221-243, 247-287, 411-462
