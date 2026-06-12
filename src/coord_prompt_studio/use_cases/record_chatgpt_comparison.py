from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from coord_prompt_studio.domain.sessions import (
    ChatGptComparison,
    ComparisonEvaluation,
    ExtractionSession,
)


class SessionRepositoryPort(Protocol):
    def get(self, session_id: str) -> ExtractionSession: ...

    def save(self, session: ExtractionSession) -> ExtractionSession: ...


@dataclass(frozen=True)
class RecordChatGptComparison:
    session_repository: SessionRepositoryPort

    def execute(self, session_id: str, extracted_text: str) -> ExtractionSession:
        session = self.session_repository.get(session_id)
        comparison = ChatGptComparison.create(extracted_text=extracted_text)
        return self.session_repository.save(session.with_chatgpt_comparison(comparison))


@dataclass(frozen=True)
class RecordComparisonEvaluation:
    session_repository: SessionRepositoryPort

    def execute(
        self,
        session_id: str,
        ratings: dict[str, str],
        note: str | None = None,
    ) -> ExtractionSession:
        session = self.session_repository.get(session_id)
        evaluations = [
            ComparisonEvaluation.create(criterion=criterion, rating=rating)
            for criterion, rating in ratings.items()
        ]
        return self.session_repository.save(
            session.with_comparison_evaluations(evaluations=evaluations, note=note)
        )
