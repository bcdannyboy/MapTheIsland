"""Executable service-boundary registry for reserved platform services."""

from __future__ import annotations

from enum import StrEnum

from pydantic import Field

from .common import ContractBaseModel


class ServiceName(StrEnum):
    """Canonical service identifiers from the Phase 00 service catalog."""

    HARVESTER = "harvester"
    DOCPROC = "docproc"
    OCR = "ocr"
    EXTRACTOR = "extractor"
    RESOLVER = "resolver"
    TOPICS = "topics"
    GRAPH_BUILDER = "graph-builder"
    INDEXER = "indexer"
    REVIEW_API = "review-api"
    QA_ORCHESTRATOR = "qa-orchestrator"
    BFF = "bff"


class ServiceBoundary(ContractBaseModel):
    """Minimal executable record of a reserved service boundary."""

    service: ServiceName
    primary_owner_role: str = Field(min_length=1)
    first_delivery_phase: str = Field(min_length=1)
    primary_responsibility: str = Field(min_length=1)


SERVICE_BOUNDARIES: dict[ServiceName, ServiceBoundary] = {
    ServiceName.HARVESTER: ServiceBoundary(
        service=ServiceName.HARVESTER,
        primary_owner_role="document processing lead",
        first_delivery_phase="P02",
        primary_responsibility="discover official DOJ sources and create raw ingest work",
    ),
    ServiceName.DOCPROC: ServiceBoundary(
        service=ServiceName.DOCPROC,
        primary_owner_role="document processing lead",
        first_delivery_phase="P02",
        primary_responsibility=(
            "classify files, parse PDFs, extract layout, and coordinate canonical "
            "evidence materialization"
        ),
    ),
    ServiceName.OCR: ServiceBoundary(
        service=ServiceName.OCR,
        primary_owner_role="document processing lead",
        first_delivery_phase="P02",
        primary_responsibility="execute OCR fallback lanes and emit OCR-confidence outcomes",
    ),
    ServiceName.EXTRACTOR: ServiceBoundary(
        service=ServiceName.EXTRACTOR,
        primary_owner_role="semantics or NLP lead",
        first_delivery_phase="P04",
        primary_responsibility=(
            "extract claims, entities, aliases, relations, redaction objects, "
            "and event candidates from accepted spans"
        ),
    ),
    ServiceName.RESOLVER: ServiceBoundary(
        service=ServiceName.RESOLVER,
        primary_owner_role="semantics or NLP lead",
        first_delivery_phase="P04",
        primary_responsibility="perform identity resolution and prepare merge-review candidates",
    ),
    ServiceName.TOPICS: ServiceBoundary(
        service=ServiceName.TOPICS,
        primary_owner_role="retrieval, graph, and analytics lead",
        first_delivery_phase="P05",
        primary_responsibility="materialize topic, sense, and weak-label research artifacts",
    ),
    ServiceName.GRAPH_BUILDER: ServiceBoundary(
        service=ServiceName.GRAPH_BUILDER,
        primary_owner_role="retrieval, graph, and analytics lead",
        first_delivery_phase="P05",
        primary_responsibility="build event-centric graph projections and bounded graph assets",
    ),
    ServiceName.INDEXER: ServiceBoundary(
        service=ServiceName.INDEXER,
        primary_owner_role="retrieval, graph, and analytics lead",
        first_delivery_phase="P05",
        primary_responsibility=(
            "materialize retrieval artifacts from accepted evidence and semantics"
        ),
    ),
    ServiceName.REVIEW_API: ServiceBoundary(
        service=ServiceName.REVIEW_API,
        primary_owner_role="review operations lead",
        first_delivery_phase="P03",
        primary_responsibility="own review queues, adjudications, and review-driven invalidation",
    ),
    ServiceName.QA_ORCHESTRATOR: ServiceBoundary(
        service=ServiceName.QA_ORCHESTRATOR,
        primary_owner_role="BFF and API lead with policy/security co-review",
        first_delivery_phase="P07",
        primary_responsibility=(
            "assemble evidence packs, enforce support verification, apply abstention, "
            "and mediate model-gateway calls"
        ),
    ),
    ServiceName.BFF: ServiceBoundary(
        service=ServiceName.BFF,
        primary_owner_role="BFF and API lead",
        first_delivery_phase="P06",
        primary_responsibility=(
            "mediate analyst requests to trusted backends and return policy-aware, "
            "provenance-aware response envelopes"
        ),
    ),
}


def get_service_boundary(service: ServiceName) -> ServiceBoundary:
    """Return the executable boundary record for a reserved service."""
    return SERVICE_BOUNDARIES[service]
