from sqlmodel import Session
from db_schema.book_cover_db import BookCover as DBBookCover
from objects.book_cover import BookCover


class BookCoverDAL():
  def create_book_cover(self, session: Session, book_cover: BookCover) -> BookCover:
    db_book_cover = DBBookCover(
      id = book_cover.id,
      source = book_cover.source,
      url = book_cover.url,
      created_at = book_cover.created_at,
      updated_at = book_cover.updated_at
    )
    session.add(db_book_cover)
    return book_cover
