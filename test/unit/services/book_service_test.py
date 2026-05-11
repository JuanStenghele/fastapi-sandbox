import pytest

from datetime import datetime, timezone
from unittest.mock import MagicMock
from uuid import uuid4
from services.book_service import BookService
from services.cover_image_service import CoverImageService
from dal.book_dal import BookDAL
from objects.book import Book
from sqlmodel import Session


class TestBookService():
  def test_create_book_success(self):
    book_title = 'Harry Potter'
    now = datetime.now(timezone.utc)
    book_dal_mock = MagicMock(spec = BookDAL)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    session_mock = MagicMock(spec = Session)
    instance = BookService(book_dal_mock, cover_image_service_mock)
    book_result = instance.create_book(session_mock, book_title, None, None, None)
    assert book_result.id is not None
    assert book_result.title == book_title

  def test_create_book_fail(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    book_dal_mock.create_book.side_effect = Exception('error')
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    session_mock = MagicMock(spec = Session)
    instance = BookService(book_dal_mock, cover_image_service_mock)
    with pytest.raises(Exception) as e:
      instance.create_book(session_mock, 'Harry Potter', None, None, None)
    assert str(e.value) == 'error'

  def test_get_book_success(self):
    now = datetime.now(timezone.utc)
    book_id = uuid4()
    book_title = 'Harry Potter'
    book_dal_mock = MagicMock(spec = BookDAL)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_dal_mock.get_book.return_value = Book(id = book_id, title = book_title, created_at = now, updated_at = now)
    session_mock = MagicMock(spec = Session)
    instance = BookService(book_dal_mock, cover_image_service_mock)
    book_result = instance.get_book(session_mock, book_id)
    assert book_result is not None
    assert book_result.id == book_id
    assert book_result.title == book_title

  def test_get_book_fail(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    book_dal_mock.get_book.side_effect = Exception('error')
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    session_mock = MagicMock(spec = Session)
    instance = BookService(book_dal_mock, cover_image_service_mock)
    with pytest.raises(Exception) as e:
      instance.get_book(session_mock, uuid4())
    assert str(e.value) == 'error'
