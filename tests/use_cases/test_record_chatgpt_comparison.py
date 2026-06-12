from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from coord_prompt_studio.domain.sessions import ExtractionResult, ExtractionSession, ImageInput
from coord_prompt_studio.use_cases.record_chatgpt_comparison import (
    RecordChatGptComparison,
    RecordComparisonEvaluation,
)


@dataclass
class InMemorySessionRepository:
    session: ExtractionSession

    def get(self, session_id: str) -> ExtractionSession:
        assert session_id == self.session.session_id
        return self.session

    def save(self, session: ExtractionSession) -> ExtractionSession:
        self.session = session
        return session


def make_session() -> ExtractionSession:
    return ExtractionSession.create(
        image_input=ImageInput.create(Path("/tmp/outfit.png"), "photo"),
        extraction_result=ExtractionResult.success("white blouse"),
    )


def test_record_chatgpt_comparison_adds_text_to_session() -> None:
    repository = InMemorySessionRepository(make_session())

    session = RecordChatGptComparison(repository).execute(
        repository.session.session_id,
        "white top",
    )

    assert session.chatgpt_comparison is not None
    assert session.chatgpt_comparison.extracted_text == "white top"


def test_record_comparison_evaluation_adds_ratings_and_note() -> None:
    repository = InMemorySessionRepository(make_session())
    session = RecordChatGptComparison(repository).execute(
        repository.session.session_id,
        "white top",
    )

    evaluated = RecordComparisonEvaluation(repository).execute(
        session.session_id,
        ratings={
            "服装要素の網羅性": "同等",
            "色・柄の正確さ": "不足",
        },
        note="color was vague",
    )

    assert evaluated.chatgpt_comparison is not None
    assert [item.rating.value for item in evaluated.chatgpt_comparison.evaluations] == [
        "同等",
        "不足",
    ]
    assert evaluated.chatgpt_comparison.note == "color was vague"
