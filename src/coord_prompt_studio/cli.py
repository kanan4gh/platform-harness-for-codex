from __future__ import annotations

from pathlib import Path
from typing import Annotated, NoReturn

import typer

from coord_prompt_studio.adapters.codex import CodexCliAdapter
from coord_prompt_studio.adapters.image_validation import ImageValidationError, ImageValidator
from coord_prompt_studio.domain.sessions import (
    ComparisonCriterion,
    ComparisonRating,
    DomainError,
    ExtractionSession,
)
from coord_prompt_studio.repositories.session_repository import (
    JsonSessionRepository,
    SessionNotFoundError,
    SessionRepositoryError,
)
from coord_prompt_studio.use_cases.extract_coordinate_prompt import ExtractCoordinatePrompt
from coord_prompt_studio.use_cases.list_sessions import ListSessions, ShowSession
from coord_prompt_studio.use_cases.record_chatgpt_comparison import (
    RecordChatGptComparison,
    RecordComparisonEvaluation,
)

app = typer.Typer(no_args_is_help=True, help="Coord Prompt Studio MVP 0 CLI")


def _repository() -> JsonSessionRepository:
    return JsonSessionRepository()


def _handle_error(exc: Exception) -> NoReturn:
    typer.secho(f"Error: {exc}", fg=typer.colors.RED, err=True)
    raise typer.Exit(code=1) from exc


@app.command()
def extract(
    image_path: Annotated[Path, typer.Argument(help="Coordinate image path.")],
    input_type: Annotated[
        str,
        typer.Option("--input-type", "-t", help="Input type: photo or illustration."),
    ] = "photo",
    note: Annotated[str | None, typer.Option("--note", "-n", help="Optional session note.")] = None,
) -> None:
    """Create an extraction session from a coordinate image."""
    use_case = ExtractCoordinatePrompt(
        image_validator=ImageValidator(),
        codex_extractor=CodexCliAdapter(),
        session_repository=_repository(),
    )
    try:
        session = use_case.execute(image_path=image_path, input_type=input_type, note=note)
    except (DomainError, ImageValidationError, SessionRepositoryError) as exc:
        _handle_error(exc)

    typer.echo(f"session_id: {session.session_id}")
    typer.echo(f"status: {session.extraction_result.status.value}")
    if session.extraction_result.prompt_text:
        typer.echo("")
        typer.echo(session.extraction_result.prompt_text)
    if session.extraction_result.error_reason:
        typer.echo(f"error_reason: {session.extraction_result.error_reason}")


@app.command("add-chatgpt")
def add_chatgpt(
    session_id: Annotated[str, typer.Argument(help="Session ID.")],
    text: Annotated[
        str | None,
        typer.Option("--text", help="ChatGPT extraction text. Use --file for longer text."),
    ] = None,
    file: Annotated[
        Path | None,
        typer.Option("--file", "-f", help="File containing ChatGPT extraction text."),
    ] = None,
) -> None:
    """Attach ChatGPT extraction text to an existing session."""
    try:
        extracted_text = _read_text_argument(text=text, file=file)
        session = RecordChatGptComparison(_repository()).execute(
            session_id=session_id,
            extracted_text=extracted_text,
        )
    except (DomainError, SessionRepositoryError, OSError) as exc:
        _handle_error(exc)

    typer.echo(f"updated: {session.session_id}")


@app.command()
def evaluate(
    session_id: Annotated[str, typer.Argument(help="Session ID.")],
    coverage: Annotated[
        str,
        typer.Option("--coverage", help="服装要素の網羅性: 同等, 不足, 過剰, 要改善"),
    ],
    colors_patterns: Annotated[
        str,
        typer.Option("--colors-patterns", help="色・柄の正確さ: 同等, 不足, 過剰, 要改善"),
    ],
    materials: Annotated[
        str,
        typer.Option("--materials", help="素材感の表現: 同等, 不足, 過剰, 要改善"),
    ],
    silhouette: Annotated[
        str,
        typer.Option("--silhouette", help="シルエットの表現: 同等, 不足, 過剰, 要改善"),
    ],
    prompt_usability: Annotated[
        str,
        typer.Option(
            "--prompt-usability",
            help="画像生成プロンプトとしての使いやすさ: 同等, 不足, 過剰, 要改善",
        ),
    ],
    note: Annotated[str | None, typer.Option("--note", "-n", help="Evaluation note.")] = None,
) -> None:
    """Record comparison ratings for a session with ChatGPT text."""
    ratings = {
        ComparisonCriterion.COVERAGE.value: coverage,
        ComparisonCriterion.COLORS_AND_PATTERNS.value: colors_patterns,
        ComparisonCriterion.MATERIALS.value: materials,
        ComparisonCriterion.SILHOUETTE.value: silhouette,
        ComparisonCriterion.PROMPT_USABILITY.value: prompt_usability,
    }
    try:
        session = RecordComparisonEvaluation(_repository()).execute(
            session_id=session_id,
            ratings=ratings,
            note=note,
        )
    except (DomainError, SessionRepositoryError) as exc:
        _handle_error(exc)

    typer.echo(f"evaluated: {session.session_id}")


@app.command("list")
def list_command() -> None:
    """List saved extraction sessions."""
    try:
        sessions = ListSessions(_repository()).execute()
    except SessionRepositoryError as exc:
        _handle_error(exc)

    if not sessions:
        typer.echo("No sessions found.")
        return

    for session in sessions:
        status = session.extraction_result.status.value
        input_type = session.image_input.input_type.value
        typer.echo(f"{session.session_id}\t{status}\t{input_type}\t{session.image_input.path}")


@app.command()
def show(session_id: Annotated[str, typer.Argument(help="Session ID.")]) -> None:
    """Show a saved extraction session."""
    try:
        session = ShowSession(_repository()).execute(session_id)
    except (SessionNotFoundError, SessionRepositoryError) as exc:
        _handle_error(exc)

    _print_session(session)


def _read_text_argument(text: str | None, file: Path | None) -> str:
    if text and file:
        raise DomainError("use either --text or --file, not both")
    if file:
        return file.read_text(encoding="utf-8")
    if text:
        return text
    raise DomainError("provide ChatGPT extraction text with --text or --file")


def _print_session(session: ExtractionSession) -> None:
    typer.echo(f"session_id: {session.session_id}")
    typer.echo(f"created_at: {session.created_at.isoformat()}")
    typer.echo(f"updated_at: {session.updated_at.isoformat()}")
    typer.echo(f"image_path: {session.image_input.path}")
    typer.echo(f"input_type: {session.image_input.input_type.value}")
    if session.image_input.note:
        typer.echo(f"note: {session.image_input.note}")
    typer.echo("")
    typer.echo("[Coord Prompt Studio extraction]")
    if session.extraction_result.prompt_text:
        typer.echo(session.extraction_result.prompt_text)
    if session.extraction_result.error_reason:
        typer.echo(f"failed: {session.extraction_result.error_reason}")

    typer.echo("")
    typer.echo("[ChatGPT extraction]")
    if session.chatgpt_comparison:
        typer.echo(session.chatgpt_comparison.extracted_text)
        if session.chatgpt_comparison.evaluations:
            typer.echo("")
            typer.echo("[Comparison evaluation]")
            for evaluation in session.chatgpt_comparison.evaluations:
                typer.echo(f"- {evaluation.criterion.value}: {evaluation.rating.value}")
        if session.chatgpt_comparison.note:
            typer.echo("")
            typer.echo(f"evaluation_note: {session.chatgpt_comparison.note}")
    else:
        typer.echo("not recorded")


def valid_rating_values() -> list[str]:
    return [item.value for item in ComparisonRating]


if __name__ == "__main__":
    app()
