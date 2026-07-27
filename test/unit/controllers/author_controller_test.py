import pytest


from unittest.mock import MagicMock
from uuid import uuid4
from fastapi import HTTPException
from objects.display import AuthorUpsertHTTPRequest
from objects.auth import AuthClaims
from objects.error import ValidationError
from services.author_service import AuthorService
from sqlalchemy.orm import Session
from logging import Logger
from controllers.author_controller import create_author, get_authors, delete_authors, get_author, update_author


class TestAuthorController():
  def test_create_author_500_error(self):
    author = AuthorUpsertHTTPRequest(name = 'J. K. Rowling')
    claims_mock = MagicMock(spec = AuthClaims)
    author_service_mock = MagicMock(spec = AuthorService)
    author_service_mock.create_author.side_effect = Exception('error')
    session_mock = MagicMock(spec = Session)
    logger_mock = MagicMock(spec = Logger)
    with pytest.raises(HTTPException) as e:
      create_author(
        author = author,
        _ = claims_mock,
        author_service = author_service_mock,
        session = session_mock,
        logger = logger_mock
      )
    assert e.value.status_code == 500
    assert e.value.detail == 'UNKNOWN_ERROR'
    assert author_service_mock.create_author.call_count == 1

  def test_get_authors_500_error(self):
    claims_mock = MagicMock(spec = AuthClaims)
    author_service_mock = MagicMock(spec = AuthorService)
    author_service_mock.get_authors_paginated.side_effect = Exception('error')
    session_mock = MagicMock(spec = Session)
    logger_mock = MagicMock(spec = Logger)
    with pytest.raises(HTTPException) as e:
      get_authors(
        search_term = None,
        page = 1,
        page_size = 10,
        _ = claims_mock,
        author_service = author_service_mock,
        session = session_mock,
        logger = logger_mock
      )
    assert e.value.status_code == 500
    assert e.value.detail == 'UNKNOWN_ERROR'
    assert author_service_mock.get_authors_paginated.call_count == 1

  def test_delete_authors_500_error(self):
    claims_mock = MagicMock(spec = AuthClaims)
    author_service_mock = MagicMock(spec = AuthorService)
    author_service_mock.delete_authors.side_effect = Exception('error')
    session_mock = MagicMock(spec = Session)
    logger_mock = MagicMock(spec = Logger)
    ids = [uuid4()]
    with pytest.raises(HTTPException) as e:
      delete_authors(
        ids = ids,
        _ = claims_mock,
        author_service = author_service_mock,
        session = session_mock,
        logger = logger_mock
      )
    assert e.value.status_code == 500
    assert e.value.detail == 'UNKNOWN_ERROR'
    assert author_service_mock.delete_authors.call_count == 1

  def test_delete_authors_400_error(self):
    claims_mock = MagicMock(spec = AuthClaims)
    author_service_mock = MagicMock(spec = AuthorService)
    author_service_mock.delete_authors.side_effect = ValidationError(detail = "AUTHORS_NOT_FOUND")
    session_mock = MagicMock(spec = Session)
    logger_mock = MagicMock(spec = Logger)
    ids = [uuid4()]
    with pytest.raises(HTTPException) as e:
      delete_authors(
        ids = ids,
        _ = claims_mock,
        author_service = author_service_mock,
        session = session_mock,
        logger = logger_mock
      )
    assert e.value.status_code == 400
    assert e.value.detail == 'AUTHORS_NOT_FOUND'
    assert author_service_mock.delete_authors.call_count == 1

  def test_get_author_500_error(self):
    claims_mock = MagicMock(spec = AuthClaims)
    author_service_mock = MagicMock(spec = AuthorService)
    author_service_mock.get_author.side_effect = Exception('error')
    session_mock = MagicMock(spec = Session)
    logger_mock = MagicMock(spec = Logger)
    author_id = uuid4()
    with pytest.raises(HTTPException) as e:
      get_author(
        id = author_id,
        _ = claims_mock,
        author_service = author_service_mock,
        session = session_mock,
        logger = logger_mock
      )
    assert e.value.status_code == 500
    assert e.value.detail == 'UNKNOWN_ERROR'
    assert author_service_mock.get_author.call_count == 1

  def test_update_author_500_error(self):
    author_id = uuid4()
    author = AuthorUpsertHTTPRequest(name = 'Robert Galbraith')
    claims_mock = MagicMock(spec = AuthClaims)
    author_service_mock = MagicMock(spec = AuthorService)
    author_service_mock.update_author.side_effect = Exception('error')
    session_mock = MagicMock(spec = Session)
    logger_mock = MagicMock(spec = Logger)
    with pytest.raises(HTTPException) as e:
      update_author(
        id = author_id,
        author = author,
        _ = claims_mock,
        author_service = author_service_mock,
        session = session_mock,
        logger = logger_mock
      )
    assert e.value.status_code == 500
    assert e.value.detail == 'UNKNOWN_ERROR'
    assert author_service_mock.update_author.call_count == 1

  def test_update_author_400_error(self):
    author_id = uuid4()
    author = AuthorUpsertHTTPRequest(name = 'Robert Galbraith')
    claims_mock = MagicMock(spec = AuthClaims)
    author_service_mock = MagicMock(spec = AuthorService)
    author_service_mock.update_author.side_effect = ValidationError(detail = "AUTHOR_NOT_FOUND")
    session_mock = MagicMock(spec = Session)
    logger_mock = MagicMock(spec = Logger)
    with pytest.raises(HTTPException) as e:
      update_author(
        id = author_id,
        author = author,
        _ = claims_mock,
        author_service = author_service_mock,
        session = session_mock,
        logger = logger_mock
      )
    assert e.value.status_code == 400
    assert e.value.detail == 'AUTHOR_NOT_FOUND'
    assert author_service_mock.update_author.call_count == 1
