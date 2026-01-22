import pytest


from system.utils.db_utils import insert_book, delete_all_books
from system.conftest import Context


class TestBookController():
  @pytest.fixture(autouse = True)
  def after_each(self, context: Context):
    yield
    delete_all_books(context.db_url)

  def test_retrieve_book(self, context: Context):
    insert_book(context.db_url, '123', 'Harry Potter')
    insert_book(context.db_url, '456', 'The Lord of the Rings')
    response = context.client.get("/v1/books", params = { "id": "123" })
    assert response.status_code == 200
    data = response.json()
    assert data == {
      'id': '123',
      'name': 'Harry Potter'
    }

  def test_retrieve_unexistent_book(self, context: Context):
    insert_book(context.db_url, '123', 'Harry Potter')
    insert_book(context.db_url, '456', 'The Lord of the Rings')
    response = context.client.get("/v1/books", params = { "id": "789" })
    assert response.status_code == 404
    data = response.json()
    assert data == {
      'detail': 'BOOK_NOT_FOUND'
    }

  def test_create_book(self, context: Context):
    book_name = 'Harry Potter'
    response = context.client.post("/v1/books", json = { "name": book_name })
    assert response.status_code == 200
    data = response.json()
    assert data['id'] is not None
    assert data['name'] == book_name

  def test_create_book_with_duplicate_name(self, context: Context):
    book_name = 'Harry Potter'
    insert_book(context.db_url, '123', book_name)
    response = context.client.post("/v1/books", json = { "name": book_name })
    assert response.status_code == 200
    data = response.json()
    assert data['id'] is not None
    assert data['name'] == book_name
