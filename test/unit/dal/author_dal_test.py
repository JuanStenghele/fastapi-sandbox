import pytest


from datetime import datetime, timezone
from unittest.mock import MagicMock
from uuid import uuid4
from sqlmodel import Session
from objects.author import Author
from dal.author_dal import AuthorDAL
from db_schema.author_db import Author as DBAuthor
from db_schema.book_author_db import BookAuthor as DBBookAuthor


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

  def test_get_author_success(self):
    session_mock = MagicMock(spec = Session)
    now = datetime.now(timezone.utc)
    author_id = uuid4()
    author_name = 'J. K. Rowling'
    db_author = DBAuthor(id = author_id, name = author_name, created_at = now, updated_at = now)
    exec_mock = MagicMock()
    exec_mock.first.return_value = db_author
    session_mock.exec.return_value = exec_mock
    instance = AuthorDAL()
    result = instance.get_author(session_mock, author_id)
    assert result is not None
    assert result.id == author_id
    assert result.name == author_name
    assert session_mock.exec.call_count == 1

  def test_get_author_not_found(self):
    session_mock = MagicMock(spec = Session)
    exec_mock = MagicMock()
    exec_mock.first.return_value = None
    session_mock.exec.return_value = exec_mock
    instance = AuthorDAL()
    result = instance.get_author(session_mock, uuid4())
    assert result is None

  def test_get_author_fail(self):
    session_mock = MagicMock(spec = Session)
    expected_message = 'Test Exception'
    session_mock.exec.side_effect = Exception(expected_message)
    instance = AuthorDAL()
    with pytest.raises(Exception) as exc_info:
      instance.get_author(session_mock, uuid4())
    assert str(exc_info.value) == expected_message
    assert session_mock.exec.call_count == 1

  def test_get_authors_success(self):
    session_mock = MagicMock(spec = Session)
    now = datetime.now(timezone.utc)
    author_id = uuid4()
    author_name = 'J. K. Rowling'
    db_author = DBAuthor(id = author_id, name = author_name, created_at = now, updated_at = now)
    exec_mock = MagicMock()
    exec_mock.all.return_value = [db_author]
    session_mock.exec.return_value = exec_mock
    instance = AuthorDAL()
    result = instance.get_authors(session_mock, None, 10, 0)
    assert len(result) == 1
    assert result[0].id == author_id
    assert result[0].name == author_name
    assert session_mock.exec.call_count == 1

  def test_get_authors_success_with_search_term(self):
    session_mock = MagicMock(spec = Session)
    now = datetime.now(timezone.utc)
    author_id = uuid4()
    author_name = 'J. K. Rowling'
    db_author = DBAuthor(id = author_id, name = author_name, created_at = now, updated_at = now)
    exec_mock = MagicMock()
    exec_mock.all.return_value = [db_author]
    session_mock.exec.return_value = exec_mock
    instance = AuthorDAL()
    result = instance.get_authors(session_mock, 'Rowling', 10, 0)
    assert len(result) == 1
    assert result[0].id == author_id
    assert result[0].name == author_name
    assert session_mock.exec.call_count == 1

  def test_get_authors_success_multiple_results(self):
    session_mock = MagicMock(spec = Session)
    now = datetime.now(timezone.utc)
    author_id_1 = uuid4()
    author_id_2 = uuid4()
    db_author_1 = DBAuthor(id = author_id_1, name = 'J. K. Rowling', created_at = now, updated_at = now)
    db_author_2 = DBAuthor(id = author_id_2, name = 'J. R. R. Tolkien', created_at = now, updated_at = now)
    exec_mock = MagicMock()
    exec_mock.all.return_value = [db_author_1, db_author_2]
    session_mock.exec.return_value = exec_mock
    instance = AuthorDAL()
    result = instance.get_authors(session_mock, None, 10, 0)
    assert len(result) == 2
    assert result[0].id == author_id_1
    assert result[0].name == 'J. K. Rowling'
    assert result[1].id == author_id_2
    assert result[1].name == 'J. R. R. Tolkien'
    assert session_mock.exec.call_count == 1

  def test_get_authors_empty_results(self):
    session_mock = MagicMock(spec = Session)
    exec_mock = MagicMock()
    exec_mock.all.return_value = []
    session_mock.exec.return_value = exec_mock
    instance = AuthorDAL()
    result = instance.get_authors(session_mock, None, 10, 0)
    assert result == []
    assert session_mock.exec.call_count == 1

  def test_get_authors_fail(self):
    session_mock = MagicMock(spec = Session)
    expected_message = 'Test Exception'
    session_mock.exec.side_effect = Exception(expected_message)
    instance = AuthorDAL()
    with pytest.raises(Exception) as exc_info:
      instance.get_authors(session_mock, None, 10, 0)
    assert str(exc_info.value) == expected_message
    assert session_mock.exec.call_count == 1

  def test_count_authors_success_no_search_term(self):
    session_mock = MagicMock(spec = Session)
    exec_mock = MagicMock()
    exec_mock.one.return_value = 5
    session_mock.exec.return_value = exec_mock
    instance = AuthorDAL()
    result = instance.count_authors(session_mock, None)
    assert result == 5
    assert session_mock.exec.call_count == 1

  def test_count_authors_success_with_search_term(self):
    session_mock = MagicMock(spec = Session)
    exec_mock = MagicMock()
    exec_mock.one.return_value = 3
    session_mock.exec.return_value = exec_mock
    instance = AuthorDAL()
    result = instance.count_authors(session_mock, 'Rowling')
    assert result == 3
    assert session_mock.exec.call_count == 1

  def test_count_authors_fail(self):
    session_mock = MagicMock(spec = Session)
    expected_message = 'Test Exception'
    session_mock.exec.side_effect = Exception(expected_message)
    instance = AuthorDAL()
    with pytest.raises(Exception) as exc_info:
      instance.count_authors(session_mock, None)
    assert str(exc_info.value) == expected_message
    assert session_mock.exec.call_count == 1

  def test_get_authors_by_ids_success(self):
    session_mock = MagicMock(spec = Session)
    now = datetime.now(timezone.utc)
    author_id_1 = uuid4()
    author_id_2 = uuid4()
    db_author_1 = DBAuthor(id = author_id_1, name = 'J. K. Rowling', created_at = now, updated_at = now)
    db_author_2 = DBAuthor(id = author_id_2, name = 'J. R. R. Tolkien', created_at = now, updated_at = now)
    exec_mock = MagicMock()
    exec_mock.all.return_value = [db_author_1, db_author_2]
    session_mock.exec.return_value = exec_mock
    instance = AuthorDAL()
    result = instance.get_authors_by_ids(session_mock, [author_id_1, author_id_2])
    assert len(result) == 2
    assert result[0].id == author_id_1
    assert result[0].name == 'J. K. Rowling'
    assert result[1].id == author_id_2
    assert result[1].name == 'J. R. R. Tolkien'
    assert session_mock.exec.call_count == 1

  def test_get_authors_by_ids_empty_results(self):
    session_mock = MagicMock(spec = Session)
    exec_mock = MagicMock()
    exec_mock.all.return_value = []
    session_mock.exec.return_value = exec_mock
    instance = AuthorDAL()
    result = instance.get_authors_by_ids(session_mock, [uuid4()])
    assert result == []
    assert session_mock.exec.call_count == 1

  def test_get_authors_by_ids_fail(self):
    session_mock = MagicMock(spec = Session)
    expected_message = 'Test Exception'
    session_mock.exec.side_effect = Exception(expected_message)
    instance = AuthorDAL()
    with pytest.raises(Exception) as exc_info:
      instance.get_authors_by_ids(session_mock, [uuid4()])
    assert str(exc_info.value) == expected_message
    assert session_mock.exec.call_count == 1

  def test_get_author_ids_with_books_success(self):
    session_mock = MagicMock(spec = Session)
    author_id_1 = uuid4()
    author_id_2 = uuid4()
    exec_mock = MagicMock()
    exec_mock.all.return_value = [author_id_1, author_id_2]
    session_mock.exec.return_value = exec_mock
    instance = AuthorDAL()
    result = instance.get_author_ids_with_books(session_mock, [author_id_1, author_id_2])
    assert result == [author_id_1, author_id_2]
    assert session_mock.exec.call_count == 1

  def test_get_author_ids_with_books_empty_results(self):
    session_mock = MagicMock(spec = Session)
    exec_mock = MagicMock()
    exec_mock.all.return_value = []
    session_mock.exec.return_value = exec_mock
    instance = AuthorDAL()
    result = instance.get_author_ids_with_books(session_mock, [uuid4()])
    assert result == []
    assert session_mock.exec.call_count == 1

  def test_get_author_ids_with_books_fail(self):
    session_mock = MagicMock(spec = Session)
    expected_message = 'Test Exception'
    session_mock.exec.side_effect = Exception(expected_message)
    instance = AuthorDAL()
    with pytest.raises(Exception) as exc_info:
      instance.get_author_ids_with_books(session_mock, [uuid4()])
    assert str(exc_info.value) == expected_message
    assert session_mock.exec.call_count == 1

  def test_soft_delete_authors_success(self):
    session_mock = MagicMock(spec = Session)
    now = datetime.now(timezone.utc)
    author_id = uuid4()
    instance = AuthorDAL()
    instance.soft_delete_authors(session_mock, [author_id], now)
    assert session_mock.exec.call_count == 1

  def test_soft_delete_authors_fail(self):
    session_mock = MagicMock(spec = Session)
    expected_message = 'Test Exception'
    session_mock.exec.side_effect = Exception(expected_message)
    now = datetime.now(timezone.utc)
    instance = AuthorDAL()
    with pytest.raises(Exception) as exc_info:
      instance.soft_delete_authors(session_mock, [uuid4()], now)
    assert str(exc_info.value) == expected_message
    assert session_mock.exec.call_count == 1

  def test_update_author_success(self):
    session_mock = MagicMock(spec = Session)
    now = datetime.now(timezone.utc)
    updated_at = datetime.now(timezone.utc)
    author_id = uuid4()
    db_author = DBAuthor(id = author_id, name = 'J. K. Rowling', created_at = now, updated_at = now)
    exec_mock = MagicMock()
    exec_mock.first.return_value = db_author
    session_mock.exec.return_value = exec_mock
    instance = AuthorDAL()
    result = instance.update_author(session_mock, author_id, 'Robert Galbraith', updated_at)
    assert result is not None
    assert result.id == author_id
    assert result.name == 'Robert Galbraith'
    assert result.updated_at == updated_at
    assert session_mock.exec.call_count == 1
    session_mock.add.assert_called_once_with(db_author)

  def test_update_author_not_found(self):
    session_mock = MagicMock(spec = Session)
    exec_mock = MagicMock()
    exec_mock.first.return_value = None
    session_mock.exec.return_value = exec_mock
    instance = AuthorDAL()
    result = instance.update_author(session_mock, uuid4(), 'Robert Galbraith', datetime.now(timezone.utc))
    assert result is None
    assert session_mock.exec.call_count == 1

  def test_update_author_fail(self):
    session_mock = MagicMock(spec = Session)
    expected_message = 'Test Exception'
    session_mock.exec.side_effect = Exception(expected_message)
    instance = AuthorDAL()
    with pytest.raises(Exception) as exc_info:
      instance.update_author(session_mock, uuid4(), 'Robert Galbraith', datetime.now(timezone.utc))
    assert str(exc_info.value) == expected_message
    assert session_mock.exec.call_count == 1
