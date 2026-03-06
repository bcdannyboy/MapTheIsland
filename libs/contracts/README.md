# Contracts Library Baseline

This library is the executable home for cross-boundary contracts after the
Phase 00 service and contract baseline.

## Phase 01 Kickoff Scope

Phase 01 begins with the smallest safe executable contract slice:

- service-name and service-boundary registry types
- integration event envelope types
- operational endpoint constants for long-lived services

These live under `src/maptheisland_contracts/` and are validated by the root
Python test and typing workflow.

## Contract Surface

- BFF request and response envelopes
- service-to-service synchronous payloads where an explicit business API is
  justified
- async event payload schemas and their version metadata
- contract versioning assets needed by generated clients or compatibility tests

The human-readable authority for the initial rules lives in
`docs/implementation/service-boundaries-and-contracts.md`. No service should
publish a reusable cross-boundary payload outside this library once Phase 01
implementation begins.

## Ownership And Contribution Path

- Primary owner role: BFF and API lead
- Required co-review: architecture lead plus at least one consuming owner
- Safe contribution pattern:
  - publish cross-boundary payload changes here first
  - update the implementation docs if the contract meaning changes
  - keep event naming and `schema_version` behavior aligned with the published
    contract rules
