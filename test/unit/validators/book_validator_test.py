import pytest


from unittest.mock import MagicMock
from uuid import uuid4
from dal.author_dal import AuthorDAL
from objects.author import Author
from objects.book_creation import BookCreationRequest
from objects.error import ValidationError
from sqlmodel import Session
from validators.book_validator import BookValidator


class TestBookValidator():
  def test_validate_creation_success(self):
    author_dal_mock = MagicMock(spec = AuthorDAL)
    author_dal_mock.get_author.return_value = MagicMock(spec = Author)
    session_mock = MagicMock(spec = Session)
    request = BookCreationRequest(title = 'Harry Potter', author_id = uuid4())
    instance = BookValidator(author_dal_mock)
    instance.validate_creation(session_mock, request)
    author_dal_mock.get_author.assert_called_once_with(session_mock, request.author_id)

  def test_validate_creation_author_not_found(self):
    author_dal_mock = MagicMock(spec = AuthorDAL)
    author_dal_mock.get_author.return_value = None
    session_mock = MagicMock(spec = Session)
    request = BookCreationRequest(title = 'Harry Potter', author_id = uuid4())
    instance = BookValidator(author_dal_mock)
    with pytest.raises(ValidationError) as exc_info:
      instance.validate_creation(session_mock, request)
    assert exc_info.value.detail == "AUTHOR_NOT_FOUND"
