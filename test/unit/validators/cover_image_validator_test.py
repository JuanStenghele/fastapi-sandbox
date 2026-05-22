import pytest


from unittest.mock import MagicMock
from constants import COVER_IMAGE_ALLOWED_CONTENT_TYPES, COVER_IMAGE_MAX_SIZE_BYTES
from objects.error import ValidationError
from objects.image import RawImage
from validators.cover_image_validator import CoverImageValidator


class TestCoverImageValidator():
  def test_validate_creation_success(self):
    image = RawImage.model_construct(file = MagicMock(), content_type = "image/jpeg", size = 1024)
    instance = CoverImageValidator()
    instance.validate_creation(image)

  def test_validate_creation_invalid_content_type(self):
    image = RawImage.model_construct(file = MagicMock(), content_type = "image/bmp", size = 1024)
    instance = CoverImageValidator()
    with pytest.raises(ValidationError) as exc_info:
      instance.validate_creation(image)
    assert "image/bmp" in exc_info.value.detail
    assert all(ct in exc_info.value.detail for ct in COVER_IMAGE_ALLOWED_CONTENT_TYPES)

  def test_validate_creation_exceeds_max_size(self):
    image = RawImage.model_construct(file = MagicMock(), content_type = "image/jpeg", size = 20 * 1024 * 1024)
    instance = CoverImageValidator()
    with pytest.raises(ValidationError) as exc_info:
      instance.validate_creation(image)
    assert str(COVER_IMAGE_MAX_SIZE_BYTES // (1024 * 1024)) in exc_info.value.detail
