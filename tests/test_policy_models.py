"""Coverage-complete tests for the Phase 01 executable policy baseline."""

from __future__ import annotations

import pytest
from maptheisland_policy import (
    PROHIBITED_FLOWS,
    AccessDisposition,
    ActorRole,
    ProhibitedFlow,
    SensitivityLevel,
    get_role_capability,
    get_sensitivity_rule,
)
from pydantic import ValidationError


def test_policy_package_exports_deny_by_default_role_and_sensitivity_rules() -> None:
    """The policy package should publish stable shared vocabulary."""
    assert ActorRole.POLICY_SECURITY_ADMIN.value == "policy_security_admin"
    assert SensitivityLevel.UNSAFE_FOR_LLM.value == "unsafe_for_llm"


def test_sensitivity_rule_lookup_preserves_public_and_restricted_handling() -> None:
    """Sensitivity handling must remain explicit across search, QA, and export."""
    public_rule = get_sensitivity_rule(SensitivityLevel.PUBLIC_GENERAL)
    restricted_rule = get_sensitivity_rule(SensitivityLevel.RESTRICTED_REDACTION_CONTEXT)
    gap_rule = get_sensitivity_rule(SensitivityLevel.WITHHELD_SOURCE_GAP)

    assert public_rule.export_eligibility is AccessDisposition.ALLOWED
    assert restricted_rule.restricted_analyst_view is AccessDisposition.RESTRICTED_ROLE_ONLY
    assert gap_rule.qa_prompt_eligibility is AccessDisposition.METADATA_ONLY


def test_role_capability_lookup_preserves_queue_and_audit_constraints() -> None:
    """Role baselines should encode review, export, and QA differences clearly."""
    review_operator = get_role_capability(ActorRole.REVIEW_OPERATOR)
    service_account = get_role_capability(ActorRole.SERVICE_ACCOUNT)
    evaluator = get_role_capability(ActorRole.RELEASE_EVALUATOR)

    assert review_operator.review_actions is AccessDisposition.ALLOWED
    assert review_operator.restricted_context_view is AccessDisposition.ASSIGNED_QUEUE_ONLY
    assert service_account.review_actions is AccessDisposition.NOT_APPLICABLE
    assert evaluator.controlled_qa is AccessDisposition.EVALUATION_APPROVED_ONLY


def test_prohibited_flows_registry_is_stable_and_validated() -> None:
    """Prohibited flows are named policy commitments, not implied guidance."""
    codes = [flow.code for flow in PROHIBITED_FLOWS]

    assert codes == [f"PF-{index:03d}" for index in range(1, 11)]
    assert PROHIBITED_FLOWS[2].description.startswith("sending unsafe_for_llm")

    with pytest.raises(ValidationError, match="String should match pattern"):
        ProhibitedFlow(code="INVALID", description="bad code")
