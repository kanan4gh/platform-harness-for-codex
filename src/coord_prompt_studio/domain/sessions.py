from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, Self


class DomainError(ValueError):
    """Raised when domain data violates Coord Prompt Studio rules."""


class InputType(StrEnum):
    PHOTO = "photo"
    ILLUSTRATION = "illustration"


class ExtractionStatus(StrEnum):
    SUCCESS = "success"
    FAILED = "failed"


class ComparisonRating(StrEnum):
    EQUIVALENT = "同等"
    INSUFFICIENT = "不足"
    EXCESSIVE = "過剰"
    NEEDS_IMPROVEMENT = "要改善"


class ComparisonCriterion(StrEnum):
    COVERAGE = "服装要素の網羅性"
    COLORS_AND_PATTERNS = "色・柄の正確さ"
    MATERIALS = "素材感の表現"
    SILHOUETTE = "シルエットの表現"
    PROMPT_USABILITY = "画像生成プロンプトとしての使いやすさ"


def now_utc() -> datetime:
    return datetime.now(UTC).replace(microsecond=0)


def parse_datetime(value: str) -> datetime:
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed


def session_id_from_datetime(value: datetime) -> str:
    return value.astimezone(UTC).strftime("%Y%m%d-%H%M%S")


@dataclass(frozen=True)
class ImageInput:
    path: str
    input_type: InputType
    note: str | None = None

    @classmethod
    def create(cls, path: Path, input_type: str, note: str | None = None) -> Self:
        try:
            parsed_type = InputType(input_type)
        except ValueError as exc:
            allowed = ", ".join(item.value for item in InputType)
            raise DomainError(f"input_type must be one of: {allowed}") from exc

        normalized_note = note.strip() if note else None
        return cls(path=str(path), input_type=parsed_type, note=normalized_note or None)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            path=str(data["path"]),
            input_type=InputType(data["input_type"]),
            note=data.get("note"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "input_type": self.input_type.value,
            "note": self.note,
        }


@dataclass(frozen=True)
class ExtractionResult:
    status: ExtractionStatus
    prompt_text: str | None = None
    error_reason: str | None = None

    @classmethod
    def success(cls, prompt_text: str) -> Self:
        normalized = prompt_text.strip()
        if not normalized:
            raise DomainError("prompt_text must not be empty")
        return cls(status=ExtractionStatus.SUCCESS, prompt_text=normalized)

    @classmethod
    def failed(cls, error_reason: str) -> Self:
        normalized = error_reason.strip()
        if not normalized:
            raise DomainError("error_reason must not be empty")
        return cls(status=ExtractionStatus.FAILED, error_reason=normalized)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            status=ExtractionStatus(data["status"]),
            prompt_text=data.get("prompt_text"),
            error_reason=data.get("error_reason"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status.value,
            "prompt_text": self.prompt_text,
            "error_reason": self.error_reason,
        }


@dataclass(frozen=True)
class ComparisonEvaluation:
    criterion: ComparisonCriterion
    rating: ComparisonRating

    @classmethod
    def create(cls, criterion: str, rating: str) -> Self:
        try:
            parsed_criterion = ComparisonCriterion(criterion)
        except ValueError as exc:
            allowed = ", ".join(item.value for item in ComparisonCriterion)
            raise DomainError(f"criterion must be one of: {allowed}") from exc

        try:
            parsed_rating = ComparisonRating(rating)
        except ValueError as exc:
            allowed = ", ".join(item.value for item in ComparisonRating)
            raise DomainError(f"rating must be one of: {allowed}") from exc

        return cls(criterion=parsed_criterion, rating=parsed_rating)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            criterion=ComparisonCriterion(data["criterion"]),
            rating=ComparisonRating(data["rating"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "criterion": self.criterion.value,
            "rating": self.rating.value,
        }


@dataclass(frozen=True)
class ChatGptComparison:
    extracted_text: str
    evaluations: list[ComparisonEvaluation] = field(default_factory=list)
    note: str | None = None

    @classmethod
    def create(
        cls,
        extracted_text: str,
        evaluations: list[ComparisonEvaluation] | None = None,
        note: str | None = None,
    ) -> Self:
        normalized_text = extracted_text.strip()
        if not normalized_text:
            raise DomainError("chatgpt extracted_text must not be empty")
        normalized_note = note.strip() if note else None
        return cls(
            extracted_text=normalized_text,
            evaluations=evaluations or [],
            note=normalized_note or None,
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            extracted_text=str(data["extracted_text"]),
            evaluations=[
                ComparisonEvaluation.from_dict(item) for item in data.get("evaluations", [])
            ],
            note=data.get("note"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "extracted_text": self.extracted_text,
            "evaluations": [item.to_dict() for item in self.evaluations],
            "note": self.note,
        }

    def with_evaluations(
        self,
        evaluations: list[ComparisonEvaluation],
        note: str | None,
    ) -> ChatGptComparison:
        normalized_note = note.strip() if note else None
        return ChatGptComparison(
            extracted_text=self.extracted_text,
            evaluations=evaluations,
            note=normalized_note or None,
        )


@dataclass(frozen=True)
class ExtractionSession:
    session_id: str
    image_input: ImageInput
    extraction_result: ExtractionResult
    created_at: datetime
    updated_at: datetime
    chatgpt_comparison: ChatGptComparison | None = None

    @classmethod
    def create(
        cls,
        image_input: ImageInput,
        extraction_result: ExtractionResult,
        created_at: datetime | None = None,
    ) -> Self:
        timestamp = created_at or now_utc()
        return cls(
            session_id=session_id_from_datetime(timestamp),
            image_input=image_input,
            extraction_result=extraction_result,
            created_at=timestamp,
            updated_at=timestamp,
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        comparison = data.get("chatgpt_comparison")
        return cls(
            session_id=str(data["session_id"]),
            image_input=ImageInput.from_dict(data["image_input"]),
            extraction_result=ExtractionResult.from_dict(data["extraction_result"]),
            created_at=parse_datetime(str(data["created_at"])),
            updated_at=parse_datetime(str(data["updated_at"])),
            chatgpt_comparison=ChatGptComparison.from_dict(comparison) if comparison else None,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "image_input": self.image_input.to_dict(),
            "extraction_result": self.extraction_result.to_dict(),
            "chatgpt_comparison": (
                self.chatgpt_comparison.to_dict() if self.chatgpt_comparison else None
            ),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def with_chatgpt_comparison(
        self,
        comparison: ChatGptComparison,
        updated_at: datetime | None = None,
    ) -> ExtractionSession:
        return ExtractionSession(
            session_id=self.session_id,
            image_input=self.image_input,
            extraction_result=self.extraction_result,
            chatgpt_comparison=comparison,
            created_at=self.created_at,
            updated_at=updated_at or now_utc(),
        )

    def with_comparison_evaluations(
        self,
        evaluations: list[ComparisonEvaluation],
        note: str | None,
        updated_at: datetime | None = None,
    ) -> ExtractionSession:
        if self.chatgpt_comparison is None:
            raise DomainError("chatgpt comparison must be added before evaluation")
        return self.with_chatgpt_comparison(
            self.chatgpt_comparison.with_evaluations(evaluations=evaluations, note=note),
            updated_at=updated_at,
        )
