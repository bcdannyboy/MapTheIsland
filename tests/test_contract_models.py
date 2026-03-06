"""Coverage-complete tests for the Phase 01 executable contract baseline."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from maptheisland_contracts import (
    SERVICE_BOUNDARIES,
    IntegrationEventEnvelope,
    IntegrationEventType,
    OperationalEndpointPath,
    ServiceName,
    get_service_boundary,
)
from pydantic import ValidationError


def test_contract_package_exports_service_catalog_and_operational_paths() -> None:
    """The contract package should publish stable service and ops identifiers."""
    assert ServiceName.BFF.value == "bff"
    assert OperationalEndpointPath.HEALTH_READY.value == "/health/ready"
    assert len(SERVICE_BOUNDARIES) == len(ServiceName)


def test_service_boundary_registry_tracks_phase_and_owner_role() -> None:
    """Reserved services must stay explicitly tied to phase and owner intent."""
    review_api = get_service_boundary(ServiceName.REVIEW_API)
    bff = get_service_boundary(ServiceName.BFF)

    assert review_api.first_delivery_phase == "P03"
    assert review_api.primary_owner_role == "review operations lead"
    assert "policy-aware" in bff.primary_responsibility


def test_event_envelope_accepts_optional_lineage_hooks_and_metadata() -> None:
    """Event envelopes carry cross-service audit and replay context."""
    envelope = IntegrationEventEnvelope(
        event_id="event-001",
        event_type=IntegrationEventType.CANONICAL_ASSETS_MATERIALIZED,
        schema_version="1.0.0",
        occurred_at=datetime(2026, 3, 6, 15, 0, tzinfo=UTC),
        producer=ServiceName.DOCPROC,
        subject_type="document",
        subject_id="doc-001",
        trace_id="trace-001",
        causation_id="event-000",
        lakefs_commit="commit-001",
        iceberg_snapshot_id="snapshot-001",
        metadata={"page_count": 12},
    )

    assert envelope.event_type is IntegrationEventType.CANONICAL_ASSETS_MATERIALIZED
    assert envelope.metadata == {"page_count": 12}
    assert envelope.lakefs_commit == "commit-001"


def test_event_envelope_rejects_blank_required_identifiers() -> None:
    """Blank required identifiers would make replay and traceability ambiguous."""
    with pytest.raises(ValidationError, match="String should have at least 1 character"):
        IntegrationEventEnvelope(
            event_id="",
            event_type=IntegrationEventType.FILE_DOWNLOADED,
            schema_version="1.0.0",
            occurred_at=datetime(2026, 3, 6, 15, 5, tzinfo=UTC),
            producer=ServiceName.HARVESTER,
            subject_type="raw_object",
            subject_id="object-001",
            trace_id="trace-002",
        )
