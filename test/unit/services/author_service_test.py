import pytest


from datetime import datetime, timezone
from unittest.mock import MagicMock
from uuid import uuid4
from services.author_service import AuthorService
from dal.author_dal import AuthorDAL
from objects.author import Author, GetAuthorsResult, GetAuthorsPaginatedResult
from objects.error import ValidationError
from sqlmodel import Session


class TestAuthorService():
  def test_create_author_success(self):
    author_name = 'J. K. Rowling'
    author_dal_mock = MagicMock(spec = AuthorDAL)
    author_dal_mock.create_author.return_value = Author(
      id = uuid4(),
      name = author_name,
      created_at = datetime.now(timezone.utc),
      updated_at = datetime.now(timezone.utc),
      deleted_at = None
    )
    session_mock = MagicMock(spec = Session)
    instance = AuthorService(author_dal_mock)
    author_result = instance.create_author(session_mock, author_name)
    assert author_result.id is not None
    assert author_result.name == author_name
    assert author_result.created_at is not None
    assert author_result.updated_at is not None
    assert author_result.deleted_at is None

  def test_create_author_fail(self):
    author_name = 'J. K. Rowling'
    author_dal_mock = MagicMock(spec = AuthorDAL)
    author_dal_mock.create_author.side_effect = Exception('error')
    session_mock = MagicMock(spec = Session)
    instance = AuthorService(author_dal_mock)
    with pytest.raises(Exception) as e:
      instance.create_author(session_mock, author_name)
    assert str(e.value) == 'error'

  def test_get_authors_success(self):
    now = datetime.now(timezone.utc)
    author_dal_mock = MagicMock(spec = AuthorDAL)
    session_mock = MagicMock(spec = Session)
    author_1 = Author(id = uuid4(), name = 'J. K. Rowling', created_at = now, updated_at = now, deleted_at = None)
    author_2 = Author(id = uuid4(), name = 'J. R. R. Tolkien', created_at = now, updated_at = now, deleted_at = None)
    author_dal_mock.count_authors.return_value = 2
    author_dal_mock.get_authors.return_value = [author_1, author_2]
    instance = AuthorService(author_dal_mock)
    result = instance.get_authors(session_mock, None, 10, 0)
    assert result.authors == [author_1, author_2]
    assert result.total_authors == 2
    author_dal_mock.count_authors.assert_called_once()
    author_dal_mock.get_authors.assert_called_once_with(session_mock, None, 10, 0)

  def test_get_authors_success_with_search_term(self):
    now = datetime.now(timezone.utc)
    author_dal_mock = MagicMock(spec = AuthorDAL)
    session_mock = MagicMock(spec = Session)
    author = Author(id = uuid4(), name = 'J. K. Rowling', created_at = now, updated_at = now, deleted_at = None)
    author_dal_mock.count_authors.return_value = 1
    author_dal_mock.get_authors.return_value = [author]
    instance = AuthorService(author_dal_mock)
    result = instance.get_authors(session_mock, 'Rowling', 10, 0)
    assert len(result.authors) == 1
    assert result.authors[0].name == 'J. K. Rowling'
    assert result.total_authors == 1
    author_dal_mock.get_authors.assert_called_once_with(session_mock, 'Rowling', 10, 0)

  def test_get_authors_empty_results(self):
    author_dal_mock = MagicMock(spec = AuthorDAL)
    session_mock = MagicMock(spec = Session)
    author_dal_mock.count_authors.return_value = 0
    author_dal_mock.get_authors.return_value = []
    instance = AuthorService(author_dal_mock)
    result = instance.get_authors(session_mock, None, 10, 0)
    assert result.authors == []
    assert result.total_authors == 0

  def test_get_authors_invalid_offset(self):
    author_dal_mock = MagicMock(spec = AuthorDAL)
    session_mock = MagicMock(spec = Session)
    instance = AuthorService(author_dal_mock)
    with pytest.raises(ValidationError) as exc_info:
      instance.get_authors(session_mock, None, 10, -1)
    assert exc_info.value.detail == 'INVALID_OFFSET'

  def test_get_authors_fail(self):
    author_dal_mock = MagicMock(spec = AuthorDAL)
    author_dal_mock.count_authors.side_effect = Exception('error')
    session_mock = MagicMock(spec = Session)
    instance = AuthorService(author_dal_mock)
    with pytest.raises(Exception) as exc_info:
      instance.get_authors(session_mock, None, 10, 0)
    assert str(exc_info.value) == 'error'

  def test_get_authors_paginated_success(self):
    now = datetime.now(timezone.utc)
    author_dal_mock = MagicMock(spec = AuthorDAL)
    session_mock = MagicMock(spec = Session)
    author_1 = Author(id = uuid4(), name = 'J. K. Rowling', created_at = now, updated_at = now, deleted_at = None)
    author_2 = Author(id = uuid4(), name = 'J. R. R. Tolkien', created_at = now, updated_at = now, deleted_at = None)
    author_dal_mock.count_authors.return_value = 5
    author_dal_mock.get_authors.return_value = [author_1, author_2]
    instance = AuthorService(author_dal_mock)
    result = instance.get_authors_paginated(session_mock, None, 1, 10)
    assert result.authors == [author_1, author_2]
    assert result.total_authors == 5
    assert result.total_pages == 1
    assert result.current_page == 1
    assert result.page_size == 10
    author_dal_mock.count_authors.assert_called_once()
    author_dal_mock.get_authors.assert_called_once_with(session_mock, None, 10, 0)

  def test_get_authors_paginated_invalid_page_size(self):
    author_dal_mock = MagicMock(spec = AuthorDAL)
    session_mock = MagicMock(spec = Session)
    instance = AuthorService(author_dal_mock)
    with pytest.raises(ValidationError) as exc_info:
      instance.get_authors_paginated(session_mock, None, 1, 7)
    assert exc_info.value.detail == 'INVALID_PAGE_SIZE'

  def test_get_authors_paginated_invalid_page(self):
    author_dal_mock = MagicMock(spec = AuthorDAL)
    session_mock = MagicMock(spec = Session)
    instance = AuthorService(author_dal_mock)
    with pytest.raises(ValidationError) as exc_info:
      instance.get_authors_paginated(session_mock, None, 0, 10)
    assert exc_info.value.detail == 'INVALID_PAGE'

  def test_get_authors_paginated_fail(self):
    author_dal_mock = MagicMock(spec = AuthorDAL)
    author_dal_mock.count_authors.side_effect = Exception('error')
    session_mock = MagicMock(spec = Session)
    instance = AuthorService(author_dal_mock)
    with pytest.raises(Exception) as exc_info:
      instance.get_authors_paginated(session_mock, None, 1, 10)
    assert str(exc_info.value) == 'error'
