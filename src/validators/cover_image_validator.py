from constants import COVER_IMAGE_ALLOWED_CONTENT_TYPES
from objects.error import ValidationError
from objects.image import RawImage


class CoverImageValidator():
  def validate(self, image: RawImage) -> None:
    if image.content_type not in COVER_IMAGE_ALLOWED_CONTENT_TYPES:
      raise ValidationError(f"Unsupported image format: {image.content_type}. Allowed: {', '.join(COVER_IMAGE_ALLOWED_CONTENT_TYPES)}")
