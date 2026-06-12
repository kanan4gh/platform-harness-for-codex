from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, UnidentifiedImageError


class ImageValidationError(ValueError):
    """Raised when an input image cannot be used for extraction."""


ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


@dataclass(frozen=True)
class ImageValidator:
    allowed_extensions: frozenset[str] = frozenset(ALLOWED_IMAGE_EXTENSIONS)

    def validate(self, image_path: str | Path) -> Path:
        path = Path(image_path).expanduser()
        if not path.exists():
            raise ImageValidationError(f"image path does not exist: {path}")
        if not path.is_file():
            raise ImageValidationError(f"image path is not a file: {path}")
        if path.suffix.lower() not in self.allowed_extensions:
            allowed = ", ".join(sorted(self.allowed_extensions))
            raise ImageValidationError(
                f"unsupported image extension: {path.suffix}. allowed: {allowed}"
            )

        try:
            with Image.open(path) as image:
                image.verify()
        except (OSError, UnidentifiedImageError) as exc:
            raise ImageValidationError(f"image cannot be read: {path}") from exc

        return path.resolve()
