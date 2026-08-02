from uuid import UUID
from dal.author_dal import AuthorDAL
from objects.error import ValidationError
from constants import MAX_DELETE_IDS
from sqlmodel import Session


class AuthorValidator():
  def __init__(self, author_dal: AuthorDAL) -> None:
    self.author_dal = author_dal

  def validate_deletion(self, session: Session, author_ids: list) -> None:
    if len(author_ids) == 0 or len(author_ids) > MAX_DELETE_IDS:
      raise ValidationError(detail = "INVALID_AUTHOR_IDS_COUNT")

    existing_authors = self.author_dal.get_authors(session, limit = len(author_ids), offset = 0, ids = author_ids)
    existing_authors_ids = [author.id for author in existing_authors]
    authors_ids_not_found = [id for id in author_ids if id not in existing_authors_ids]
    if len(authors_ids_not_found) != 0:
      raise ValidationError(detail = f"AUTHORS_NOT_FOUND: {', '.join(str(id) for id in authors_ids_not_found)}")

    author_ids_with_books = self.author_dal.get_author_ids_with_books(session, author_ids)
    if len(author_ids_with_books) != 0:
      raise ValidationError(detail = f"AUTHORS_HAVE_BOOKS: {', '.join(str(id) for id in author_ids_with_books)}")
