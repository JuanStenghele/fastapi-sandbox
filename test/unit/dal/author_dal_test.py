import pytest


from datetime import datetime, timezone
from unittest.mock import MagicMock
from uuid import uuid4
from sqlmodel import Session
from objects.author import Author
from dal.author_dal import AuthorDAL


class TestAuthorDal():
  def test_create_author_success(self):
    session_mock = MagicMock(spec = Session)
    author_id = uuid4()
    author_name = 'J. K. Rowling'
    created_at = datetime.now(timezone.utc)
    updated_at = datetime.now(timezone.utc)
    author = Author(
      id = author_id,
      name = author_name,
      created_at = created_at,
      updated_at = updated_at,
      deleted_at = None
    )
    instance = AuthorDAL()
    result = instance.create_author(session_mock, author)
    assert result == author
    added_author = session_mock.add.call_args[0][0]
    assert added_author.id == author_id
    assert added_author.name == author_name
    assert added_author.created_at == created_at
    assert added_author.updated_at == updated_at
    assert added_author.deleted_at is None

  def test_create_author_fail(self):
    session_mock = MagicMock(spec = Session)
    expected_message = 'Test Exception'
    session_mock.add.side_effect = Exception(expected_message)
    author_id = uuid4()
    author_name = 'J. K. Rowling'
    created_at = datetime.now(timezone.utc)
    updated_at = datetime.now(timezone.utc)
    author = Author(
      id = author_id,
      name = author_name,
      created_at = created_at,
      updated_at = updated_at,
      deleted_at = None
    )
    instance = AuthorDAL()
    with pytest.raises(Exception) as exc_info:
      instance.create_author(session_mock, author)
    assert str(exc_info.value) == expected_message
    assert session_mock.add.call_count == 1
