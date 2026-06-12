from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from coord_prompt_studio.adapters.codex import CodexExtractionResponse
from coord_prompt_studio.domain.sessions import ExtractionResult, ExtractionSession, ImageInput


class ImageValidatorPort(Protocol):
    def validate(self, image_path: str | Path) -> Path: ...


class CodexExtractorPort(Protocol):
    def extract_coordinate_prompt(self, image_input: ImageInput) -> CodexExtractionResponse: ...


class SessionRepositoryPort(Protocol):
    def save(self, session: ExtractionSession) -> ExtractionSession: ...


@dataclass(frozen=True)
class ExtractCoordinatePrompt:
    image_validator: ImageValidatorPort
    codex_extractor: CodexExtractorPort
    session_repository: SessionRepositoryPort

    def execute(
        self,
        image_path: str | Path,
        input_type: str,
        note: str | None = None,
    ) -> ExtractionSession:
        validated_path = self.image_validator.validate(image_path)
        image_input = ImageInput.create(path=validated_path, input_type=input_type, note=note)

        response = self.codex_extractor.extract_coordinate_prompt(image_input)
        if response.succeeded and response.prompt_text is not None:
            result = ExtractionResult.success(response.prompt_text)
        else:
            result = ExtractionResult.failed(
                response.error_reason or "coordinate extraction failed"
            )

        session = ExtractionSession.create(image_input=image_input, extraction_result=result)
        return self.session_repository.save(session)
