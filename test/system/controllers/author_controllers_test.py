import pytest


from uuid import uuid4
from system.test_utils.db_utils import delete_all_authors, delete_all_books, insert_author, insert_book
from system.test_utils.auth_utils import get_admin_auth_token, get_auth_headers, get_user_auth_token
from system.conftest import Context


class TestAuthorController():
  @pytest.fixture(autouse = True)
  def after_each(self, context: Context):
    self.user_auth_token = get_user_auth_token(context.auth_token_url, "test-user")
    self.admin_auth_token = get_admin_auth_token(context.auth_token_url, "test-admin")
    yield
    delete_all_books(context.db_url)
    delete_all_authors(context.db_url)

  def test_create_author(self, context: Context):
    author_name = 'J. K. Rowling'
    response = context.client.post("/v1/authors", json = { "name": author_name }, headers = get_auth_headers(self.admin_auth_token))
    assert response.status_code == 200
    data = response.json()
    assert data['id'] is not None
    assert data['name'] == author_name

  def test_create_author_with_duplicate_name(self, context: Context):
    author_name = 'J. K. Rowling'
    auth_header = get_auth_headers(self.admin_auth_token)
    first_response = context.client.post("/v1/authors", json = { "name": author_name }, headers = auth_header)
    second_response = context.client.post("/v1/authors", json = { "name": author_name }, headers = auth_header)
    assert first_response.status_code == 200
    assert second_response.status_code == 200
    first_data = first_response.json()
    second_data = second_response.json()
    assert first_data['id'] is not None
    assert second_data['id'] is not None
    assert first_data['id'] != second_data['id']
    assert first_data['name'] == author_name
    assert second_data['name'] == author_name

  def test_create_author_without_admin_scope(self, context: Context):
    auth_token = get_user_auth_token(context.auth_token_url, "test-user")
    response = context.client.post("/v1/authors", json = { "name": "J. K. Rowling" }, headers = get_auth_headers(auth_token))
    assert response.status_code == 403
    data = response.json()
    assert data == {
      'detail': 'INSUFFICIENT_PERMISSIONS'
    }

  def test_get_authors_no_search_term(self, context: Context):
    author_id_1 = uuid4()
    author_id_2 = uuid4()
    insert_author(context.db_url, author_id_1, 'J. K. Rowling')
    insert_author(context.db_url, author_id_2, 'J. R. R. Tolkien')
    response = context.client.get("/v1/authors", headers = get_auth_headers(self.user_auth_token))
    assert response.status_code == 200
    data = response.json()
    assert data['total_authors'] == 2
    assert data['total_pages'] == 1
    assert data['current_page'] == 1
    assert data['page_size'] == 10
    assert len(data['authors']) == 2
    returned_ids = { author['id'] for author in data['authors'] }
    assert str(author_id_1) in returned_ids
    assert str(author_id_2) in returned_ids

  def test_get_authors_with_search_term(self, context: Context):
    author_id = uuid4()
    insert_author(context.db_url, author_id, 'J. K. Rowling')
    insert_author(context.db_url, uuid4(), 'J. R. R. Tolkien')
    response = context.client.get("/v1/authors", params = { "search_term": "Rowling" }, headers = get_auth_headers(self.user_auth_token))
    assert response.status_code == 200
    data = response.json()
    assert data['total_authors'] == 1
    assert len(data['authors']) == 1
    assert data['authors'][0]['id'] == str(author_id)
    assert data['authors'][0]['name'] == 'J. K. Rowling'

  def test_get_authors_pagination(self, context: Context):
    author_id_1 = uuid4()
    author_id_2 = uuid4()
    insert_author(context.db_url, author_id_1, 'J. K. Rowling')
    insert_author(context.db_url, author_id_2, 'J. R. R. Tolkien')
    response = context.client.get("/v1/authors", params = { "page": 1, "page_size": 50 }, headers = get_auth_headers(self.user_auth_token))
    assert response.status_code == 200
    data = response.json()
    assert data['total_authors'] == 2
    assert data['current_page'] == 1
    assert data['page_size'] == 50
    assert len(data['authors']) == 2
    returned_ids = { author['id'] for author in data['authors'] }
    assert str(author_id_1) in returned_ids
    assert str(author_id_2) in returned_ids

  def test_get_authors_invalid_page_size(self, context: Context):
    response = context.client.get("/v1/authors", params = { "page_size": 7 }, headers = get_auth_headers(self.user_auth_token))
    assert response.status_code == 400
    data = response.json()
    assert data == { 'detail': 'INVALID_PAGE_SIZE' }

  def test_get_authors_no_results(self, context: Context):
    insert_author(context.db_url, uuid4(), 'J. K. Rowling')
    response = context.client.get("/v1/authors", params = { "search_term": "NonExistent" }, headers = get_auth_headers(self.user_auth_token))
    assert response.status_code == 200
    data = response.json()
    assert data['total_authors'] == 0
    assert len(data['authors']) == 0
    assert data['total_pages'] == 0

  def test_delete_authors_success(self, context: Context):
    author_id_1 = uuid4()
    author_id_2 = uuid4()
    insert_author(context.db_url, author_id_1, 'J. K. Rowling')
    insert_author(context.db_url, author_id_2, 'J. R. R. Tolkien')
    response = context.client.delete("/v1/authors", params = { "ids": [str(author_id_1), str(author_id_2)] }, headers = get_auth_headers(self.admin_auth_token))
    assert response.status_code == 204

  def test_delete_authors_without_admin_scope(self, context: Context):
    auth_token = get_user_auth_token(context.auth_token_url, "test-user")
    response = context.client.delete("/v1/authors", params = { "ids": [str(uuid4())] }, headers = get_auth_headers(auth_token))
    assert response.status_code == 403
    data = response.json()
    assert data == {
      'detail': 'INSUFFICIENT_PERMISSIONS'
    }

  def test_delete_authors_no_auth(self, context: Context):
    response = context.client.delete("/v1/authors", params = { "ids": [str(uuid4())] })
    assert response.status_code == 401
    data = response.json()
    assert data == {
      'detail': 'MISSING_TOKEN'
    }

  def test_delete_authors_nonexistent_ids(self, context: Context):
    author_id = uuid4()
    insert_author(context.db_url, author_id, 'J. K. Rowling')
    nonexistent_id = uuid4()
    response = context.client.delete("/v1/authors", params = { "ids": [str(author_id), str(nonexistent_id)] }, headers = get_auth_headers(self.admin_auth_token))
    assert response.status_code == 400
    data = response.json()
    assert data['detail'] == f"AUTHORS_NOT_FOUND: ['{str(nonexistent_id)}']"

  def test_delete_authors_with_existing_books(self, context: Context):
    author_id = uuid4()
    insert_author(context.db_url, author_id, 'J. K. Rowling')
    book_id = uuid4()
    insert_book(context.db_url, book_id, "Harry Potter", author_id)
    response = context.client.delete("/v1/authors", params = { "ids": [str(author_id)] }, headers = get_auth_headers(self.admin_auth_token))
    assert response.status_code == 400
    data = response.json()
    assert data['detail'] == f"AUTHORS_HAVE_BOOKS: ['{str(author_id)}']"

  def test_delete_authors_too_many_ids(self, context: Context):
    too_many_ids = [str(uuid4()) for _ in range(101)]
    response = context.client.delete("/v1/authors", params = { "ids": too_many_ids }, headers = get_auth_headers(self.admin_auth_token))
    assert response.status_code == 400
    data = response.json()
    assert data == { 'detail': 'INVALID_AUTHOR_IDS_COUNT' }

  def test_delete_authors_invalid_uuid(self, context: Context):
    response = context.client.delete("/v1/authors", params = { "ids": ["not-a-uuid"] }, headers = get_auth_headers(self.admin_auth_token))
    assert response.status_code == 400
    data = response.json()
    assert data['detail'] == 'INVALID_UUID: badly formed hexadecimal UUID string'
