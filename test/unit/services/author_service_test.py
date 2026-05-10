import pytest


from datetime import datetime, timezone
from unittest.mock import MagicMock
from uuid import uuid4
from services.author_service import AuthorService
from dal.author_dal import AuthorDAL
from objects.author import Author
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
