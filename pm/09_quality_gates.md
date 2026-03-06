# Quality Gates

Each gate is blocking unless the decision log explicitly grants an exception.

## Absolute Verification Rule

- No task, subtask, phase, milestone, or release may be accepted with a failing automated local test.
- No task, subtask, phase, milestone, or release may be accepted with a failing integration test.
- No task, subtask, phase, milestone, or release may be accepted unless handwritten code remains at 100 percent coverage.
- If a code change introduces a new path, the tests and coverage enforcement for that path are part of the same change set.
- Exceptions are not allowed for the universal 100 percent local-pass, 100 percent integration-pass, and 100 percent handwritten-code coverage rule recorded in `D-010`. Work that fails that rule remains incomplete.

## Gate Evidence Package Requirements

Every gate review should point to:

- the tasks or subtasks being accepted
- the artifacts being promoted
- the local and integration test reports used as evidence
- the coverage report proving 100 percent handwritten-code coverage for the affected scope
- the validation outputs or evaluation reports used as evidence
- the active risks that remain open after signoff
- the role archetype accountable for signoff

If any of those elements is missing, the gate is not ready for signoff.

## QG-01: Contract And Schema Baseline

- Applies to: Phase 00 completion
- Required evidence:
  - canonical evidence schema defined
  - review-state model defined
  - sensitivity taxonomy defined
  - BFF and service contract baseline defined
- Failure mode:
  - later work proceeds on implicit contracts

## QG-02: Reproducible Platform Baseline

- Applies to: Phase 01 completion
- Required evidence:
  - reproducible infra definition exists
  - stateful services bootstrap succeeds in the target environment
  - secrets and certificates are not hard-coded
  - CI runs baseline checks
- Failure mode:
  - environment-specific drift or non-reproducible deploys

## QG-03: Evidence Ingest Reproducibility

- Applies to: Phase 02 completion
- Required evidence:
  - ingest branch and merge workflow works
  - manifest and raw evidence hashes reconcile
  - `Document`, `Page`, and `Span` assets materialize with provenance
  - failed validation branches remain auditable
- Failure mode:
  - evidence cannot be replayed or trusted

## QG-04: Policy And Review Enforcement

- Applies to: Phase 03 completion and every later release
- Required evidence:
  - restricted spans are filtered correctly
  - unauthorized roles cannot access protected routes, queries, or exports
  - review and adjudication events persist and trigger downstream updates
  - audit logging covers sensitive actions
- Failure mode:
  - unsafe disclosure or non-auditable high-impact actions

## QG-05: Semantic Extraction Credibility

- Applies to: Phase 04 completion
- Required evidence:
  - extraction outputs attach to source spans
  - identity merges have review paths
  - event extraction distinguishes confidence and temporal uncertainty
  - redaction objects obey safe-handling rules
- Failure mode:
  - graph, retrieval, and UI surfaces rest on uninspectable semantics

## QG-06: Retrieval And Analytics Defensibility

- Applies to: Phase 05 completion
- Required evidence:
  - search returns explainable match reasons
  - graph edges differentiate evidence-backed and inferred semantics
  - analytics tables derive from event-centric data rather than raw co-mention
  - evaluation and MLflow tracking cover major models and heuristics
- Failure mode:
  - analysts cannot tell why results were produced

## QG-07: Evidence Workbench Readiness

- Applies to: Phase 06 release candidate
- Required evidence:
  - search works across major artifact classes
  - document viewer can reconcile image/native/OCR layers
  - entity and event pages expose supporting evidence and confidence state
  - review workbench is usable end to end
  - job polling and cache invalidation behave deterministically
- Failure mode:
  - first analyst-facing release is not operationally useful

## QG-08: Controlled QA Safety

- Applies to: Phase 07 QA release candidate
- Required evidence:
  - evidence-pack assembly is inspectable
  - support states are explicit
  - abstention works
  - citation links navigate to highlighted evidence
  - restricted context never enters unauthorized prompts or outputs
- Failure mode:
  - QA becomes a rumor or hallucination surface

## QG-09: Production Readiness

- Applies to: restricted pilot and production milestones
- Required evidence:
  - SLO dashboards and alerting exist
  - backup and recovery procedures are proven
  - release rollback path exists
  - security, policy, and export rules are signed off
  - operational runbooks exist for major failure classes
- Failure mode:
  - unstable or unsafe release

## Gate Ownership Model

- QG-01: architecture lead and program manager
- QG-02: platform lead
- QG-03: data plane lead
- QG-04: policy/security lead
- QG-05: semantics lead
- QG-06: retrieval/analytics lead
- QG-07: application lead
- QG-08: application lead and policy/security lead
- QG-09: release lead with cross-functional signoff

## Exception Rule

If a gate exception is requested, the exception must identify:

- the specific missing evidence
- the risk introduced by bypassing the gate
- the containment plan
- the rollback condition that would trigger reversal

This exception rule does not apply to the universal test-pass and coverage gate
in `D-010`.
