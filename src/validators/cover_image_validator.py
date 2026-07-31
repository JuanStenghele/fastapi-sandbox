from uuid import UUID
from constants import COVER_IMAGE_ALLOWED_CONTENT_TYPES, COVER_IMAGE_MAX_SIZE_BYTES
from dal.book_dal import BookDAL
from objects.error import ValidationError
from objects.image import RawImage
from sqlmodel import Session


class CoverImageValidator():
  def __init__(self, book_dal: BookDAL) -> None:
    self.book_dal = book_dal

  def validate_upsert(self, session: Session, book_id: UUID, image: RawImage) -> None:
    if self.book_dal.get_book(session, book_id) is None:
      raise ValidationError(detail = "BOOK_NOT_FOUND")
    if image.content_type not in COVER_IMAGE_ALLOWED_CONTENT_TYPES:
      raise ValidationError(f"Unsupported image format: {image.content_type}. Allowed: {', '.join(COVER_IMAGE_ALLOWED_CONTENT_TYPES)}")
    if image.get_size() > COVER_IMAGE_MAX_SIZE_BYTES:
      raise ValidationError(f"Image exceeds maximum allowed size of {COVER_IMAGE_MAX_SIZE_BYTES // (1024 * 1024)} MB")

  def validate_deletion(self, session: Session, book_ids: list) -> None:
    existing_books = self.book_dal.get_books_by_ids(session, book_ids)
    existing_books_ids = [book.id for book in existing_books]
    books_ids_not_found = [id for id in book_ids if id not in existing_books_ids]
    if len(books_ids_not_found) != 0:
      raise ValidationError(detail = f"BOOKS_NOT_FOUND: {', '.join(str(id) for id in books_ids_not_found)}")
