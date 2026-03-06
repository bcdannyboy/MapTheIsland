"""Executable Phase 01 baseline for shared policy vocabulary and matrices."""

from __future__ import annotations

from enum import StrEnum

from maptheisland_schemas import SensitivityLevel
from pydantic import BaseModel, ConfigDict, Field


class PolicyBaseModel(BaseModel):
    """Shared Pydantic configuration for policy vocabulary models."""

    model_config = ConfigDict(extra="forbid", frozen=True, protected_namespaces=())


class ActorRole(StrEnum):
    """Provisional actor roles from the published deny-by-default baseline."""

    STANDARD_ANALYST = "standard_analyst"
    RESTRICTED_ANALYST = "restricted_analyst"
    REVIEW_OPERATOR = "review_operator"
    POLICY_SECURITY_ADMIN = "policy_security_admin"
    RELEASE_EVALUATOR = "release_evaluator"
    SERVICE_ACCOUNT = "service_account"


class AccessDisposition(StrEnum):
    """Normalized access dispositions used by the Phase 01 policy baseline."""

    ALLOWED = "allowed"
    DENIED = "denied"
    MASKED_ONLY = "masked_only"
    METADATA_ONLY = "metadata_only"
    RESTRICTED_ROLE_ONLY = "restricted_role_only"
    EXPLICIT_APPROVAL_REQUIRED = "explicit_approval_required"
    POLICY_SAFE_ONLY = "policy_safe_only"
    ASSIGNED_QUEUE_ONLY = "assigned_queue_only"
    LIMITED_WORKFLOW_ONLY = "limited_workflow_only"
    AUDITED_PURPOSE_REQUIRED = "audited_purpose_required"
    EVALUATION_APPROVED_ONLY = "evaluation_approved_only"
    SERVICE_OWNED_ONLY = "service_owned_only"
    NOT_APPLICABLE = "not_applicable"


class SensitivityHandlingRule(PolicyBaseModel):
    """Policy surface expectations for one sensitivity classification."""

    sensitivity: SensitivityLevel
    meaning: str = Field(min_length=1)
    broad_analyst_search: AccessDisposition
    restricted_analyst_view: AccessDisposition
    qa_prompt_eligibility: AccessDisposition
    export_eligibility: AccessDisposition
    notes: str = Field(min_length=1)


class RoleCapabilityRule(PolicyBaseModel):
    """Allow or deny baseline for one actor role across major policy surfaces."""

    role: ActorRole
    public_evidence_view: AccessDisposition
    restricted_context_view: AccessDisposition
    review_actions: AccessDisposition
    sensitive_label_approval: AccessDisposition
    raw_span_export: AccessDisposition
    derived_summary_export: AccessDisposition
    controlled_qa: AccessDisposition
    notes: str = Field(min_length=1)


class ProhibitedFlow(PolicyBaseModel):
    """Named prohibited flow that must eventually become a negative test."""

    code: str = Field(pattern=r"^PF-\d{3}$")
    description: str = Field(min_length=1)


SENSITIVITY_RULES: dict[SensitivityLevel, SensitivityHandlingRule] = {
    SensitivityLevel.PUBLIC_GENERAL: SensitivityHandlingRule(
        sensitivity=SensitivityLevel.PUBLIC_GENERAL,
        meaning="public evidence without extra handling constraints beyond normal provenance",
        broad_analyst_search=AccessDisposition.ALLOWED,
        restricted_analyst_view=AccessDisposition.ALLOWED,
        qa_prompt_eligibility=AccessDisposition.ALLOWED,
        export_eligibility=AccessDisposition.ALLOWED,
        notes="Derived and raw export remain route-policy governed rather than implicitly open.",
    ),
    SensitivityLevel.PUBLIC_EXPLICIT_REDACTED: SensitivityHandlingRule(
        sensitivity=SensitivityLevel.PUBLIC_EXPLICIT_REDACTED,
        meaning="public evidence that visibly contains official redactions",
        broad_analyst_search=AccessDisposition.ALLOWED,
        restricted_analyst_view=AccessDisposition.ALLOWED,
        qa_prompt_eligibility=AccessDisposition.MASKED_ONLY,
        export_eligibility=AccessDisposition.EXPLICIT_APPROVAL_REQUIRED,
        notes="Search and view are allowed, but prompt and export paths remain redaction-aware.",
    ),
    SensitivityLevel.RESTRICTED_REDACTION_CONTEXT: SensitivityHandlingRule(
        sensitivity=SensitivityLevel.RESTRICTED_REDACTION_CONTEXT,
        meaning="redaction-adjacent context that could materially increase deanonymization risk",
        broad_analyst_search=AccessDisposition.DENIED,
        restricted_analyst_view=AccessDisposition.RESTRICTED_ROLE_ONLY,
        qa_prompt_eligibility=AccessDisposition.DENIED,
        export_eligibility=AccessDisposition.DENIED,
        notes="Restricted-role access requires explicit purpose and must remain deny-by-default.",
    ),
    SensitivityLevel.PROTECTED_VICTIM_CONTEXT: SensitivityHandlingRule(
        sensitivity=SensitivityLevel.PROTECTED_VICTIM_CONTEXT,
        meaning="content that could reveal or materially narrow protected identity",
        broad_analyst_search=AccessDisposition.DENIED,
        restricted_analyst_view=AccessDisposition.DENIED,
        qa_prompt_eligibility=AccessDisposition.DENIED,
        export_eligibility=AccessDisposition.DENIED,
        notes="No later surface may assume governance approval that does not yet exist.",
    ),
    SensitivityLevel.WITHHELD_SOURCE_GAP: SensitivityHandlingRule(
        sensitivity=SensitivityLevel.WITHHELD_SOURCE_GAP,
        meaning=(
            "structured indication that expected evidence is absent or intentionally "
            "unavailable"
        ),
        broad_analyst_search=AccessDisposition.METADATA_ONLY,
        restricted_analyst_view=AccessDisposition.METADATA_ONLY,
        qa_prompt_eligibility=AccessDisposition.METADATA_ONLY,
        export_eligibility=AccessDisposition.METADATA_ONLY,
        notes="Gap markers may describe absence but may not masquerade as substitute evidence.",
    ),
    SensitivityLevel.UNSAFE_FOR_LLM: SensitivityHandlingRule(
        sensitivity=SensitivityLevel.UNSAFE_FOR_LLM,
        meaning="content that must not enter synthesis, judging, or answer-generation prompts",
        broad_analyst_search=AccessDisposition.DENIED,
        restricted_analyst_view=AccessDisposition.RESTRICTED_ROLE_ONLY,
        qa_prompt_eligibility=AccessDisposition.DENIED,
        export_eligibility=AccessDisposition.EXPLICIT_APPROVAL_REQUIRED,
        notes=(
            "View eligibility may differ from prompt eligibility, but QA remains "
            "denied by default."
        ),
    ),
}

ROLE_CAPABILITY_RULES: dict[ActorRole, RoleCapabilityRule] = {
    ActorRole.STANDARD_ANALYST: RoleCapabilityRule(
        role=ActorRole.STANDARD_ANALYST,
        public_evidence_view=AccessDisposition.ALLOWED,
        restricted_context_view=AccessDisposition.DENIED,
        review_actions=AccessDisposition.DENIED,
        sensitive_label_approval=AccessDisposition.DENIED,
        raw_span_export=AccessDisposition.EXPLICIT_APPROVAL_REQUIRED,
        derived_summary_export=AccessDisposition.POLICY_SAFE_ONLY,
        controlled_qa=AccessDisposition.POLICY_SAFE_ONLY,
        notes=(
            "This role is the broad-access baseline and never implies restricted "
            "export authority."
        ),
    ),
    ActorRole.RESTRICTED_ANALYST: RoleCapabilityRule(
        role=ActorRole.RESTRICTED_ANALYST,
        public_evidence_view=AccessDisposition.ALLOWED,
        restricted_context_view=AccessDisposition.RESTRICTED_ROLE_ONLY,
        review_actions=AccessDisposition.DENIED,
        sensitive_label_approval=AccessDisposition.DENIED,
        raw_span_export=AccessDisposition.DENIED,
        derived_summary_export=AccessDisposition.EXPLICIT_APPROVAL_REQUIRED,
        controlled_qa=AccessDisposition.POLICY_SAFE_ONLY,
        notes="Restricted view does not widen export authority or review authority by default.",
    ),
    ActorRole.REVIEW_OPERATOR: RoleCapabilityRule(
        role=ActorRole.REVIEW_OPERATOR,
        public_evidence_view=AccessDisposition.ALLOWED,
        restricted_context_view=AccessDisposition.ASSIGNED_QUEUE_ONLY,
        review_actions=AccessDisposition.ALLOWED,
        sensitive_label_approval=AccessDisposition.LIMITED_WORKFLOW_ONLY,
        raw_span_export=AccessDisposition.DENIED,
        derived_summary_export=AccessDisposition.LIMITED_WORKFLOW_ONLY,
        controlled_qa=AccessDisposition.LIMITED_WORKFLOW_ONLY,
        notes="Queue-specific operational authority is not a blanket restricted-data role.",
    ),
    ActorRole.POLICY_SECURITY_ADMIN: RoleCapabilityRule(
        role=ActorRole.POLICY_SECURITY_ADMIN,
        public_evidence_view=AccessDisposition.ALLOWED,
        restricted_context_view=AccessDisposition.ALLOWED,
        review_actions=AccessDisposition.ALLOWED,
        sensitive_label_approval=AccessDisposition.ALLOWED,
        raw_span_export=AccessDisposition.AUDITED_PURPOSE_REQUIRED,
        derived_summary_export=AccessDisposition.AUDITED_PURPOSE_REQUIRED,
        controlled_qa=AccessDisposition.AUDITED_PURPOSE_REQUIRED,
        notes="Sensitive access for this role remains auditable and purpose-bound.",
    ),
    ActorRole.RELEASE_EVALUATOR: RoleCapabilityRule(
        role=ActorRole.RELEASE_EVALUATOR,
        public_evidence_view=AccessDisposition.ALLOWED,
        restricted_context_view=AccessDisposition.EVALUATION_APPROVED_ONLY,
        review_actions=AccessDisposition.DENIED,
        sensitive_label_approval=AccessDisposition.DENIED,
        raw_span_export=AccessDisposition.EVALUATION_APPROVED_ONLY,
        derived_summary_export=AccessDisposition.EVALUATION_APPROVED_ONLY,
        controlled_qa=AccessDisposition.EVALUATION_APPROVED_ONLY,
        notes="Evaluation access is narrow and tied to approved fixtures or evidence packs.",
    ),
    ActorRole.SERVICE_ACCOUNT: RoleCapabilityRule(
        role=ActorRole.SERVICE_ACCOUNT,
        public_evidence_view=AccessDisposition.SERVICE_OWNED_ONLY,
        restricted_context_view=AccessDisposition.SERVICE_OWNED_ONLY,
        review_actions=AccessDisposition.NOT_APPLICABLE,
        sensitive_label_approval=AccessDisposition.NOT_APPLICABLE,
        raw_span_export=AccessDisposition.NOT_APPLICABLE,
        derived_summary_export=AccessDisposition.NOT_APPLICABLE,
        controlled_qa=AccessDisposition.SERVICE_OWNED_ONLY,
        notes=(
            "Service accounts only receive the minimum rights required by the "
            "owning service path."
        ),
    ),
}

PROHIBITED_FLOWS: tuple[ProhibitedFlow, ...] = (
    ProhibitedFlow(
        code="PF-001",
        description="sending restricted_redaction_context into broad search indexing",
    ),
    ProhibitedFlow(
        code="PF-002",
        description="sending protected_victim_context into model prompts",
    ),
    ProhibitedFlow(
        code="PF-003",
        description="sending unsafe_for_llm spans into QA, summarization, or judge prompts",
    ),
    ProhibitedFlow(
        code="PF-004",
        description="exposing raw redaction-adjacent neighborhoods to standard analysts",
    ),
    ProhibitedFlow(
        code="PF-005",
        description="allowing the browser to infer or widen policy context client-side",
    ),
    ProhibitedFlow(
        code="PF-006",
        description=(
            "treating denied export requests as hidden UI controls without server "
            "enforcement"
        ),
    ),
    ProhibitedFlow(
        code="PF-007",
        description="emitting person-level risk scores or accusatory labels",
    ),
    ProhibitedFlow(
        code="PF-008",
        description=(
            "collapsing evidence-backed relationships and inferred relationships "
            "into one analyst-visible class by default"
        ),
    ),
    ProhibitedFlow(
        code="PF-009",
        description="auto-merging high-impact identity candidates without a review artifact",
    ),
    ProhibitedFlow(
        code="PF-010",
        description=(
            "returning unsupported QA narratives when the support state is "
            "insufficient_support"
        ),
    ),
)


def get_sensitivity_rule(level: SensitivityLevel) -> SensitivityHandlingRule:
    """Return the published handling rule for a sensitivity value."""
    return SENSITIVITY_RULES[level]


def get_role_capability(role: ActorRole) -> RoleCapabilityRule:
    """Return the deny-by-default baseline capability rule for one actor role."""
    return ROLE_CAPABILITY_RULES[role]
