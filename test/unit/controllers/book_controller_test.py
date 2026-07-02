import pytest

from unittest.mock import MagicMock
from uuid import uuid4
from fastapi import HTTPException
from objects.display import BookCreationHTTPRequest
from objects.auth import AuthClaims
from objects.error import ValidationError
from services.book_service import BookService
from sqlalchemy.orm import Session
from logging import Logger


class TestBookController():
  def test_create_book_500_error(self):
    from controllers.book_controller import create_books
    http_request = BookCreationHTTPRequest(title = 'Harry Potter', author_id = uuid4())
    claims_mock = MagicMock(spec = AuthClaims)
    book_service_mock = MagicMock(spec = BookService)
    book_service_mock.create_book.side_effect = Exception('error')
    session_mock = MagicMock(spec = Session)
    logger_mock = MagicMock(spec = Logger)
    with pytest.raises(HTTPException) as e:
      create_books(
        http_request = http_request,
        _ = claims_mock,
        book_service = book_service_mock,
        session = session_mock,
        logger = logger_mock
      )
    assert e.value.status_code == 500
    assert e.value.detail == 'UNKNOWN_ERROR'
    assert book_service_mock.create_book.call_count == 1

  def test_get_book_500_error(self):
    from controllers.book_controller import get_book
    claims_mock = MagicMock(spec = AuthClaims)
    book_service_mock = MagicMock(spec = BookService)
    book_service_mock.get_book.side_effect = Exception('error')
    session_mock = MagicMock(spec = Session)
    logger_mock = MagicMock(spec = Logger)
    with pytest.raises(HTTPException) as e:
      get_book(
        id = uuid4(),
        _ = claims_mock,
        book_service = book_service_mock,
        session = session_mock,
        logger = logger_mock
      )
    assert e.value.status_code == 500
    assert e.value.detail == 'UNKNOWN_ERROR'
    assert book_service_mock.get_book.call_count == 1

  def test_get_books_500_error(self):
    from controllers.book_controller import get_books
    claims_mock = MagicMock(spec = AuthClaims)
    book_service_mock = MagicMock(spec = BookService)
    book_service_mock.get_books_paginated.side_effect = Exception('error')
    session_mock = MagicMock(spec = Session)
    logger_mock = MagicMock(spec = Logger)
    with pytest.raises(HTTPException) as e:
      get_books(
        search_term = None,
        page = 1,
        page_size = 10,
        _ = claims_mock,
        book_service = book_service_mock,
        session = session_mock,
        logger = logger_mock
      )
    assert e.value.status_code == 500
    assert e.value.detail == 'UNKNOWN_ERROR'
    assert book_service_mock.get_books_paginated.call_count == 1
