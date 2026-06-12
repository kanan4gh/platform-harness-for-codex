from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

from coord_prompt_studio.adapters.image_validation import ImageValidationError, ImageValidator


def test_image_validator_accepts_readable_image(tmp_path: Path) -> None:
    image_path = tmp_path / "outfit.png"
    Image.new("RGB", (1, 1)).save(image_path)

    validated = ImageValidator().validate(image_path)

    assert validated == image_path.resolve()


def test_image_validator_rejects_unsupported_extension(tmp_path: Path) -> None:
    image_path = tmp_path / "outfit.txt"
    image_path.write_text("not image", encoding="utf-8")

    with pytest.raises(ImageValidationError, match="unsupported image extension"):
        ImageValidator().validate(image_path)


def test_image_validator_rejects_unreadable_image(tmp_path: Path) -> None:
    image_path = tmp_path / "outfit.png"
    image_path.write_text("not image", encoding="utf-8")

    with pytest.raises(ImageValidationError, match="image cannot be read"):
        ImageValidator().validate(image_path)
