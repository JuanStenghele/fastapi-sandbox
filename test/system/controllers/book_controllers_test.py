import pytest

from uuid import uuid4
from system.utils.db_utils import insert_author, insert_book, delete_all_books
from system.utils.auth_utils import get_auth_headers, get_user_auth_token
from system.conftest import Context


class TestBookController():
  @pytest.fixture(autouse = True)
  def after_each(self, context: Context):
    self.auth_token = get_user_auth_token(context.auth_token_url, "test-user")
    yield
    delete_all_books(context.db_url)

  def test_retrieve_book(self, context: Context):
    author_id = uuid4()
    insert_author(context.db_url, author_id, 'J. K. Rowling')
    book_id = uuid4()
    insert_book(context.db_url, book_id, 'Harry Potter', author_id)
    tolkien_id = uuid4()
    insert_author(context.db_url, tolkien_id, 'J. R. R. Tolkien')
    insert_book(context.db_url, uuid4(), 'The Lord of the Rings', tolkien_id)
    response = context.client.get("/v1/books", params = { "id": str(book_id) }, headers = get_auth_headers(self.auth_token))
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == str(book_id)
    assert data['title'] == 'Harry Potter'

  def test_retrieve_unexistent_book(self, context: Context):
    author_id = uuid4()
    insert_author(context.db_url, author_id, 'J. K. Rowling')
    insert_book(context.db_url, uuid4(), 'Harry Potter', author_id)
    response = context.client.get("/v1/books", params = { "id": str(uuid4()) }, headers = get_auth_headers(self.auth_token))
    assert response.status_code == 404
    data = response.json()
    assert data == {
      'detail': 'BOOK_NOT_FOUND'
    }

  def test_create_book(self, context: Context):
    author_id = uuid4()
    insert_author(context.db_url, author_id, 'J. K. Rowling')
    book_title = 'Harry Potter'
    response = context.client.post("/v1/books", data = { "title": book_title, "author_id": str(author_id) }, headers = get_auth_headers(self.auth_token))
    assert response.status_code == 200
    data = response.json()
    assert data['id'] is not None
    assert data['title'] == book_title

  def test_create_book_invalid_author(self, context: Context):
    response = context.client.post("/v1/books", data = { "title": "Harry Potter", "author_id": str(uuid4()) }, headers = get_auth_headers(self.auth_token))
    assert response.status_code == 400
    data = response.json()
    assert data == { 'detail': 'AUTHOR_NOT_FOUND' }

  def test_create_book_with_duplicate_title(self, context: Context):
    author_id = uuid4()
    insert_author(context.db_url, author_id, 'J. K. Rowling')
    book_title = 'Harry Potter'
    insert_book(context.db_url, uuid4(), book_title, author_id)
    response = context.client.post("/v1/books", data = { "title": book_title, "author_id": str(author_id) }, headers = get_auth_headers(self.auth_token))
    assert response.status_code == 200
    data = response.json()
    assert data['id'] is not None
    assert data['title'] == book_title
