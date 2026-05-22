from uuid import UUID
from sqlmodel import select, Session
from db_schema.book_author_db import BookAuthor as DBBookAuthor
from db_schema.book_cover_db import BookCover as DBBookCover
from db_schema.book_db import Book as DBBook
from objects.book import Book
from objects.cover_image import CoverImage


class BookDAL():
  def create_book(self, session: Session, book: Book) -> Book:
    db_book = DBBook(
      id = book.id,
      title = book.title,
      description = book.description,
      isbn = book.isbn,
      publication_date = book.publication_date,
      cover_image_id = book.cover_image.id if book.cover_image else None,
      created_at = book.created_at,
      updated_at = book.updated_at
    )
    session.add(db_book)
    session.flush()
    db_book_author = DBBookAuthor(
      book_id = book.id,
      author_id = book.author_id,
      created_at = book.created_at,
    )
    session.add(db_book_author)
    return book

  def get_book(self, session: Session, id: UUID) -> Book | None:
    query = (
      select(DBBook, DBBookAuthor, DBBookCover)
      .join(DBBookAuthor, DBBookAuthor.book_id == DBBook.id, isouter = True)
      .join(DBBookCover, DBBookCover.id == DBBook.cover_image_id, isouter = True)
      .where(DBBook.id == id)
    )
    result = session.exec(query).first()
    if result is None:
      return None
    db_book, book_author, db_cover = result
    return Book(
      id = db_book.id,
      title = db_book.title,
      author_id = book_author.author_id if book_author else None,
      description = db_book.description,
      isbn = db_book.isbn,
      publication_date = db_book.publication_date,
      cover_image = CoverImage(id = db_cover.id, url = db_cover.url) if db_cover else None,
      created_at = db_book.created_at,
      updated_at = db_book.updated_at,
      deleted_at = db_book.deleted_at
    )
