from constants import COVER_IMAGE_ALLOWED_CONTENT_TYPES, COVER_IMAGE_MAX_SIZE_BYTES
from objects.error import ValidationError
from objects.image import RawImage


class CoverImageValidator():
  def validate(self, image: RawImage) -> None:
    if image.content_type not in COVER_IMAGE_ALLOWED_CONTENT_TYPES:
      raise ValidationError(f"Unsupported image format: {image.content_type}. Allowed: {', '.join(COVER_IMAGE_ALLOWED_CONTENT_TYPES)}")
    if image.get_size() > COVER_IMAGE_MAX_SIZE_BYTES:
      raise ValidationError(f"Image exceeds maximum allowed size of {COVER_IMAGE_MAX_SIZE_BYTES // (1024 * 1024)} MB")
