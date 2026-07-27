from datetime import datetime
from uuid import UUID
from sqlmodel import select, update, Session
from db_schema.book_cover_db import BookCover as DBBookCover
from objects.book_cover import BookCover


class BookCoverDAL():
  def create_book_cover(self, session: Session, book_cover: BookCover) -> BookCover:
    db_book_cover = DBBookCover(
      book_id = book_cover.book_id,
      source = book_cover.source,
      url = book_cover.url,
      path = book_cover.path,
      created_at = book_cover.created_at,
      updated_at = book_cover.updated_at
    )
    session.add(db_book_cover)
    return book_cover

  def get_book_cover(self, session: Session, book_id: UUID) -> BookCover | None:
    query = select(DBBookCover).where(DBBookCover.book_id == book_id, DBBookCover.deleted_at == None)
    result = session.exec(query).first()
    if result is None:
      return None
    return BookCover.model_validate(result)

  def get_book_covers_by_ids(self, session: Session, book_ids: list) -> list[BookCover]:
    query = select(DBBookCover).where(DBBookCover.book_id.in_(book_ids), DBBookCover.deleted_at == None)
    results = session.exec(query).all()
    return [BookCover.model_validate(result) for result in results]

  def soft_delete_book_covers(self, session: Session, book_ids: list, deleted_at: datetime) -> None:
    query = update(DBBookCover).where(DBBookCover.book_id.in_(book_ids)).values(deleted_at = deleted_at)
    session.exec(query)

  def update_book_cover(self, session: Session, book_id: UUID, url: str, path: str, updated_at: datetime) -> None:
    query = update(DBBookCover).where(DBBookCover.book_id == book_id).values(url = url, path = path, updated_at = updated_at, deleted_at = None)
    session.exec(query)
