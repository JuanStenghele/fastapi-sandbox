import uuid


from datetime import datetime, timezone
from uuid import UUID
from dal.book_dal import BookDAL
from objects.book import Book
from objects.book_creation import BookCreationRequest
from services.cover_image_service import CoverImageService
from sqlmodel import Session
from validators.book_validator import BookValidator


class BookService():
  def __init__(self, book_dal: BookDAL, cover_image_service: CoverImageService, book_validator: BookValidator) -> None:
    self.book_dal: BookDAL = book_dal
    self.cover_image_service = cover_image_service
    self.book_validator: BookValidator = book_validator

  def create_book(self, session: Session, request: BookCreationRequest) -> Book:
    self.book_validator.validate_creation(session, request)
    cover = self.cover_image_service.create(session, request.cover_image) if request.cover_image else None
    now = datetime.now(timezone.utc)
    book = Book(
      id = uuid.uuid4(),
      title = request.title,
      author_id = request.author_id,
      description = request.description,
      isbn = request.isbn,
      publication_date = request.publication_date,
      cover_image = cover,
      created_at = now,
      updated_at = now
    )
    self.book_dal.create_book(session, book)
    return book

  def get_book(self, session: Session, id: UUID) -> Book | None:
    return self.book_dal.get_book(session, id)
