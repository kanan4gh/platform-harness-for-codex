from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from coord_prompt_studio.domain.sessions import ImageInput


@dataclass(frozen=True)
class CodexExtractionResponse:
    prompt_text: str | None = None
    error_reason: str | None = None

    @property
    def succeeded(self) -> bool:
        return self.prompt_text is not None


@dataclass(frozen=True)
class CodexCliAdapter:
    prompt_template_path: Path = Path("prompts/coordinate_extraction.md")
    command: tuple[str, ...] = ("codex", "exec")
    timeout_seconds: int = 180

    def extract_coordinate_prompt(self, image_input: ImageInput) -> CodexExtractionResponse:
        instruction = self._build_instruction(image_input)
        try:
            completed = subprocess.run(
                [*self.command, instruction],
                check=False,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
            )
        except FileNotFoundError:
            return CodexExtractionResponse(error_reason="codex CLI was not found")
        except subprocess.TimeoutExpired:
            return CodexExtractionResponse(error_reason="codex CLI timed out")

        stdout = completed.stdout.strip()
        stderr = completed.stderr.strip()
        if completed.returncode != 0:
            reason = stderr or stdout or f"codex CLI failed with exit code {completed.returncode}"
            return CodexExtractionResponse(error_reason=reason)
        if not stdout:
            return CodexExtractionResponse(error_reason="codex CLI returned empty output")
        return CodexExtractionResponse(prompt_text=stdout)

    def _build_instruction(self, image_input: ImageInput) -> str:
        template = self.prompt_template_path.read_text(encoding="utf-8")
        note = image_input.note or "なし"
        return "\n\n".join(
            [
                template,
                "## 入力",
                f"- 画像パス: {image_input.path}",
                f"- 入力種別: {image_input.input_type.value}",
                f"- メモ: {note}",
                "上記の画像パスを参照し、コーディネート抽出を実行してください。",
            ]
        )
