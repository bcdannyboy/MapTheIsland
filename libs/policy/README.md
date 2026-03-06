# Policy Library Baseline

This library is the executable home for shared policy vocabulary and helpers
after the Phase 00 policy baseline.

## Phase 01 Kickoff Scope

Phase 01 begins with the deny-by-default executable policy baseline under
`src/maptheisland_policy/`. The initial source root now carries:

- role vocabulary
- normalized access-disposition vocabulary
- executable sensitivity-handling rules
- executable role-capability rules
- prohibited-flow constants that later phases must turn into negative tests

## Policy Surface

- sensitivity taxonomy values and helpers
- role and capability vocabulary
- policy decision and deny-reason types
- export-control helpers
- prohibited-flow constants used by service and UI policy enforcement

The human-readable authority for the initial rules lives in
`docs/implementation/policy-taxonomy-and-safety-model.md`. No service should
fork shared sensitivity, export, or deny-reason semantics locally once the
library begins carrying executable policy types.

## Ownership And Contribution Path

- Primary owner role: policy and security lead
- Required co-review: architecture lead and affected consuming owner
- Safe contribution pattern:
  - keep final governance assumptions deny-by-default until `OQ-03` is resolved
  - do not widen restricted-role or export behavior locally inside a service
  - update the policy implementation doc and PM surfaces when shared policy
    semantics change
