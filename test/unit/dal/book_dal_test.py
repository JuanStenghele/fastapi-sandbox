import pytest

from datetime import datetime, timezone
from unittest.mock import MagicMock
from uuid import uuid4
from sqlmodel import Session
from objects.book import Book
from dal.book_dal import BookDAL
from db_schema.book_author_db import BookAuthor as DBBookAuthor
from db_schema.book_cover_db import BookCover as DBBookCover
from db_schema.book_db import Book as DBBook


class TestBookDal():
  def test_create_book_success(self):
    session_mock = MagicMock(spec = Session)
    now = datetime.now(timezone.utc)
    book_id = uuid4()
    author_id = uuid4()
    book_title = 'Harry Potter'
    book = Book(id = book_id, title = book_title, author_id = author_id, created_at = now, updated_at = now)
    instance = BookDAL()
    result = instance.create_book(session_mock, book)
    assert result == book
    assert session_mock.add.call_count == 2
    added_book = session_mock.add.call_args_list[0][0][0]
    assert added_book.id == book_id
    assert added_book.title == book_title
    added_book_author = session_mock.add.call_args_list[1][0][0]
    assert added_book_author.book_id == book_id
    assert added_book_author.author_id == author_id

  def test_create_book_fail(self):
    session_mock = MagicMock(spec = Session)
    expected_message = 'Test Exception'
    session_mock.add.side_effect = Exception(expected_message)
    now = datetime.now(timezone.utc)
    book = Book(id = uuid4(), title = 'Harry Potter', author_id = uuid4(), created_at = now, updated_at = now)
    instance = BookDAL()
    with pytest.raises(Exception) as exc_info:
      instance.create_book(session_mock, book)
    assert str(exc_info.value) == expected_message
    assert session_mock.add.call_count == 1

  def test_get_book_success(self):
    session_mock = MagicMock(spec = Session)
    now = datetime.now(timezone.utc)
    book_id = uuid4()
    author_id = uuid4()
    book_title = 'Harry Potter'
    db_book = DBBook(id = book_id, title = book_title, created_at = now, updated_at = now)
    db_book_author = DBBookAuthor(book_id = book_id, author_id = author_id, created_at = now)
    exec_mock = MagicMock()
    exec_mock.first.return_value = (db_book, db_book_author, None)
    session_mock.exec.return_value = exec_mock
    instance = BookDAL()
    result = instance.get_book(session_mock, book_id)
    assert result is not None
    assert result.id == book_id
    assert result.title == book_title
    assert result.author_id == author_id
    assert result.cover_image is None
    assert session_mock.exec.call_count == 1

  def test_get_book_success_with_cover(self):
    session_mock = MagicMock(spec = Session)
    now = datetime.now(timezone.utc)
    book_id = uuid4()
    author_id = uuid4()
    cover_url = 'https://example.com/cover.jpg'
    db_book = DBBook(id = book_id, title = 'Harry Potter', created_at = now, updated_at = now)
    db_book_author = DBBookAuthor(book_id = book_id, author_id = author_id, created_at = now)
    db_cover = DBBookCover(book_id = book_id, source = 's3', url = cover_url, created_at = now, updated_at = now)
    exec_mock = MagicMock()
    exec_mock.first.return_value = (db_book, db_book_author, db_cover)
    session_mock.exec.return_value = exec_mock
    instance = BookDAL()
    result = instance.get_book(session_mock, book_id)
    assert result is not None
    assert result.cover_image is not None
    assert result.cover_image.book_id == book_id
    assert result.cover_image.url == cover_url

  def test_get_book_not_found(self):
    session_mock = MagicMock(spec = Session)
    exec_mock = MagicMock()
    exec_mock.first.return_value = None
    session_mock.exec.return_value = exec_mock
    instance = BookDAL()
    result = instance.get_book(session_mock, uuid4())
    assert result is None

  def test_get_book_fail(self):
    session_mock = MagicMock(spec = Session)
    expected_message = 'Test Exception'
    session_mock.exec.side_effect = Exception(expected_message)
    instance = BookDAL()
    with pytest.raises(Exception) as exc_info:
      instance.get_book(session_mock, uuid4())
    assert str(exc_info.value) == expected_message
    assert session_mock.exec.call_count == 1

  def test_get_books_success(self):
    session_mock = MagicMock(spec = Session)
    now = datetime.now(timezone.utc)
    book_id = uuid4()
    author_id = uuid4()
    book_title = 'Harry Potter'
    db_book = DBBook(id = book_id, title = book_title, created_at = now, updated_at = now)
    db_book_author = DBBookAuthor(book_id = book_id, author_id = author_id, created_at = now)
    exec_mock = MagicMock()
    exec_mock.all.return_value = [(db_book, db_book_author, None)]
    session_mock.exec.return_value = exec_mock
    instance = BookDAL()
    result = instance.get_books(session_mock, None, 10, 0)
    assert len(result) == 1
    assert result[0].id == book_id
    assert result[0].title == book_title
    assert result[0].author_id == author_id
    assert result[0].cover_image is None
    assert session_mock.exec.call_count == 1

  def test_get_books_success_with_search_term(self):
    session_mock = MagicMock(spec = Session)
    now = datetime.now(timezone.utc)
    book_id = uuid4()
    author_id = uuid4()
    book_title = 'Harry Potter'
    db_book = DBBook(id = book_id, title = book_title, created_at = now, updated_at = now)
    db_book_author = DBBookAuthor(book_id = book_id, author_id = author_id, created_at = now)
    exec_mock = MagicMock()
    exec_mock.all.return_value = [(db_book, db_book_author, None)]
    session_mock.exec.return_value = exec_mock
    instance = BookDAL()
    result = instance.get_books(session_mock, 'Harry', 10, 0)
    assert len(result) == 1
    assert result[0].id == book_id
    assert result[0].title == book_title
    assert session_mock.exec.call_count == 1

  def test_get_books_success_with_search_term_and_cover(self):
    session_mock = MagicMock(spec = Session)
    now = datetime.now(timezone.utc)
    book_id = uuid4()
    author_id = uuid4()
    cover_url = 'https://example.com/cover.jpg'
    db_book = DBBook(id = book_id, title = 'Harry Potter', created_at = now, updated_at = now)
    db_book_author = DBBookAuthor(book_id = book_id, author_id = author_id, created_at = now)
    db_cover = DBBookCover(book_id = book_id, source = 's3', url = cover_url, created_at = now, updated_at = now)
    exec_mock = MagicMock()
    exec_mock.all.return_value = [(db_book, db_book_author, db_cover)]
    session_mock.exec.return_value = exec_mock
    instance = BookDAL()
    result = instance.get_books(session_mock, 'Harry', 10, 0)
    assert result[0].cover_image is not None
    assert result[0].cover_image.book_id == book_id
    assert result[0].cover_image.url == cover_url

  def test_get_books_success_multiple_results(self):
    session_mock = MagicMock(spec = Session)
    now = datetime.now(timezone.utc)
    book_id_1 = uuid4()
    book_id_2 = uuid4()
    author_id = uuid4()
    db_book_1 = DBBook(id = book_id_1, title = 'Harry Potter', created_at = now, updated_at = now)
    db_book_2 = DBBook(id = book_id_2, title = 'The Lord of the Rings', created_at = now, updated_at = now)
    db_book_author_1 = DBBookAuthor(book_id = book_id_1, author_id = author_id, created_at = now)
    db_book_author_2 = DBBookAuthor(book_id = book_id_2, author_id = author_id, created_at = now)
    exec_mock = MagicMock()
    exec_mock.all.return_value = [(db_book_1, db_book_author_1, None), (db_book_2, db_book_author_2, None)]
    session_mock.exec.return_value = exec_mock
    instance = BookDAL()
    result = instance.get_books(session_mock, None, 10, 0)
    assert len(result) == 2
    assert result[0].id == book_id_1
    assert result[0].title == 'Harry Potter'
    assert result[1].id == book_id_2
    assert result[1].title == 'The Lord of the Rings'
    assert session_mock.exec.call_count == 1

  def test_get_books_empty_results(self):
    session_mock = MagicMock(spec = Session)
    exec_mock = MagicMock()
    exec_mock.all.return_value = []
    session_mock.exec.return_value = exec_mock
    instance = BookDAL()
    result = instance.get_books(session_mock, None, 10, 0)
    assert result == []
    assert session_mock.exec.call_count == 1

  def test_get_books_fail(self):
    session_mock = MagicMock(spec = Session)
    expected_message = 'Test Exception'
    session_mock.exec.side_effect = Exception(expected_message)
    instance = BookDAL()
    with pytest.raises(Exception) as exc_info:
      instance.get_books(session_mock, None, 10, 0)
    assert str(exc_info.value) == expected_message
    assert session_mock.exec.call_count == 1

  def test_count_books_success_no_search_term(self):
    session_mock = MagicMock(spec = Session)
    exec_mock = MagicMock()
    exec_mock.one.return_value = 5
    session_mock.exec.return_value = exec_mock
    instance = BookDAL()
    result = instance.count_books(session_mock, None)
    assert result == 5
    assert session_mock.exec.call_count == 1

  def test_count_books_success_with_search_term(self):
    session_mock = MagicMock(spec = Session)
    exec_mock = MagicMock()
    exec_mock.one.return_value = 3
    session_mock.exec.return_value = exec_mock
    instance = BookDAL()
    result = instance.count_books(session_mock, 'Harry')
    assert result == 3
    assert session_mock.exec.call_count == 1

  def test_count_books_fail(self):
    session_mock = MagicMock(spec = Session)
    expected_message = 'Test Exception'
    session_mock.exec.side_effect = Exception(expected_message)
    instance = BookDAL()
    with pytest.raises(Exception) as exc_info:
      instance.count_books(session_mock, None)
    assert str(exc_info.value) == expected_message
    assert session_mock.exec.call_count == 1
