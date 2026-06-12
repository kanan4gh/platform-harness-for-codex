from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from coord_prompt_studio.domain.sessions import ExtractionSession


class SessionRepositoryError(RuntimeError):
    """Raised when session persistence fails."""


class SessionNotFoundError(SessionRepositoryError):
    """Raised when a session file does not exist."""


@dataclass(frozen=True)
class JsonSessionRepository:
    sessions_dir: Path = Path("data/sessions")

    def save(self, session: ExtractionSession) -> ExtractionSession:
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        path = self._path_for(session.session_id)
        path.write_text(
            json.dumps(session.to_dict(), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return session

    def get(self, session_id: str) -> ExtractionSession:
        path = self._path_for(session_id)
        if not path.exists():
            raise SessionNotFoundError(f"session not found: {session_id}")
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise SessionRepositoryError(f"invalid session json: {path}")
        return ExtractionSession.from_dict(data)

    def list(self) -> list[ExtractionSession]:
        if not self.sessions_dir.exists():
            return []

        sessions = []
        for path in self.sessions_dir.glob("*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise SessionRepositoryError(f"invalid session json: {path}")
            sessions.append(ExtractionSession.from_dict(data))
        return sorted(sessions, key=lambda session: session.created_at, reverse=True)

    def _path_for(self, session_id: str) -> Path:
        if "/" in session_id or "\\" in session_id:
            raise SessionRepositoryError(f"invalid session id: {session_id}")
        return self.sessions_dir / f"{session_id}.json"
