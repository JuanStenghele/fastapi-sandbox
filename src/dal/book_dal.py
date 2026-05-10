from uuid import UUID
from sqlmodel import select, Session
from db_schema.book_db import Book as DBBook
from objects.book import Book


class BookDAL():
  def create_book(self, session: Session, book: Book) -> Book:
    db_book = DBBook(
      id = book.id,
      title = book.title,
      description = book.description,
      isbn = book.isbn,
      publication_date = book.publication_date,
      cover_image_id = book.cover_image_id,
      created_at = book.created_at,
      updated_at = book.updated_at
    )
    session.add(db_book)
    return book

  def get_book(self, session: Session, id: UUID) -> Book | None:
    statement = select(DBBook).where(DBBook.id == id)
    result = session.exec(statement).first()
    if result is None:
      return None
    return Book.model_validate(result)
