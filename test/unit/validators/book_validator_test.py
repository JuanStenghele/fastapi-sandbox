import pytest


from unittest.mock import MagicMock
from uuid import uuid4
from dal.author_dal import AuthorDAL
from dal.book_dal import BookDAL
from objects.author import Author
from objects.book_creation import BookCreationRequest
from objects.display import BookUpdateHTTPRequest
from objects.error import ValidationError
from sqlmodel import Session
from validators.book_validator import BookValidator
from objects.book import Book


class TestBookValidator():
  def test_validate_creation_success(self):
    author_dal_mock = MagicMock(spec = AuthorDAL)
    author_dal_mock.get_author.return_value = MagicMock(spec = Author)
    book_dal_mock = MagicMock(spec = BookDAL)
    session_mock = MagicMock(spec = Session)
    request = BookCreationRequest(title = 'Harry Potter', author_id = uuid4())
    instance = BookValidator(author_dal_mock, book_dal_mock)
    instance.validate_creation(session_mock, request)
    author_dal_mock.get_author.assert_called_once_with(session_mock, request.author_id)

  def test_validate_creation_author_not_found(self):
    author_dal_mock = MagicMock(spec = AuthorDAL)
    author_dal_mock.get_author.return_value = None
    book_dal_mock = MagicMock(spec = BookDAL)
    session_mock = MagicMock(spec = Session)
    request = BookCreationRequest(title = 'Harry Potter', author_id = uuid4())
    instance = BookValidator(author_dal_mock, book_dal_mock)
    with pytest.raises(ValidationError) as exc_info:
      instance.validate_creation(session_mock, request)
    assert exc_info.value.detail == "AUTHOR_NOT_FOUND"

  def test_validate_deletion_success(self):
    book_id = uuid4()
    book_dal_mock = MagicMock(spec = BookDAL)
    book_dal_mock.get_books_by_ids.return_value = [MagicMock(spec = Book, id = book_id)]
    author_dal_mock = MagicMock(spec = AuthorDAL)
    session_mock = MagicMock(spec = Session)
    instance = BookValidator(author_dal_mock, book_dal_mock)
    instance.validate_deletion(session_mock, [book_id])
    book_dal_mock.get_books_by_ids.assert_called_once_with(session_mock, [book_id])

  def test_validate_deletion_books_not_found(self):
    book_id = uuid4()
    book_dal_mock = MagicMock(spec = BookDAL)
    book_dal_mock.get_books_by_ids.return_value = []
    author_dal_mock = MagicMock(spec = AuthorDAL)
    session_mock = MagicMock(spec = Session)
    instance = BookValidator(author_dal_mock, book_dal_mock)
    with pytest.raises(ValidationError) as exc_info:
      instance.validate_deletion(session_mock, [book_id])
    assert exc_info.value.detail == f"BOOKS_NOT_FOUND: ['{str(book_id)}']"

  def test_validate_deletion_empty_ids(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    author_dal_mock = MagicMock(spec = AuthorDAL)
    session_mock = MagicMock(spec = Session)
    instance = BookValidator(author_dal_mock, book_dal_mock)
    with pytest.raises(ValidationError) as exc_info:
      instance.validate_deletion(session_mock, [])
    assert exc_info.value.detail == "INVALID_BOOK_IDS_COUNT"

  def test_validate_deletion_too_many_ids(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    author_dal_mock = MagicMock(spec = AuthorDAL)
    session_mock = MagicMock(spec = Session)
    instance = BookValidator(author_dal_mock, book_dal_mock)
    with pytest.raises(ValidationError) as exc_info:
      instance.validate_deletion(session_mock, [uuid4() for _ in range(101)])
    assert exc_info.value.detail == "INVALID_BOOK_IDS_COUNT"

  def test_validate_update_success(self):
    author_dal_mock = MagicMock(spec = AuthorDAL)
    book_dal_mock = MagicMock(spec = BookDAL)
    session_mock = MagicMock(spec = Session)
    request = BookUpdateHTTPRequest(title = 'New Title')
    instance = BookValidator(author_dal_mock, book_dal_mock)
    instance.validate_update(session_mock, request)

  def test_validate_update_author_not_found(self):
    author_dal_mock = MagicMock(spec = AuthorDAL)
    author_dal_mock.get_author.return_value = None
    book_dal_mock = MagicMock(spec = BookDAL)
    session_mock = MagicMock(spec = Session)
    request = BookUpdateHTTPRequest(author_id = uuid4())
    instance = BookValidator(author_dal_mock, book_dal_mock)
    with pytest.raises(ValidationError) as exc_info:
      instance.validate_update(session_mock, request)
    assert exc_info.value.detail == "AUTHOR_NOT_FOUND"

  def test_validate_update_author_exists(self):
    author_id = uuid4()
    author_dal_mock = MagicMock(spec = AuthorDAL)
    author_dal_mock.get_author.return_value = MagicMock(spec = Author)
    book_dal_mock = MagicMock(spec = BookDAL)
    session_mock = MagicMock(spec = Session)
    request = BookUpdateHTTPRequest(author_id = author_id)
    instance = BookValidator(author_dal_mock, book_dal_mock)
    instance.validate_update(session_mock, request)
    author_dal_mock.get_author.assert_called_once_with(session_mock, author_id)

  def test_validate_cover_deletion_success(self):
    book_id = uuid4()
    book_dal_mock = MagicMock(spec = BookDAL)
    book_dal_mock.get_book.return_value = MagicMock(spec = Book)
    author_dal_mock = MagicMock(spec = AuthorDAL)
    session_mock = MagicMock(spec = Session)
    instance = BookValidator(author_dal_mock, book_dal_mock)
    instance.validate_cover_deletion(session_mock, book_id)
    book_dal_mock.get_book.assert_called_once_with(session_mock, book_id)

  def test_validate_cover_deletion_not_found(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    book_dal_mock.get_book.return_value = None
    author_dal_mock = MagicMock(spec = AuthorDAL)
    session_mock = MagicMock(spec = Session)
    instance = BookValidator(author_dal_mock, book_dal_mock)
    with pytest.raises(ValidationError) as exc_info:
      instance.validate_cover_deletion(session_mock, uuid4())
    assert exc_info.value.detail == "BOOK_NOT_FOUND"
