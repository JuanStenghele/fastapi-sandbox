from uuid import UUID
from sqlalchemy import func
from sqlmodel import select, Session
from db_schema.author_db import Author as DBAuthor
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
    query = select(DBAuthor).where(DBAuthor.id == id)
    result = session.exec(query).first()
    if result is None:
      return None
    return Author.model_validate(result)

  def get_authors(self, session: Session, search_term: str | None, limit: int, offset: int) -> list[Author]:
    query = select(DBAuthor)
    if search_term:
      query = query.filter(DBAuthor.name.icontains(search_term, autoescape = True))
    query = query.order_by(DBAuthor.id.asc()).limit(limit).offset(offset)
    results = session.exec(query).all()
    return [Author.model_validate(result) for result in results]

  def count_authors(self, session: Session, search_term: str | None) -> int:
    query = select(func.count()).select_from(DBAuthor)
    if search_term:
      query = query.filter(DBAuthor.name.icontains(search_term, autoescape = True))
    return session.exec(query).one()
