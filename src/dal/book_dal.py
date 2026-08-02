from uuid import UUID
from datetime import date, datetime
from sqlalchemy import func
from sqlmodel import select, update, Session
from db_schema.book_author_db import BookAuthor as DBBookAuthor
from db_schema.stored_object_db import StoredObject as DBStoredObject
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

  def update_book(self, session: Session, id: UUID, title: str | None, author_id: UUID | None, description: str | None, isbn: str | None, publication_date: date | None, updated_at: datetime) -> Book | None:
    query = select(DBBook).where(DBBook.id == id, DBBook.deleted_at == None)
    db_book = session.exec(query).first()
    if db_book is None:
      return None
    if title is not None:
      db_book.title = title
    if description is not None:
      db_book.description = description
    if isbn is not None:
      db_book.isbn = isbn
    if publication_date is not None:
      db_book.publication_date = publication_date
    db_book.updated_at = updated_at
    session.add(db_book)
    if author_id is not None:
      session.exec(update(DBBookAuthor).where(DBBookAuthor.book_id == id).values(deleted_at = updated_at))
      db_book_author = DBBookAuthor(
        book_id = id,
        author_id = author_id,
        created_at = updated_at,
      )
      session.add(db_book_author)
    session.flush()
    return self.get_book(session, id)

  def get_book(self, session: Session, id: UUID) -> Book | None:
    query = (
      select(DBBook, DBBookAuthor, DBStoredObject)
      .join(DBBookAuthor, (DBBookAuthor.book_id == DBBook.id) & (DBBookAuthor.deleted_at == None), isouter = True)
      .join(DBStoredObject, (DBStoredObject.id == DBBook.cover_image_stored_object_id) & (DBStoredObject.deleted_at == None), isouter = True)
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
      cover_image = CoverImage(book_id = db_book.id, url = db_cover.public_url) if db_cover else None,
      created_at = db_book.created_at,
      updated_at = db_book.updated_at,
      deleted_at = db_book.deleted_at
    )

  def get_books(self, session: Session, limit: int, offset: int, ids: list | None = None, search_term: str | None = None) -> list[Book]:
    query = (
      select(DBBook, DBBookAuthor, DBStoredObject)
      .join(DBBookAuthor, (DBBookAuthor.book_id == DBBook.id) & (DBBookAuthor.deleted_at == None), isouter = True)
      .join(DBStoredObject, (DBStoredObject.id == DBBook.cover_image_stored_object_id) & (DBStoredObject.deleted_at == None), isouter = True)
      .where(DBBook.deleted_at == None)
    )
    if ids is not None:
      query = query.where(DBBook.id.in_(ids))
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
        cover_image = CoverImage(book_id = db_book.id, url = db_cover.public_url) if db_cover else None,
        created_at = db_book.created_at,
        updated_at = db_book.updated_at,
        deleted_at = db_book.deleted_at
      )
      for db_book, book_author, db_cover in results
    ]

  def count_books(self, session: Session, search_term: str | None) -> int:
    query = select(func.count()).select_from(DBBook).where(DBBook.deleted_at == None)
    if search_term:
      query = query.filter(DBBook.title.icontains(search_term, autoescape = True))
    return session.exec(query).one()

  def update_book_cover_stored_object_id(self, session: Session, id: UUID, stored_object_id: UUID, updated_at: datetime) -> None:
    query = update(DBBook).where(DBBook.id == id).values(cover_image_stored_object_id = stored_object_id, updated_at = updated_at)
    session.exec(query)

  def delete_book_cover_stored_object_ids(self, session: Session, ids: list, updated_at: datetime) -> None:
    query = update(DBBook).where(DBBook.id.in_(ids)).values(cover_image_stored_object_id = None, updated_at = updated_at)
    session.exec(query)

  def soft_delete_books(self, session: Session, ids: list, deleted_at: datetime) -> None:
    query = update(DBBook).where(DBBook.id.in_(ids)).values(deleted_at = deleted_at)
    session.exec(query)
    query = update(DBBookAuthor).where(DBBookAuthor.book_id.in_(ids)).values(deleted_at = deleted_at)
    session.exec(query)
