"""Coverage-complete tests for the Phase 00 schema baseline."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import pytest
from maptheisland_schemas import (
    BoundingBox,
    Claim,
    Document,
    ExtractionEngineIdentity,
    Page,
    ProvenanceTuple,
    ReviewState,
    SensitivityLevel,
    Span,
)
from pydantic import AnyHttpUrl, TypeAdapter, ValidationError

DOC_URL = TypeAdapter(AnyHttpUrl).validate_python("https://www.justice.gov/example/document.pdf")


def build_provenance(**overrides: object) -> ProvenanceTuple:
    """Create a valid provenance tuple with optional overrides."""
    payload: dict[str, Any] = {
        "source_url": DOC_URL,
        "fetch_timestamp": datetime(2026, 3, 6, 12, 0, tzinfo=UTC),
        "sha256": "a" * 64,
        "lakefs_commit": "commit-001",
        "iceberg_snapshot_id": "snapshot-001",
        "extractor_version": "pymupdf-1.0.0",
        "model_version": None,
        "materialized_at": datetime(2026, 3, 6, 12, 30, tzinfo=UTC),
        "review_state": ReviewState.PENDING,
    }
    payload.update(overrides)
    return ProvenanceTuple(**payload)


def test_module_exports_expected_types() -> None:
    """The public package surface should remain stable for downstream imports."""
    assert ExtractionEngineIdentity.PYMUPDF.value == "pymupdf"
    assert ReviewState.NEEDS_HUMAN_REVIEW.value == "needs_human_review"
    assert SensitivityLevel.UNSAFE_FOR_LLM.value == "unsafe_for_llm"


def test_bounding_box_validates_coordinate_order() -> None:
    """Bounding boxes must be strictly increasing on both axes."""
    box = BoundingBox(x_min=0.0, y_min=1.0, x_max=10.0, y_max=11.0)
    assert box.x_max == 10.0

    with pytest.raises(ValidationError, match="x_max must be greater than x_min"):
        BoundingBox(x_min=2.0, y_min=1.0, x_max=2.0, y_max=5.0)

    with pytest.raises(ValidationError, match="y_max must be greater than y_min"):
        BoundingBox(x_min=0.0, y_min=4.0, x_max=5.0, y_max=4.0)


def test_provenance_tuple_normalizes_sha256_and_keeps_optional_model_version() -> None:
    """The provenance tuple is the reusable lineage authority."""
    provenance = build_provenance(sha256="A" * 64)

    assert provenance.sha256 == "a" * 64
    assert provenance.model_version is None


def test_provenance_tuple_rejects_invalid_sha256() -> None:
    """Invalid lineage digests must be blocked early."""
    with pytest.raises(ValidationError, match="sha256 must be a 64-character hexadecimal digest"):
        build_provenance(sha256="bad-digest")


def test_document_reuses_provenance_validation() -> None:
    """Document rows mirror the key provenance fields for queryability."""
    document = Document(
        document_id="doc-001",
        source_url=DOC_URL,
        sha256="B" * 64,
        mime_type="application/pdf",
        doc_type="memorandum",
        page_count=3,
        lakefs_commit="commit-001",
        ingest_batch_id="ingest-001",
        sensitivity=SensitivityLevel.PUBLIC_GENERAL,
        review_state=ReviewState.ACCEPTED,
        provenance=build_provenance(),
    )

    assert document.sha256 == "b" * 64
    assert document.metadata == {}

    with pytest.raises(ValidationError, match="sha256 must be a 64-character hexadecimal digest"):
        Document(
            document_id="doc-001",
            source_url=DOC_URL,
            sha256="not-a-digest",
            mime_type="application/pdf",
            doc_type="memorandum",
            page_count=3,
            lakefs_commit="commit-001",
            ingest_batch_id="ingest-001",
            sensitivity=SensitivityLevel.PUBLIC_GENERAL,
            review_state=ReviewState.ACCEPTED,
            provenance=build_provenance(),
        )


def test_page_accepts_valid_confidence_range() -> None:
    """Page records preserve multi-lane extraction confidence signals."""
    page = Page(
        page_id="page-001",
        document_id="doc-001",
        page_number=1,
        image_uri="s3://bucket/doc-001/page-001.png",
        width=612.0,
        height=792.0,
        native_text_confidence=0.95,
        ocr_confidence=0.82,
        handwriting_prob=0.10,
        layout_json_uri="s3://bucket/doc-001/page-001-layout.json",
        sensitivity=SensitivityLevel.PUBLIC_GENERAL,
        review_state=ReviewState.PENDING,
        provenance=build_provenance(),
    )

    assert page.handwriting_prob == pytest.approx(0.10)

    with pytest.raises(ValidationError):
        Page(
            page_id="page-001",
            document_id="doc-001",
            page_number=1,
            image_uri="s3://bucket/doc-001/page-001.png",
            width=612.0,
            height=792.0,
            native_text_confidence=1.2,
            ocr_confidence=0.82,
            handwriting_prob=0.10,
            layout_json_uri="s3://bucket/doc-001/page-001-layout.json",
            sensitivity=SensitivityLevel.PUBLIC_GENERAL,
            review_state=ReviewState.PENDING,
            provenance=build_provenance(),
        )


def test_span_requires_forward_offsets_and_supports_optional_bbox() -> None:
    """Spans are the atomic truth objects and therefore require strict offsets."""
    span = Span(
        span_id="span-001",
        page_id="page-001",
        block_type="paragraph",
        text_raw="Original raw text",
        text_normalized="original raw text",
        char_start=0,
        char_end=17,
        bbox=BoundingBox(x_min=0.0, y_min=0.0, x_max=10.0, y_max=10.0),
        extraction_engine=ExtractionEngineIdentity.PYMUPDF,
        confidence=0.99,
        sensitivity=SensitivityLevel.PUBLIC_GENERAL,
        review_state=ReviewState.ACCEPTED,
        checksum="checksum-001",
        provenance=build_provenance(),
    )

    assert span.bbox is not None
    assert span.extraction_engine is ExtractionEngineIdentity.PYMUPDF

    span_without_bbox = Span(
        span_id="span-002",
        page_id="page-001",
        block_type="line",
        text_raw="Text",
        text_normalized="text",
        char_start=5,
        char_end=9,
        extraction_engine=ExtractionEngineIdentity.TESSERACT,
        confidence=0.75,
        sensitivity=SensitivityLevel.PUBLIC_EXPLICIT_REDACTED,
        review_state=ReviewState.NEEDS_HUMAN_REVIEW,
        checksum="checksum-002",
        provenance=build_provenance(),
    )

    assert span_without_bbox.bbox is None

    with pytest.raises(ValidationError, match="char_end must be greater than char_start"):
        Span(
            span_id="span-003",
            page_id="page-001",
            block_type="line",
            text_raw="Text",
            text_normalized="text",
            char_start=9,
            char_end=9,
            extraction_engine=ExtractionEngineIdentity.TESSERACT,
            confidence=0.75,
            sensitivity=SensitivityLevel.PUBLIC_GENERAL,
            review_state=ReviewState.PENDING,
            checksum="checksum-003",
            provenance=build_provenance(),
        )


def test_claim_accepts_partial_temporal_data_and_rejects_inverted_intervals() -> None:
    """Claims may be partially dated, but not temporally inverted."""
    claim = Claim(
        claim_id="claim-001",
        subject_ref="entity-001",
        predicate="mentions",
        object_ref_or_literal="entity-002",
        time_start=datetime(2026, 3, 1, 8, 0, tzinfo=UTC),
        source_span_id="span-001",
        extractor="phase-00-baseline",
        model_version="none",
        confidence=0.85,
        sensitivity=SensitivityLevel.PUBLIC_GENERAL,
        review_state=ReviewState.PENDING,
        provenance=build_provenance(),
    )

    assert claim.time_end is None

    with pytest.raises(
        ValidationError,
        match="time_end must be greater than or equal to time_start",
    ):
        Claim(
            claim_id="claim-002",
            subject_ref="entity-001",
            predicate="mentions",
            object_ref_or_literal="entity-002",
            time_start=datetime(2026, 3, 2, 8, 0, tzinfo=UTC),
            time_end=datetime(2026, 3, 1, 8, 0, tzinfo=UTC),
            source_span_id="span-001",
            extractor="phase-00-baseline",
            confidence=0.85,
            sensitivity=SensitivityLevel.PUBLIC_GENERAL,
            review_state=ReviewState.PENDING,
            provenance=build_provenance(),
        )
