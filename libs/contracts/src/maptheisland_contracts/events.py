"""Executable async event contract baseline for cross-service integration."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import Field

from .common import ContractBaseModel
from .services import ServiceName


class IntegrationEventType(StrEnum):
    """Canonical event types published in the Phase 00 event inventory."""

    SOURCE_DISCOVERED = "source.discovered"
    FILE_DOWNLOADED = "file.downloaded"
    FILE_ROUTED = "file.routed"
    FILE_PARSED = "file.parsed"
    OCR_COMPLETED = "ocr.completed"
    CANONICAL_ASSETS_MATERIALIZED = "canonical.assets.materialized"
    CLAIMS_EXTRACTED = "claims.extracted"
    ENTITY_MERGE_PROPOSED = "entity.merge.proposed"
    ADJUDICATION_ACCEPTED = "adjudication.accepted"
    ADJUDICATION_REJECTED = "adjudication.rejected"
    INDEX_REFRESHED = "index.refreshed"
    GRAPH_PROJECTION_REBUILT = "graph.projection.rebuilt"
    TOPICS_MATERIALIZED = "topics.materialized"
    QA_ANSWER_RECORDED = "qa.answer.recorded"
    QA_ABSTAINED = "qa.abstained"


class IntegrationEventEnvelope(ContractBaseModel):
    """Minimum required metadata shared by every integration event."""

    event_id: str = Field(min_length=1)
    event_type: IntegrationEventType
    schema_version: str = Field(min_length=1)
    occurred_at: datetime
    producer: ServiceName
    subject_type: str = Field(min_length=1)
    subject_id: str = Field(min_length=1)
    trace_id: str = Field(min_length=1)
    causation_id: str | None = None
    lakefs_commit: str | None = None
    iceberg_snapshot_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
