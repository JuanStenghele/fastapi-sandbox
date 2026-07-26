from datetime import datetime
from uuid import UUID
from sqlalchemy import func
from sqlmodel import select, update, Session
from db_schema.author_db import Author as DBAuthor
from db_schema.book_author_db import BookAuthor as DBBookAuthor
from objects.author import Author


class AuthorDAL():
  def create_author(self, session: Session, author: Author) -> Author:
    db_author = DBAuthor(
      id = author.id,
      name = author.name,
      created_at = author.created_at,
      updated_at = author.updated_at,
      deleted_at = author.deleted_at
    )
    session.add(db_author)
    return author

  def get_author(self, session: Session, id: UUID) -> Author | None:
    query = select(DBAuthor).where(DBAuthor.id == id, DBAuthor.deleted_at == None)
    result = session.exec(query).first()
    if result is None:
      return None
    return Author.model_validate(result)

  def get_authors(self, session: Session, search_term: str | None, limit: int, offset: int) -> list[Author]:
    query = select(DBAuthor).where(DBAuthor.deleted_at == None)
    if search_term:
      query = query.filter(DBAuthor.name.icontains(search_term, autoescape = True))
    query = query.order_by(DBAuthor.id.asc()).limit(limit).offset(offset)
    results = session.exec(query).all()
    return [Author.model_validate(result) for result in results]

  def get_authors_by_ids(self, session: Session, ids: list) -> list[Author]:
    query = select(DBAuthor).where(DBAuthor.id.in_(ids), DBAuthor.deleted_at == None)
    results = session.exec(query).all()
    return [Author.model_validate(result) for result in results]

  def get_author_ids_with_books(self, session: Session, author_ids: list) -> list:
    query = select(DBBookAuthor.author_id).where(
      DBBookAuthor.author_id.in_(author_ids),
      DBBookAuthor.deleted_at == None
    )
    results = session.exec(query).all()
    return [result for result in results]

  def update_author(self, session: Session, id: UUID, name: str, updated_at: datetime) -> Author | None:
    query = select(DBAuthor).where(DBAuthor.id == id, DBAuthor.deleted_at == None)
    result = session.exec(query).first()
    if result is None:
      return None
    result.name = name
    result.updated_at = updated_at
    session.add(result)
    return Author.model_validate(result)

  def soft_delete_authors(self, session: Session, ids: list, deleted_at: datetime) -> None:
    stmt = update(DBAuthor).where(DBAuthor.id.in_(ids)).values(deleted_at = deleted_at)
    session.exec(stmt)

  def count_authors(self, session: Session, search_term: str | None) -> int:
    query = select(func.count()).select_from(DBAuthor).where(DBAuthor.deleted_at == None)
    if search_term:
      query = query.filter(DBAuthor.name.icontains(search_term, autoescape = True))
    return session.exec(query).one()
