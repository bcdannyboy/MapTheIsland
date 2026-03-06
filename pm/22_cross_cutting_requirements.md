# Cross-Cutting Requirements

These requirements apply across phases and workstreams. A task can be locally complete and still fail the program if it violates one of these rules.

## CCR-01 Provenance Completeness

- Every stored analytical object must retain traceability to source evidence.
- No user-facing output may require reverse engineering to understand where it came from.
- New artifact classes must be added to [`14_artifact_inventory.md`](./14_artifact_inventory.md).

## CCR-02 Policy Before Promotion

- Sensitive content must be classified before broad indexing, summarization, embedding, or QA use.
- A feature may compute on restricted content only when its output path is explicitly policy-bounded.
- Promotion rules must exist before rollout.

## CCR-03 Evidence And Inference Separation

- Evidence, extracted claims, hypotheses, and user-facing summaries must remain distinguishable in storage, APIs, UI, and exports.
- No workflow may visually or semantically collapse evidence-backed and inferred relationships into one class by default.

## CCR-04 Reviewability

- High-impact automation must create reviewable objects, not hidden side effects.
- Review queues, audit events, and rollback or correction paths must exist before a risky workflow is considered production-ready.

## CCR-05 Operational Reproducibility

- Infra, services, and derived-asset generation must be reproducible from code and tracked configuration.
- Manual recovery actions must result in follow-up automation or runbook documentation.

## CCR-06 Observability Minimums

- Every major pipeline and user-facing surface must expose success, failure, latency, and queue-health signals.
- If a workflow cannot be observed, it is not release-ready.

## CCR-07 Security And Least Privilege

- Human access, service access, and browser access are separate concerns.
- Trusted-write and filtered-read boundaries must be explicit.
- Export permissions are stricter than view permissions.

## CCR-08 Data Lifecycle Discipline

- Raw evidence is immutable.
- Derived artifacts are versioned and replaceable through rematerialization.
- Failed or superseded outputs must be quarantined or retired explicitly, not silently overwritten.

## CCR-09 Performance And Scale Awareness

- Interactive surfaces must use bounded queries, server-side aggregation, or precomputed assets.
- Features must record likely bottlenecks or scaling assumptions before rollout.

## CCR-10 Reliability And Recovery

- Backup, restore, replay, and rollback expectations must be defined for each major store and promoted workflow.
- Recovery procedures are release blockers for pilot and production milestones.

## CCR-11 Cost And Capacity Visibility

- GPU-heavy, OCR-heavy, embedding-heavy, and stateful workflows must expose capacity assumptions and cost implications.
- Material cost changes become explicit decision inputs.

## CCR-12 Accessibility And Analyst Usability

- Keyboard-heavy review flows, readable uncertainty cues, and non-ambiguous state labels are required product behavior, not optional polish.

## CCR-13 Documentation As Operational Infrastructure

- PM docs, implementation specs, runbooks, and research registers are part of delivery.
- If work changes behavior, scope, dependencies, or operating procedure, the corresponding documents change in the same session.

## CCR-14 External Decision Transparency

- Unresolved deployment, governance, staffing, or budget questions must remain visible.
- No task may hide an external blocker by inventing a local assumption.

## CCR-15 Testing And Evaluation As Product Requirements

- Deterministic code paths require tests and may not remain partially covered.
- Model-assisted paths require tests plus evaluation data and thresholds.
- UI flows require route and end-to-end validation proportional to their risk.
- Handwritten code across the repository must remain at 100 percent coverage.
- Task, phase, and milestone completion all require 100 percent local and integration test pass rates.

## CCR-16 Environment And Promotion Discipline

- Code, schemas, migrations, data branches, and release promotion each require explicit environment rules.
- Temporary shortcuts across environments are prohibited unless documented as emergency procedure.

## CCR-17 Release Governance

- Release decisions depend on quality gates, phase exit evidence, unresolved-risk tolerance, and signoffs.
- Scope changes that affect release boundaries must update the dashboard, dependency map, and release package requirements before implementation continues.
