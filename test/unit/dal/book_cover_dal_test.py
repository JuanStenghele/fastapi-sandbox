import pytest


from datetime import datetime, timezone
from unittest.mock import MagicMock
from uuid import uuid4
from sqlmodel import Session
from objects.book_cover import BookCover
from dal.book_cover_dal import BookCoverDAL


class TestBookCoverDal():
  def test_create_book_cover_success(self):
    session_mock = MagicMock(spec = Session)
    book_cover_id = uuid4()
    now = datetime.now(timezone.utc)
    book_cover = BookCover(
      id = book_cover_id,
      source = "s3",
      url = "https://example.com/cover.jpg",
      created_at = now,
      updated_at = now
    )
    instance = BookCoverDAL()
    result = instance.create_book_cover(session_mock, book_cover)
    assert result == book_cover
    added_book_cover = session_mock.add.call_args[0][0]
    assert added_book_cover.id == book_cover_id
    assert added_book_cover.source == "s3"
    assert added_book_cover.url == "https://example.com/cover.jpg"
    assert added_book_cover.created_at == now
    assert added_book_cover.updated_at == now

  def test_create_book_cover_fail(self):
    session_mock = MagicMock(spec = Session)
    expected_message = 'Test Exception'
    session_mock.add.side_effect = Exception(expected_message)
    now = datetime.now(timezone.utc)
    book_cover = BookCover(
      id = uuid4(),
      source = "s3",
      url = "https://example.com/cover.jpg",
      created_at = now,
      updated_at = now
    )
    instance = BookCoverDAL()
    with pytest.raises(Exception) as exc_info:
      instance.create_book_cover(session_mock, book_cover)
    assert str(exc_info.value) == expected_message
    assert session_mock.add.call_count == 1
