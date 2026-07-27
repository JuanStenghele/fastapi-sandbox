from dal.author_dal import AuthorDAL
from dal.book_dal import BookDAL
from objects.book_creation import BookCreationRequest
from objects.error import ValidationError
from constants import MAX_DELETE_IDS
from sqlmodel import Session


class BookValidator():
  def __init__(self, author_dal: AuthorDAL, book_dal: BookDAL) -> None:
    self.author_dal = author_dal
    self.book_dal = book_dal

  def validate_creation(self, session: Session, request: BookCreationRequest) -> None:
    if self.author_dal.get_author(session, request.author_id) is None:
      raise ValidationError("AUTHOR_NOT_FOUND")

  def validate_deletion(self, session: Session, book_ids: list) -> None:
    if len(book_ids) == 0 or len(book_ids) > MAX_DELETE_IDS:
      raise ValidationError(detail = "INVALID_BOOK_IDS_COUNT")

    existing_books = self.book_dal.get_books_by_ids(session, book_ids)
    existing_books_ids = [book.id for book in existing_books]
    books_ids_not_found = [id for id in book_ids if id not in existing_books_ids]
    if books_ids_not_found:
      raise ValidationError(detail = f"BOOKS_NOT_FOUND: {[str(id) for id in books_ids_not_found]}")
