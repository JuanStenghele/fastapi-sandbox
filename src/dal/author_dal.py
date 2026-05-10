from sqlmodel import Session
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
