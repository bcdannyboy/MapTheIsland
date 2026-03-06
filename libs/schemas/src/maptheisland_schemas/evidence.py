"""Canonical evidence models for the MapTheIsland Phase 00 baseline.

The architecture makes the evidence-backed span the primary truth object and
requires provenance to be carried by every derived artifact. These models are
the first executable version of that rule. They are intentionally strict so
later services inherit explicit validation behavior rather than informal
conventions.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field, field_validator, model_validator


def normalize_sha256(value: str) -> str:
    """Return a normalized SHA-256 digest or raise for invalid input."""
    lowered = value.lower()
    if len(lowered) != 64 or any(character not in "0123456789abcdef" for character in lowered):
        msg = "sha256 must be a 64-character hexadecimal digest"
        raise ValueError(msg)
    return lowered


class SensitivityLevel(StrEnum):
    """Supported span and artifact sensitivity states."""

    PUBLIC_GENERAL = "public_general"
    PUBLIC_EXPLICIT_REDACTED = "public_explicit_redacted"
    RESTRICTED_REDACTION_CONTEXT = "restricted_redaction_context"
    PROTECTED_VICTIM_CONTEXT = "protected_victim_context"
    WITHHELD_SOURCE_GAP = "withheld_source_gap"
    UNSAFE_FOR_LLM = "unsafe_for_llm"


class ReviewState(StrEnum):
    """Normalized review lifecycle states shared across evidence artifacts."""

    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    DEFERRED = "deferred"
    NEEDS_HUMAN_REVIEW = "needs_human_review"
    SUPERSEDED = "superseded"


class ExtractionEngineIdentity(StrEnum):
    """Known engine identifiers used by text and layout extraction lanes."""

    PYPDF = "pypdf"
    PYMUPDF = "pymupdf"
    UNSTRUCTURED = "unstructured"
    TESSERACT = "tesseract"
    DOCTR = "doctr"
    TROCR = "trocr"


class MapTheIslandBaseModel(BaseModel):
    """Shared model configuration for Phase 00 schema types."""

    model_config = ConfigDict(extra="forbid", frozen=True, protected_namespaces=())


class BoundingBox(MapTheIslandBaseModel):
    """Page-relative rectangular geometry for a span."""

    x_min: float = Field(ge=0.0, description="Left coordinate in page space.")
    y_min: float = Field(ge=0.0, description="Top coordinate in page space.")
    x_max: float = Field(ge=0.0, description="Right coordinate in page space.")
    y_max: float = Field(ge=0.0, description="Bottom coordinate in page space.")

    @model_validator(mode="after")
    def validate_order(self) -> BoundingBox:
        """Reject degenerate or inverted boxes.

        The viewer and layout-aware extraction code both require strictly
        increasing coordinates. Allowing zero-area or inverted boxes would make
        downstream highlighting ambiguous.
        """
        if self.x_max <= self.x_min:
            msg = "x_max must be greater than x_min"
            raise ValueError(msg)
        if self.y_max <= self.y_min:
            msg = "y_max must be greater than y_min"
            raise ValueError(msg)
        return self


class ProvenanceTuple(MapTheIslandBaseModel):
    """Mandatory lineage bundle carried by evidence and derived artifacts."""

    source_url: AnyHttpUrl
    fetch_timestamp: datetime
    sha256: str
    lakefs_commit: str = Field(min_length=1)
    iceberg_snapshot_id: str = Field(min_length=1)
    extractor_version: str = Field(min_length=1)
    model_version: str | None = None
    materialized_at: datetime
    review_state: ReviewState

    @field_validator("sha256")
    @classmethod
    def validate_sha256(cls, value: str) -> str:
        """Require a lowercase or uppercase hexadecimal SHA-256 digest."""
        return normalize_sha256(value)


class Document(MapTheIslandBaseModel):
    """Canonical document-level evidence record."""

    document_id: str = Field(min_length=1)
    source_url: AnyHttpUrl
    sha256: str
    mime_type: str = Field(min_length=1)
    doc_type: str = Field(min_length=1)
    page_count: int = Field(gt=0)
    lakefs_commit: str = Field(min_length=1)
    ingest_batch_id: str = Field(min_length=1)
    sensitivity: SensitivityLevel
    review_state: ReviewState
    metadata: dict[str, Any] = Field(default_factory=dict)
    provenance: ProvenanceTuple

    @field_validator("sha256")
    @classmethod
    def validate_sha256(cls, value: str) -> str:
        """Mirror the provenance digest validation on the document surface."""
        return normalize_sha256(value)


class Page(MapTheIslandBaseModel):
    """Canonical page-level evidence record."""

    page_id: str = Field(min_length=1)
    document_id: str = Field(min_length=1)
    page_number: int = Field(gt=0)
    image_uri: str = Field(min_length=1)
    width: float = Field(gt=0.0)
    height: float = Field(gt=0.0)
    native_text_confidence: float = Field(ge=0.0, le=1.0)
    ocr_confidence: float = Field(ge=0.0, le=1.0)
    handwriting_prob: float = Field(ge=0.0, le=1.0)
    layout_json_uri: str = Field(min_length=1)
    sensitivity: SensitivityLevel
    review_state: ReviewState
    provenance: ProvenanceTuple


class Span(MapTheIslandBaseModel):
    """Atomic evidence-backed textual unit."""

    span_id: str = Field(min_length=1)
    page_id: str = Field(min_length=1)
    block_type: str = Field(min_length=1)
    text_raw: str = Field(min_length=1)
    text_normalized: str = Field(min_length=1)
    char_start: int = Field(ge=0)
    char_end: int = Field(gt=0)
    bbox: BoundingBox | None = None
    extraction_engine: ExtractionEngineIdentity
    confidence: float = Field(ge=0.0, le=1.0)
    sensitivity: SensitivityLevel
    review_state: ReviewState
    checksum: str = Field(min_length=1)
    provenance: ProvenanceTuple

    @model_validator(mode="after")
    def validate_offsets(self) -> Span:
        """Ensure spans always point to a forward text interval."""
        if self.char_end <= self.char_start:
            msg = "char_end must be greater than char_start"
            raise ValueError(msg)
        return self


class Claim(MapTheIslandBaseModel):
    """Structured assertion derived from one or more source spans."""

    claim_id: str = Field(min_length=1)
    subject_ref: str = Field(min_length=1)
    predicate: str = Field(min_length=1)
    object_ref_or_literal: str = Field(min_length=1)
    time_start: datetime | None = None
    time_end: datetime | None = None
    location_ref: str | None = None
    source_span_id: str = Field(min_length=1)
    extractor: str = Field(min_length=1)
    model_version: str | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    sensitivity: SensitivityLevel
    review_state: ReviewState
    provenance: ProvenanceTuple

    @model_validator(mode="after")
    def validate_time_interval(self) -> Claim:
        """Reject inverted time intervals while allowing partial temporal data."""
        if (
            self.time_start is not None
            and self.time_end is not None
            and self.time_end < self.time_start
        ):
            msg = "time_end must be greater than or equal to time_start"
            raise ValueError(msg)
        return self
