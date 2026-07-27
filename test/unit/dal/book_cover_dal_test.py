import pytest


from datetime import datetime, timezone
from unittest.mock import MagicMock
from uuid import uuid4
from sqlmodel import Session
from objects.book_cover import BookCover
from dal.book_cover_dal import BookCoverDAL
from db_schema.book_cover_db import BookCover as DBBookCover


class TestBookCoverDal():
  def test_create_book_cover_success(self):
    session_mock = MagicMock(spec = Session)
    book_id = uuid4()
    now = datetime.now(timezone.utc)
    book_cover = BookCover(
      book_id = book_id,
      source = "s3",
      url = "https://example.com/cover.jpg",
      path = "public/user-content/cover-images/cover.jpg",
      created_at = now,
      updated_at = now
    )
    instance = BookCoverDAL()
    result = instance.create_book_cover(session_mock, book_cover)
    assert result == book_cover
    added_book_cover = session_mock.add.call_args[0][0]
    assert added_book_cover.book_id == book_id
    assert added_book_cover.source == "s3"
    assert added_book_cover.url == "https://example.com/cover.jpg"
    assert added_book_cover.path == "public/user-content/cover-images/cover.jpg"
    assert added_book_cover.created_at == now
    assert added_book_cover.updated_at == now

  def test_create_book_cover_fail(self):
    session_mock = MagicMock(spec = Session)
    expected_message = 'Test Exception'
    session_mock.add.side_effect = Exception(expected_message)
    now = datetime.now(timezone.utc)
    book_cover = BookCover(
      book_id = uuid4(),
      source = "s3",
      url = "https://example.com/cover.jpg",
      path = "public/user-content/cover-images/cover.jpg",
      created_at = now,
      updated_at = now
    )
    instance = BookCoverDAL()
    with pytest.raises(Exception) as exc_info:
      instance.create_book_cover(session_mock, book_cover)
    assert str(exc_info.value) == expected_message
    assert session_mock.add.call_count == 1

  def test_get_book_cover_success(self):
    session_mock = MagicMock(spec = Session)
    now = datetime.now(timezone.utc)
    book_id = uuid4()
    db_cover = DBBookCover(book_id = book_id, source = "s3", url = "https://example.com/cover.jpg", path = "public/user-content/cover-images/cover.jpg", created_at = now, updated_at = now)
    exec_mock = MagicMock()
    exec_mock.first.return_value = db_cover
    session_mock.exec.return_value = exec_mock
    instance = BookCoverDAL()
    result = instance.get_book_cover(session_mock, book_id)
    assert result is not None
    assert result.book_id == book_id
    assert result.url == "https://example.com/cover.jpg"
    assert session_mock.exec.call_count == 1

  def test_get_book_cover_not_found(self):
    session_mock = MagicMock(spec = Session)
    exec_mock = MagicMock()
    exec_mock.first.return_value = None
    session_mock.exec.return_value = exec_mock
    instance = BookCoverDAL()
    result = instance.get_book_cover(session_mock, uuid4())
    assert result is None

  def test_get_book_cover_fail(self):
    session_mock = MagicMock(spec = Session)
    expected_message = 'Test Exception'
    session_mock.exec.side_effect = Exception(expected_message)
    instance = BookCoverDAL()
    with pytest.raises(Exception) as exc_info:
      instance.get_book_cover(session_mock, uuid4())
    assert str(exc_info.value) == expected_message

  def test_get_book_covers_by_ids_success(self):
    session_mock = MagicMock(spec = Session)
    now = datetime.now(timezone.utc)
    book_id_1 = uuid4()
    book_id_2 = uuid4()
    db_cover_1 = DBBookCover(book_id = book_id_1, source = "s3", url = "https://example.com/cover1.jpg", path = "public/user-content/cover-images/cover1.jpg", created_at = now, updated_at = now)
    db_cover_2 = DBBookCover(book_id = book_id_2, source = "s3", url = "https://example.com/cover2.jpg", path = "public/user-content/cover-images/cover2.jpg", created_at = now, updated_at = now)
    exec_mock = MagicMock()
    exec_mock.all.return_value = [db_cover_1, db_cover_2]
    session_mock.exec.return_value = exec_mock
    instance = BookCoverDAL()
    result = instance.get_book_covers_by_ids(session_mock, [book_id_1, book_id_2])
    assert len(result) == 2
    assert result[0].book_id == book_id_1
    assert result[1].book_id == book_id_2

  def test_get_book_covers_by_ids_empty_results(self):
    session_mock = MagicMock(spec = Session)
    exec_mock = MagicMock()
    exec_mock.all.return_value = []
    session_mock.exec.return_value = exec_mock
    instance = BookCoverDAL()
    result = instance.get_book_covers_by_ids(session_mock, [uuid4()])
    assert result == []

  def test_get_book_covers_by_ids_fail(self):
    session_mock = MagicMock(spec = Session)
    expected_message = 'Test Exception'
    session_mock.exec.side_effect = Exception(expected_message)
    instance = BookCoverDAL()
    with pytest.raises(Exception) as exc_info:
      instance.get_book_covers_by_ids(session_mock, [uuid4()])
    assert str(exc_info.value) == expected_message

  def test_soft_delete_book_covers_success(self):
    session_mock = MagicMock(spec = Session)
    now = datetime.now(timezone.utc)
    book_id = uuid4()
    instance = BookCoverDAL()
    instance.soft_delete_book_covers(session_mock, [book_id], now)
    assert session_mock.exec.call_count == 1

  def test_soft_delete_book_covers_fail(self):
    session_mock = MagicMock(spec = Session)
    expected_message = 'Test Exception'
    session_mock.exec.side_effect = Exception(expected_message)
    now = datetime.now(timezone.utc)
    instance = BookCoverDAL()
    with pytest.raises(Exception) as exc_info:
      instance.soft_delete_book_covers(session_mock, [uuid4()], now)
    assert str(exc_info.value) == expected_message
