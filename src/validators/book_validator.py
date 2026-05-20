from dal.author_dal import AuthorDAL
from objects.book_creation import BookCreationRequest
from objects.error import ValidationError
from sqlmodel import Session


class BookValidator():
  def __init__(self, author_dal: AuthorDAL) -> None:
    self.author_dal = author_dal

  def validate_creation(self, session: Session, request: BookCreationRequest) -> None:
    if self.author_dal.get_author(session, request.author_id) is None:
      raise ValidationError("AUTHOR_NOT_FOUND")
