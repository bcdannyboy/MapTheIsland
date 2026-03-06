# Policy Taxonomy And Safety Model

## Purpose

This document is the detailed `P00-T03` policy baseline for span sensitivity,
restricted-context handling, role intent, export strictness, prohibited flows,
and policy-verification expectations.

The architecture makes policy a precondition for higher-level NLP and analyst
surfaces. This baseline therefore fixes what later Phase 03, Phase 06, and
Phase 07 implementation must treat as non-negotiable.

## Governing Safety Rules

- Redactions are not puzzles to solve.
- Restricted evidence may exist in storage without being broadly exposed.
- View permissions and export permissions are separate, with export stricter.
- Model prompts may only receive content that is explicitly allowed for that
  model-assisted path.
- High-impact actions require reviewable artifacts and human adjudication.
- QA must abstain when policy or support-state rules require it.

## Sensitivity Taxonomy

The executable enum in `libs/schemas` is the authoritative value set. The table
below fixes the implementation meaning of each value:

| Sensitivity Value | Meaning | Broad Analyst Search | Restricted Analyst View | QA Prompt Eligibility | Export Eligibility |
| --- | --- | --- | --- | --- | --- |
| `public_general` | public evidence without extra handling constraints beyond normal provenance and review semantics | allowed | allowed | allowed | derived and raw export allowed when route policy permits |
| `public_explicit_redacted` | public evidence that visibly contains official redactions and therefore carries handling sensitivity even though the artifact is public | allowed with redaction-aware rendering | allowed | allowed only with masked-adjacency rules | raw export only if redaction policy permits |
| `restricted_redaction_context` | contextual neighborhood around a redaction that could materially increase deanonymization risk | denied | allowed only to restricted roles with explicit reason | denied by default | denied by default |
| `protected_victim_context` | content that could reveal or materially narrow protected victim identity or other protected sensitive context | denied | denied unless a future governance path explicitly allows it | denied | denied |
| `withheld_source_gap` | a structured indication that expected evidence is absent, withheld, or intentionally unavailable | allowed as a gap marker only | allowed | allowed as metadata only, not as substitute evidence | allowed only as metadata |
| `unsafe_for_llm` | content that must not enter synthesis, judging, or answer-generation prompts under normal operations | denied from broad QA and summarization paths | view rules determined separately | denied | export rules depend on the underlying sensitivity and role |

## Restricted-Context Cases

The following cases must be treated as restricted even when the surrounding
document is public:

- redaction-adjacent textual neighborhoods
- victim-sensitive name, contact, or location contexts
- protected span combinations that increase deanonymization risk when joined
- raw export bundles that are broader than the analyst-facing rendered view
- QA evidence packs that would reveal withheld or unsafe-for-LLM content

## Provisional Role And Capability Matrix

`OQ-03` remains unresolved, so the following matrix defines implementation
intent only. It is a deny-by-default baseline, not a final governance approval.

| Capability Class | Public Evidence View | Restricted Context View | Review Actions | Sensitive Label Approval | Raw Span Export | Derived Summary Export | Controlled QA |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `standard_analyst` | allowed | denied | denied | denied | denied unless explicitly route-approved | allowed for policy-safe outputs | allowed only on policy-safe evidence |
| `restricted_analyst` | allowed | allowed for explicitly granted restricted surfaces | denied unless also review-enabled | denied | denied by default | allowed only for policy-approved outputs | allowed only if prompts remain policy-safe |
| `review_operator` | allowed | allowed for assigned queue items | allowed | limited to queue-specific decisions | denied outside review evidence packages | denied unless workflow explicitly authorizes | denied unless queue requires QA review |
| `policy_security_admin` | allowed | allowed | allowed | allowed | allowed only with audit and explicit purpose | allowed with audit | allowed for validation and policy review |
| `release_evaluator` | allowed | allowed only for evaluation-approved fixtures and evidence packs | denied | denied | denied unless explicitly approved evaluation artifact | allowed for evaluation reports | allowed for controlled regression suites |
| `service_account` | only what the owning service requires | only what the owning service requires | not applicable | not applicable | not applicable | not applicable | only within approved server-side paths |

## Export Strictness Rules

- Export permission is never implied by view permission.
- Raw supporting spans require stricter approval than rendered summaries.
- Restricted-context exports default to denied.
- QA answers may be exportable only if their evidence pack, citations, and
  support state remain within policy.
- Signed URLs for permitted exports must be short-lived and scope-limited.

## Prohibited Flows

The following flows are explicitly prohibited and must later become negative
tests:

- sending `restricted_redaction_context` into broad search indexing
- sending `protected_victim_context` into model prompts
- sending `unsafe_for_llm` spans into QA, summarization, or judge prompts
- exposing raw redaction-adjacent neighborhoods to standard analysts
- allowing the browser to infer or widen policy context client-side
- treating denied export requests as merely hidden UI controls without server
  enforcement
- emitting person-level risk scores or accusatory labels
- collapsing evidence-backed relationships and inferred relationships into one
  analyst-visible class by default
- auto-merging high-impact identity candidates without a review artifact
- returning unsupported QA narratives when the support state is
  `insufficient_support`

## Policy Verification Matrix

| Policy Requirement | Control Point | Minimum Verification Obligation | First Implementing Phase |
| --- | --- | --- | --- |
| sensitivity classification before broad promotion | span-level sensitivity pipeline | positive and negative tests for every enum value and deny path | `P03-T01` |
| restricted contexts excluded from general search | indexer and BFF search filters | integration tests proving denied spans do not appear in standard search results | `P03-T01`, `P05-T01`, `P06-T03` |
| export stricter than view | BFF export routes and policy engine | tests for allowed view plus denied raw export combinations | `P03-T03`, `P06-T01` |
| redaction context protected from deanonymization-adjacent rendering | document viewer and redaction analytics routes | UI and integration tests for summarized versus hidden context by role | `P03-T03`, `P06-T04`, `P07-T03` |
| high-impact merges require review | resolver plus review-api | tests that merge proposals create review items and cannot self-promote | `P03-T04`, `P04-T02` |
| QA prompt safety and abstention | qa-orchestrator and BFF | tests for prompt filtering, support states, abstention, and denied prompt inputs | `P07-T01`, `P07-T02` |
| audit coverage for sensitive actions | review, export, QA, admin paths | integration tests plus audit-record assertions | `P03-T05`, `P07-T04` |

## Open Governance Note

`OQ-03` still blocks final governance approval for restricted-role assignments
and export authorities. Until that is resolved:

- all restricted surfaces remain deny-by-default
- implementation may proceed with internal-only scaffolding
- release or pilot claims must not assume governance approval exists

## References

- `Architecture_Plan.md`, sections 1, 9, 13, 16, and Part II sections 11, 12,
  and 16
- `pm/01_architecture_constraints.md`
- `pm/16_decision_boundaries.md`
- `libs/schemas/src/maptheisland_schemas/evidence.py`
