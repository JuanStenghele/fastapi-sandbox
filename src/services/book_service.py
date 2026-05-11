import uuid


from datetime import date, datetime, timezone
from uuid import UUID
from dal.book_dal import BookDAL
from objects.book import Book
from objects.image import RawImage
from services.cover_image_service import CoverImageService
from sqlmodel import Session


class BookService():
  def __init__(self, book_dal: BookDAL, cover_image_service: CoverImageService) -> None:
    self.book_dal: BookDAL = book_dal
    self.cover_image_service = cover_image_service

  def create_book(self, session: Session, title: str, description: str | None, isbn: str | None, publication_date: date | None, cover_image: RawImage | None = None) -> Book:
    cover_image_id = None
    cover_image_url = None
    if cover_image is not None:
      book_cover = self.cover_image_service.create(session, cover_image)
      cover_image_id = book_cover.id
      cover_image_url = book_cover.url
    now = datetime.now(timezone.utc)
    book = Book(
      id = uuid.uuid4(),
      title = title,
      description = description,
      isbn = isbn,
      publication_date = publication_date,
      cover_image_id = cover_image_id,
      cover_image_url = cover_image_url,
      created_at = now,
      updated_at = now
    )
    self.book_dal.create_book(session, book)
    return book

  def get_book(self, session: Session, id: UUID) -> Book | None:
    return self.book_dal.get_book(session, id)
