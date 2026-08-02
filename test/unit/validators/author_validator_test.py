import pytest


from unittest.mock import MagicMock
from uuid import uuid4
from dal.author_dal import AuthorDAL
from objects.author import Author
from objects.error import ValidationError
from sqlmodel import Session
from validators.author_validator import AuthorValidator


class TestAuthorValidator():
  def test_validate_deletion_success(self):
    author_id = uuid4()
    author_dal_mock = MagicMock(spec = AuthorDAL)
    author_dal_mock.get_authors.return_value = [MagicMock(spec = Author, id = author_id)]
    author_dal_mock.get_author_ids_with_books.return_value = []
    session_mock = MagicMock(spec = Session)
    instance = AuthorValidator(author_dal_mock)
    instance.validate_deletion(session_mock, [author_id])
    author_dal_mock.get_authors.assert_called_once_with(session_mock, limit = 1, offset = 0, ids = [author_id])
    author_dal_mock.get_author_ids_with_books.assert_called_once_with(session_mock, [author_id])

  def test_validate_deletion_authors_not_found(self):
    author_id = uuid4()
    author_dal_mock = MagicMock(spec = AuthorDAL)
    author_dal_mock.get_authors.return_value = []
    session_mock = MagicMock(spec = Session)
    instance = AuthorValidator(author_dal_mock)
    with pytest.raises(ValidationError) as exc_info:
      instance.validate_deletion(session_mock, [author_id])
    assert exc_info.value.detail == f"AUTHORS_NOT_FOUND: {str(author_id)}"

  def test_validate_deletion_authors_have_books(self):
    author_id = uuid4()
    author_dal_mock = MagicMock(spec = AuthorDAL)
    author_dal_mock.get_authors.return_value = [MagicMock(spec = Author, id = author_id)]
    author_dal_mock.get_author_ids_with_books.return_value = [author_id]
    session_mock = MagicMock(spec = Session)
    instance = AuthorValidator(author_dal_mock)
    with pytest.raises(ValidationError) as exc_info:
      instance.validate_deletion(session_mock, [author_id])
    assert exc_info.value.detail == f"AUTHORS_HAVE_BOOKS: {str(author_id)}"

  def test_validate_deletion_empty_ids(self):
    author_dal_mock = MagicMock(spec = AuthorDAL)
    session_mock = MagicMock(spec = Session)
    instance = AuthorValidator(author_dal_mock)
    with pytest.raises(ValidationError) as exc_info:
      instance.validate_deletion(session_mock, [])
    assert exc_info.value.detail == "INVALID_AUTHOR_IDS_COUNT"

  def test_validate_deletion_too_many_ids(self):
    author_dal_mock = MagicMock(spec = AuthorDAL)
    session_mock = MagicMock(spec = Session)
    instance = AuthorValidator(author_dal_mock)
    with pytest.raises(ValidationError) as exc_info:
      instance.validate_deletion(session_mock, [uuid4() for _ in range(101)])
    assert exc_info.value.detail == "INVALID_AUTHOR_IDS_COUNT"
