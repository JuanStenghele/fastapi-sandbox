import pytest


from datetime import datetime, timezone
from unittest.mock import MagicMock
from uuid import uuid4
from services.book_service import BookService
from services.cover_image_service import CoverImageService
from dal.book_dal import BookDAL
from objects.book import Book
from objects.book_creation import BookCreationRequest
from validators.book_validator import BookValidator
from sqlmodel import Session


class TestBookService():
  def test_create_book_success(self):
    book_title = 'Harry Potter'
    author_id = uuid4()
    book_dal_mock = MagicMock(spec = BookDAL)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    session_mock = MagicMock(spec = Session)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock)
    request = BookCreationRequest(title = book_title, author_id = author_id)
    result = instance.create_book(session_mock, request)
    assert result.id is not None
    assert result.title == book_title
    assert result.author_id == author_id
    book_validator_mock.validate_creation.assert_called_once()

  def test_create_book_fail(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    book_dal_mock.create_book.side_effect = Exception('error')
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    session_mock = MagicMock(spec = Session)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock)
    request = BookCreationRequest(title = 'Harry Potter', author_id = uuid4())
    with pytest.raises(Exception) as exc_info:
      instance.create_book(session_mock, request)
    assert str(exc_info.value) == 'error'

  def test_create_book_validation_fail(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    book_validator_mock.validate_creation.side_effect = Exception('validation error')
    session_mock = MagicMock(spec = Session)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock)
    request = BookCreationRequest(title = 'Harry Potter', author_id = uuid4())
    with pytest.raises(Exception) as exc_info:
      instance.create_book(session_mock, request)
    assert str(exc_info.value) == 'validation error'
    book_dal_mock.create_book.assert_not_called()

  def test_get_book_success(self):
    now = datetime.now(timezone.utc)
    book_id = uuid4()
    book_title = 'Harry Potter'
    book_dal_mock = MagicMock(spec = BookDAL)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    book_dal_mock.get_book.return_value = Book(id = book_id, title = book_title, author_id = uuid4(), created_at = now, updated_at = now)
    session_mock = MagicMock(spec = Session)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock)
    result = instance.get_book(session_mock, book_id)
    assert result is not None
    assert result.id == book_id
    assert result.title == book_title

  def test_get_book_fail(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    book_dal_mock.get_book.side_effect = Exception('error')
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    session_mock = MagicMock(spec = Session)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock)
    with pytest.raises(Exception) as exc_info:
      instance.get_book(session_mock, uuid4())
    assert str(exc_info.value) == 'error'
