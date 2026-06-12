from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from coord_prompt_studio.adapters.codex import CodexExtractionResponse
from coord_prompt_studio.domain.sessions import ExtractionSession, ImageInput
from coord_prompt_studio.use_cases.extract_coordinate_prompt import ExtractCoordinatePrompt


@dataclass
class FakeImageValidator:
    validated_path: Path

    def validate(self, image_path: str | Path) -> Path:
        return self.validated_path


@dataclass
class FakeCodexExtractor:
    response: CodexExtractionResponse
    received_input: ImageInput | None = None

    def extract_coordinate_prompt(self, image_input: ImageInput) -> CodexExtractionResponse:
        self.received_input = image_input
        return self.response


@dataclass
class InMemorySessionRepository:
    saved_session: ExtractionSession | None = None

    def save(self, session: ExtractionSession) -> ExtractionSession:
        self.saved_session = session
        return session


def test_extract_coordinate_prompt_saves_successful_session() -> None:
    validator = FakeImageValidator(Path("/tmp/outfit.png"))
    codex = FakeCodexExtractor(CodexExtractionResponse(prompt_text="white blouse, denim skirt"))
    repository = InMemorySessionRepository()
    use_case = ExtractCoordinatePrompt(validator, codex, repository)

    session = use_case.execute("outfit.png", "illustration", "reference")

    assert session.extraction_result.prompt_text == "white blouse, denim skirt"
    assert session.image_input.path == "/tmp/outfit.png"
    assert session.image_input.input_type.value == "illustration"
    assert session.image_input.note == "reference"
    assert repository.saved_session == session
    assert codex.received_input == session.image_input


def test_extract_coordinate_prompt_saves_failed_session() -> None:
    validator = FakeImageValidator(Path("/tmp/outfit.png"))
    codex = FakeCodexExtractor(CodexExtractionResponse(error_reason="codex failed"))
    repository = InMemorySessionRepository()
    use_case = ExtractCoordinatePrompt(validator, codex, repository)

    session = use_case.execute("outfit.png", "photo")

    assert session.extraction_result.status.value == "failed"
    assert session.extraction_result.error_reason == "codex failed"
