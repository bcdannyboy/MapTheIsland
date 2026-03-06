"""Shared contract primitives for MapTheIsland cross-boundary payloads.

Phase 00 published the human-readable contract baseline. Phase 01 begins the
executable contract layer so later services, review flows, and orchestration
code do not recreate event and operational boundary semantics from memory.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class ContractBaseModel(BaseModel):
    """Shared Pydantic configuration for executable contract models."""

    model_config = ConfigDict(extra="forbid", frozen=True, protected_namespaces=())


class OperationalEndpointPath(StrEnum):
    """Required operational endpoints for long-lived runtime services."""

    HEALTH_LIVE = "/health/live"
    HEALTH_READY = "/health/ready"
    METRICS = "/metrics"
    VERSION = "/version"
    OPENAPI = "/openapi.json"
