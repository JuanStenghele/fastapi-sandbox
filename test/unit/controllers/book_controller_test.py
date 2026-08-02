import pytest

from unittest.mock import MagicMock
from uuid import uuid4
from fastapi import HTTPException
from objects.book import BookCreationHTTPRequest, BookUpdateHTTPRequest
from objects.auth import AuthClaims
from objects.error import ValidationError
from services.book_service import BookService
from services.cover_image_service import CoverImageService
from sqlalchemy.orm import Session
from logging import Logger
from controllers.book_controller import create_books, get_book, get_books, delete_books, update_book, delete_book_cover, update_book_cover


class TestBookController():
  def test_create_book_500_error(self):
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

  def test_delete_books_500_error(self):
    claims_mock = MagicMock(spec = AuthClaims)
    book_service_mock = MagicMock(spec = BookService)
    book_service_mock.delete_books.side_effect = Exception('error')
    session_mock = MagicMock(spec = Session)
    logger_mock = MagicMock(spec = Logger)
    ids = [uuid4()]
    with pytest.raises(HTTPException) as e:
      delete_books(
        ids = ids,
        _ = claims_mock,
        book_service = book_service_mock,
        session = session_mock,
        logger = logger_mock
      )
    assert e.value.status_code == 500
    assert e.value.detail == 'UNKNOWN_ERROR'
    assert book_service_mock.delete_books.call_count == 1

  def test_delete_books_400_error(self):
    claims_mock = MagicMock(spec = AuthClaims)
    book_service_mock = MagicMock(spec = BookService)
    book_service_mock.delete_books.side_effect = ValidationError(detail = "BOOKS_NOT_FOUND")
    session_mock = MagicMock(spec = Session)
    logger_mock = MagicMock(spec = Logger)
    ids = [uuid4()]
    with pytest.raises(HTTPException) as e:
      delete_books(
        ids = ids,
        _ = claims_mock,
        book_service = book_service_mock,
        session = session_mock,
        logger = logger_mock
      )
    assert e.value.status_code == 400
    assert e.value.detail == 'BOOKS_NOT_FOUND'
    assert book_service_mock.delete_books.call_count == 1

  def test_update_book_500_error(self):
    claims_mock = MagicMock(spec = AuthClaims)
    book_service_mock = MagicMock(spec = BookService)
    book_service_mock.update_book.side_effect = Exception('error')
    session_mock = MagicMock(spec = Session)
    logger_mock = MagicMock(spec = Logger)
    book_request = BookUpdateHTTPRequest(title = 'New Title')
    with pytest.raises(HTTPException) as e:
      update_book(
        id = uuid4(),
        book = book_request,
        _ = claims_mock,
        book_service = book_service_mock,
        session = session_mock,
        logger = logger_mock
      )
    assert e.value.status_code == 500
    assert e.value.detail == 'UNKNOWN_ERROR'
    assert book_service_mock.update_book.call_count == 1

  def test_update_book_400_error(self):
    claims_mock = MagicMock(spec = AuthClaims)
    book_service_mock = MagicMock(spec = BookService)
    book_service_mock.update_book.side_effect = ValidationError(detail = "AUTHOR_NOT_FOUND")
    session_mock = MagicMock(spec = Session)
    logger_mock = MagicMock(spec = Logger)
    book_request = BookUpdateHTTPRequest(author_id = uuid4())
    with pytest.raises(HTTPException) as e:
      update_book(
        id = uuid4(),
        book = book_request,
        _ = claims_mock,
        book_service = book_service_mock,
        session = session_mock,
        logger = logger_mock
      )
    assert e.value.status_code == 400
    assert e.value.detail == 'AUTHOR_NOT_FOUND'
    assert book_service_mock.update_book.call_count == 1

  def test_update_book_404_error(self):
    claims_mock = MagicMock(spec = AuthClaims)
    book_service_mock = MagicMock(spec = BookService)
    book_service_mock.update_book.return_value = None
    session_mock = MagicMock(spec = Session)
    logger_mock = MagicMock(spec = Logger)
    book_request = BookUpdateHTTPRequest(title = 'New Title')
    with pytest.raises(HTTPException) as e:
      update_book(
        id = uuid4(),
        book = book_request,
        _ = claims_mock,
        book_service = book_service_mock,
        session = session_mock,
        logger = logger_mock
      )
    assert e.value.status_code == 404
    assert e.value.detail == 'BOOK_NOT_FOUND'
    assert book_service_mock.update_book.call_count == 1

  def test_delete_book_cover_500_error(self):
    claims_mock = MagicMock(spec = AuthClaims)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    cover_image_service_mock.delete_book_covers.side_effect = Exception('error')
    session_mock = MagicMock(spec = Session)
    logger_mock = MagicMock(spec = Logger)
    with pytest.raises(HTTPException) as e:
      delete_book_cover(
        id = uuid4(),
        _ = claims_mock,
        cover_image_service = cover_image_service_mock,
        session = session_mock,
        logger = logger_mock
      )
    assert e.value.status_code == 500
    assert e.value.detail == 'UNKNOWN_ERROR'
    assert cover_image_service_mock.delete_book_covers.call_count == 1

  def test_delete_book_cover_400_error(self):
    claims_mock = MagicMock(spec = AuthClaims)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    cover_image_service_mock.delete_book_covers.side_effect = ValidationError(detail = "BOOKS_NOT_FOUND: id")
    session_mock = MagicMock(spec = Session)
    logger_mock = MagicMock(spec = Logger)
    with pytest.raises(HTTPException) as e:
      delete_book_cover(
        id = uuid4(),
        _ = claims_mock,
        cover_image_service = cover_image_service_mock,
        session = session_mock,
        logger = logger_mock
      )
    assert e.value.status_code == 404
    assert e.value.detail == 'BOOKS_NOT_FOUND: id'
    assert cover_image_service_mock.delete_book_covers.call_count == 1

  def test_update_book_cover_500_error(self):
    claims_mock = MagicMock(spec = AuthClaims)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    cover_image_service_mock.update_book_cover.side_effect = Exception('error')
    session_mock = MagicMock(spec = Session)
    logger_mock = MagicMock(spec = Logger)
    cover_image_mock = MagicMock()
    cover_image_mock.file = MagicMock()
    cover_image_mock.content_type = "image/jpeg"
    cover_image_mock.size = 1024
    with pytest.raises(HTTPException) as e:
      update_book_cover(
        id = uuid4(),
        cover_image = cover_image_mock,
        _ = claims_mock,
        cover_image_service = cover_image_service_mock,
        session = session_mock,
        logger = logger_mock
      )
    assert e.value.status_code == 500
    assert e.value.detail == 'UNKNOWN_ERROR'
    assert cover_image_service_mock.update_book_cover.call_count == 1

  def test_update_book_cover_404_error(self):
    claims_mock = MagicMock(spec = AuthClaims)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    cover_image_service_mock.update_book_cover.side_effect = ValidationError(detail = "BOOKS_NOT_FOUND: some-uuid")
    session_mock = MagicMock(spec = Session)
    logger_mock = MagicMock(spec = Logger)
    cover_image_mock = MagicMock()
    cover_image_mock.file = MagicMock()
    cover_image_mock.content_type = "image/jpeg"
    cover_image_mock.size = 1024
    with pytest.raises(HTTPException) as e:
      update_book_cover(
        id = uuid4(),
        cover_image = cover_image_mock,
        _ = claims_mock,
        cover_image_service = cover_image_service_mock,
        session = session_mock,
        logger = logger_mock
      )
    assert e.value.status_code == 404
    assert e.value.detail == 'BOOKS_NOT_FOUND: some-uuid'
    assert cover_image_service_mock.update_book_cover.call_count == 1
