from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from coord_prompt_studio.domain.sessions import ExtractionSession


class SessionRepositoryPort(Protocol):
    def get(self, session_id: str) -> ExtractionSession: ...

    def list(self) -> list[ExtractionSession]: ...


@dataclass(frozen=True)
class ListSessions:
    session_repository: SessionRepositoryPort

    def execute(self) -> list[ExtractionSession]:
        return self.session_repository.list()


@dataclass(frozen=True)
class ShowSession:
    session_repository: SessionRepositoryPort

    def execute(self, session_id: str) -> ExtractionSession:
        return self.session_repository.get(session_id)
