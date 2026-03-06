# Backlog Conventions

## Purpose

The backlog files are the detailed execution layer of the plan. Each phase file contains exhaustive tasks and subtasks with explicit dependencies, outputs, and acceptance criteria.

Each phase file should also include phase-level context so contributors do not have to infer cross-phase handoff expectations. The current standard phase-level context is:

- phase objective
- architecture traceability
- entry and exit criteria
- phase handoff summary
- produced and consumed artifacts
- blocking open questions
- primary signoff roles

## Required Fields Per Task

- Task ID
- Title
- Status
- Objective
- Architecture traceability
- Dependencies
- Parallelization
- Required external decisions
- Consumed artifacts or upstream outputs when known
- Produced artifacts or downstream outputs when known
- Allowed interface or contract surfaces to modify when relevant
- Primary downstream consumers blocked by the task when relevant
- Deliverables
- Acceptance criteria
- Subtasks

## Required Fields Per Subtask

- Subtask ID
- Description
- Depends on
- Dependency classification
- Parallelization note
- Concrete output

## Status Values

- `planned`
- `active`
- `blocked`
- `done`
- `deferred`

## Dependency Language

- `blocking`: hard predecessor
- `soft_dependency`: helpful but not blocking
- `independent`: may start immediately
- `parallelizable`: safe to run alongside specified tasks or subtasks

## Update Rule

When a task changes, update:

1. the relevant phase backlog file
2. [`../11_status_dashboard.md`](../11_status_dashboard.md)
3. the current session log under [`../logs/`](../logs)

If the change affects risk, scope, or external research, update the relevant root PM files in the same session.
