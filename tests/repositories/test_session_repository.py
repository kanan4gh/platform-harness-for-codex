from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from coord_prompt_studio.domain.sessions import ExtractionResult, ExtractionSession, ImageInput
from coord_prompt_studio.repositories.session_repository import (
    JsonSessionRepository,
    SessionNotFoundError,
)


def make_session(image_path: str, created_at: datetime) -> ExtractionSession:
    return ExtractionSession.create(
        image_input=ImageInput.create(Path(image_path), "photo"),
        extraction_result=ExtractionResult.success("prompt text"),
        created_at=created_at,
    )


def test_repository_saves_and_loads_session(tmp_path: Path) -> None:
    repository = JsonSessionRepository(tmp_path)
    session = make_session("/tmp/a.png", datetime(2026, 6, 12, 8, 0, tzinfo=UTC))

    repository.save(session)

    assert repository.get(session.session_id) == session


def test_repository_lists_sessions_by_created_at_desc(tmp_path: Path) -> None:
    repository = JsonSessionRepository(tmp_path)
    older = make_session("/tmp/older.png", datetime(2026, 6, 12, 8, 0, tzinfo=UTC))
    newer = make_session("/tmp/newer.png", datetime(2026, 6, 12, 9, 0, tzinfo=UTC))

    repository.save(older)
    repository.save(newer)

    assert [session.session_id for session in repository.list()] == [
        newer.session_id,
        older.session_id,
    ]


def test_repository_get_missing_session_raises_error(tmp_path: Path) -> None:
    repository = JsonSessionRepository(tmp_path)

    with pytest.raises(SessionNotFoundError, match="session not found"):
        repository.get("missing")
