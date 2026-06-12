from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from coord_prompt_studio.domain.sessions import (
    ChatGptComparison,
    ComparisonEvaluation,
    DomainError,
    ExtractionResult,
    ExtractionSession,
    ImageInput,
)


def test_image_input_create_with_invalid_input_type_raises_domain_error() -> None:
    with pytest.raises(DomainError, match="input_type must be one of"):
        ImageInput.create(Path("sample.png"), "sketch")


def test_extraction_result_success_with_empty_text_raises_domain_error() -> None:
    with pytest.raises(DomainError, match="prompt_text must not be empty"):
        ExtractionResult.success("  ")


def test_comparison_evaluation_create_with_invalid_rating_raises_domain_error() -> None:
    with pytest.raises(DomainError, match="rating must be one of"):
        ComparisonEvaluation.create("服装要素の網羅性", "良い")


def test_session_to_dict_round_trips() -> None:
    created_at = datetime(2026, 6, 12, 8, 30, tzinfo=UTC)
    session = ExtractionSession.create(
        image_input=ImageInput.create(Path("/tmp/sample.png"), "photo", "summer"),
        extraction_result=ExtractionResult.success("white shirt and denim"),
        created_at=created_at,
    )
    session = session.with_chatgpt_comparison(
        ChatGptComparison.create(
            extracted_text="white top and blue jeans",
            evaluations=[ComparisonEvaluation.create("服装要素の網羅性", "同等")],
            note="close enough",
        ),
        updated_at=created_at,
    )

    restored = ExtractionSession.from_dict(session.to_dict())

    assert restored == session


def test_session_evaluation_requires_chatgpt_comparison() -> None:
    session = ExtractionSession.create(
        image_input=ImageInput.create(Path("/tmp/sample.png"), "illustration"),
        extraction_result=ExtractionResult.success("black dress"),
    )

    with pytest.raises(DomainError, match="chatgpt comparison must be added"):
        session.with_comparison_evaluations(
            evaluations=[ComparisonEvaluation.create("素材感の表現", "要改善")],
            note=None,
        )
