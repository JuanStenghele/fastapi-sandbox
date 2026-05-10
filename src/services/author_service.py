import uuid


from datetime import datetime, timezone
from dal.author_dal import AuthorDAL
from objects.author import Author
from sqlmodel import Session


class AuthorService():
  def __init__(self, author_dal: AuthorDAL) -> None:
    self.author_dal: AuthorDAL = author_dal

  def create_author(self, session: Session, author_name: str) -> Author:
    now = datetime.now(timezone.utc)
    author = Author(
      id = uuid.uuid4(),
      name = author_name,
      created_at = now,
      updated_at = now,
      deleted_at = None
    )
    self.author_dal.create_author(session, author)
    return author
