import uuid


from datetime import date, datetime, timezone
from uuid import UUID
from dal.book_dal import BookDAL
from objects.book import Book
from sqlmodel import Session


class BookService():
  def __init__(self, book_dal: BookDAL) -> None:
    self.book_dal: BookDAL = book_dal

  def create_book(self, session: Session, title: str, description: str | None, isbn: str | None, publication_date: date | None) -> Book:
    now = datetime.now(timezone.utc)
    book = Book(
      id = uuid.uuid4(),
      title = title,
      description = description,
      isbn = isbn,
      publication_date = publication_date,
      created_at = now,
      updated_at = now
    )
    self.book_dal.create_book(session, book)
    return book

  def get_book(self, session: Session, id: UUID) -> Book | None:
    return self.book_dal.get_book(session, id)
