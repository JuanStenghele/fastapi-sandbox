from uuid import UUID
from datetime import datetime
from sqlalchemy import func
from sqlmodel import select, update, Session
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
      .join(DBBookCover, DBBookCover.book_id == DBBook.id, isouter = True)
      .where(DBBook.id == id, DBBook.deleted_at == None)
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
      cover_image = CoverImage(book_id = db_cover.book_id, url = db_cover.url) if db_cover else None,
      created_at = db_book.created_at,
      updated_at = db_book.updated_at,
      deleted_at = db_book.deleted_at
    )

  def get_books(self, session: Session, search_term: str | None, limit: int, offset: int) -> list[Book]:
    query = (
      select(DBBook, DBBookAuthor, DBBookCover)
      .join(DBBookAuthor, DBBookAuthor.book_id == DBBook.id, isouter = True)
      .join(DBBookCover, DBBookCover.book_id == DBBook.id, isouter = True)
      .where(DBBook.deleted_at == None)
    )
    if search_term:
      query = query.filter(DBBook.title.icontains(search_term, autoescape = True))
    query = query.order_by(DBBook.id.asc()).limit(limit).offset(offset)
    results = session.exec(query).all()
    return [
      Book(
        id = db_book.id,
        title = db_book.title,
        author_id = book_author.author_id if book_author else None,
        description = db_book.description,
        isbn = db_book.isbn,
        publication_date = db_book.publication_date,
        cover_image = CoverImage(book_id = db_cover.book_id, url = db_cover.url) if db_cover else None,
        created_at = db_book.created_at,
        updated_at = db_book.updated_at,
        deleted_at = db_book.deleted_at
      )
      for db_book, book_author, db_cover in results
    ]

  def get_books_by_ids(self, session: Session, ids: list) -> list[Book]:
    query = (
      select(DBBook, DBBookAuthor, DBBookCover)
      .join(DBBookAuthor, DBBookAuthor.book_id == DBBook.id, isouter = True)
      .join(DBBookCover, DBBookCover.book_id == DBBook.id, isouter = True)
      .where(DBBook.id.in_(ids), DBBook.deleted_at == None)
    )
    results = session.exec(query).all()
    return [
      Book(
        id = db_book.id,
        title = db_book.title,
        author_id = book_author.author_id if book_author else None,
        description = db_book.description,
        isbn = db_book.isbn,
        publication_date = db_book.publication_date,
        cover_image = CoverImage(book_id = db_cover.book_id, url = db_cover.url) if db_cover else None,
        created_at = db_book.created_at,
        updated_at = db_book.updated_at,
        deleted_at = db_book.deleted_at
      )
      for db_book, book_author, db_cover in results
    ]

  def soft_delete_books(self, session: Session, ids: list, deleted_at: datetime) -> None:
    query = update(DBBook).where(DBBook.id.in_(ids)).values(deleted_at = deleted_at)
    session.exec(query)
    query = update(DBBookAuthor).where(DBBookAuthor.book_id.in_(ids)).values(deleted_at = deleted_at)
    session.exec(query)
    query = update(DBBookCover).where(DBBookCover.book_id.in_(ids)).values(deleted_at = deleted_at)
    session.exec(query)

  def count_books(self, session: Session, search_term: str | None) -> int:
    query = select(func.count()).select_from(DBBook).where(DBBook.deleted_at == None)
    if search_term:
      query = query.filter(DBBook.title.icontains(search_term, autoescape = True))
    return session.exec(query).one()
