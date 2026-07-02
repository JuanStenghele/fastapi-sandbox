import pytest

from uuid import uuid4
from system.utils.db_utils import insert_author, insert_book, clean_all_tables
from system.utils.auth_utils import get_auth_headers, get_user_auth_token, get_admin_auth_token
from system.utils.storage_utils import get_test_image_path, clean_bucket, file_exists
from system.conftest import Context


class TestBookController():
  @pytest.fixture(autouse = True)
  def after_each(self, context: Context):
    self.auth_token = get_user_auth_token(context.auth_token_url, "test-user")
    self.admin_auth_token = get_admin_auth_token(context.auth_token_url, "test-user")
    yield
    clean_all_tables(context.db_url)
    clean_bucket(context.storage_service_url, context.storage_access_key_id, context.storage_secret_access_key, context.storage_bucket_name)

  def test_retrieve_book(self, context: Context):
    author_id = uuid4()
    insert_author(context.db_url, author_id, 'J. K. Rowling')
    book_id = uuid4()
    insert_book(context.db_url, book_id, 'Harry Potter', author_id)
    tolkien_id = uuid4()
    insert_author(context.db_url, tolkien_id, 'J. R. R. Tolkien')
    insert_book(context.db_url, uuid4(), 'The Lord of the Rings', tolkien_id)
    response = context.client.get(f"/v1/books/{book_id}", headers = get_auth_headers(self.auth_token))
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == str(book_id)
    assert data['title'] == 'Harry Potter'

  def test_retrieve_unexistent_book(self, context: Context):
    author_id = uuid4()
    insert_author(context.db_url, author_id, 'J. K. Rowling')
    insert_book(context.db_url, uuid4(), 'Harry Potter', author_id)
    response = context.client.get(f"/v1/books/{uuid4()}", headers = get_auth_headers(self.auth_token))
    assert response.status_code == 404
    data = response.json()
    assert data == {
      'detail': 'BOOK_NOT_FOUND'
    }

  def test_create_book(self, context: Context):
    author_id = uuid4()
    insert_author(context.db_url, author_id, 'J. K. Rowling')
    book_title = 'Harry Potter'
    book_description = 'A young wizard discovers his magical heritage.'
    book_isbn = '978-0-7475-3269-9'
    book_publication_date = '1997-06-26'
    response = context.client.post("/v1/books", data = { "title": book_title, "author_id": str(author_id), "description": book_description, "isbn": book_isbn, "publication_date": book_publication_date }, headers = get_auth_headers(self.admin_auth_token))
    assert response.status_code == 200
    data = response.json()
    assert data['id'] is not None
    assert data['title'] == book_title
    assert data['description'] == book_description
    assert data['isbn'] == book_isbn
    assert data['publication_date'] == book_publication_date

  def test_create_book_invalid_author(self, context: Context):
    response = context.client.post("/v1/books", data = { "title": "Harry Potter", "author_id": str(uuid4()) }, headers = get_auth_headers(self.admin_auth_token))
    assert response.status_code == 400
    data = response.json()
    assert data == { 'detail': 'AUTHOR_NOT_FOUND' }

  def test_create_book_without_admin_scope(self, context: Context):
    auth_token = get_user_auth_token(context.auth_token_url, "test-user")
    response = context.client.post("/v1/books", data = { "title": "Harry Potter", "author_id": str(uuid4()) }, headers = get_auth_headers(auth_token))
    assert response.status_code == 403
    data = response.json()
    assert data == { 'detail': 'INSUFFICIENT_PERMISSIONS' }

  def test_create_book_with_cover(self, context: Context):
    author_id = uuid4()
    insert_author(context.db_url, author_id, 'J. K. Rowling')
    book_title = 'Harry Potter'
    book_description = 'A young wizard discovers his magical heritage.'
    book_isbn = '978-0-7475-3269-9'
    book_publication_date = '1997-06-26'
    cover_image = open(get_test_image_path("harry_potter_cover.jpg"), "rb")
    response = context.client.post(
      "/v1/books",
      data = { "title": book_title, "author_id": str(author_id), "description": book_description, "isbn": book_isbn, "publication_date": book_publication_date },
      files = { "cover_image": ("harry_potter_cover.jpg", cover_image, "image/jpeg") },
      headers = get_auth_headers(self.admin_auth_token)
    )
    cover_image.close()
    assert response.status_code == 200
    data = response.json()
    assert data['id'] is not None
    assert data['title'] == book_title
    assert data['description'] == book_description
    assert data['isbn'] == book_isbn
    assert data['publication_date'] == book_publication_date
    cover_image_key = f"public/user-content/cover-images/{data['id']}.jpg"
    assert data['cover_image_url'] is not None
    assert f"user-content/cover-images/{data['id']}.jpg" in data['cover_image_url']
    assert file_exists(context.storage_service_url, context.storage_access_key_id, context.storage_secret_access_key, context.storage_bucket_name, cover_image_key)

  def test_create_book_with_duplicate_title(self, context: Context):
    author_id = uuid4()
    insert_author(context.db_url, author_id, 'J. K. Rowling')
    book_title = 'Harry Potter'
    insert_book(context.db_url, uuid4(), book_title, author_id)
    response = context.client.post("/v1/books", data = { "title": book_title, "author_id": str(author_id) }, headers = get_auth_headers(self.admin_auth_token))
    assert response.status_code == 200
    data = response.json()
    assert data['id'] is not None
    assert data['title'] == book_title

  def test_get_books_no_search_term(self, context: Context):
    author_id = uuid4()
    insert_author(context.db_url, author_id, 'J. K. Rowling')
    book_id_1 = uuid4()
    book_id_2 = uuid4()
    insert_book(context.db_url, book_id_1, 'Harry Potter', author_id)
    insert_book(context.db_url, book_id_2, 'The Lord of the Rings', author_id)
    response = context.client.get("/v1/books", headers = get_auth_headers(self.auth_token))
    assert response.status_code == 200
    data = response.json()
    assert data['total_books'] == 2
    assert data['total_pages'] == 1
    assert data['current_page'] == 1
    assert data['page_size'] == 10
    assert len(data['books']) == 2
    returned_ids = { book['id'] for book in data['books'] }
    assert str(book_id_1) in returned_ids
    assert str(book_id_2) in returned_ids

  def test_get_books_with_search_term(self, context: Context):
    author_id = uuid4()
    insert_author(context.db_url, author_id, 'J. K. Rowling')
    harry_id = uuid4()
    insert_book(context.db_url, harry_id, 'Harry Potter', author_id)
    insert_book(context.db_url, uuid4(), 'The Lord of the Rings', author_id)
    response = context.client.get("/v1/books", params = { "search_term": "Potter" }, headers = get_auth_headers(self.auth_token))
    assert response.status_code == 200
    data = response.json()
    assert data['total_books'] == 1
    assert len(data['books']) == 1
    assert data['books'][0]['id'] == str(harry_id)
    assert data['books'][0]['title'] == 'Harry Potter'

  def test_get_books_pagination(self, context: Context):
    author_id = uuid4()
    insert_author(context.db_url, author_id, 'J. K. Rowling')
    book_id_1 = uuid4()
    book_id_2 = uuid4()
    insert_book(context.db_url, book_id_1, 'Harry Potter', author_id)
    insert_book(context.db_url, book_id_2, 'The Lord of the Rings', author_id)
    response = context.client.get("/v1/books", params = { "page": 1, "page_size": 50 }, headers = get_auth_headers(self.auth_token))
    assert response.status_code == 200
    data = response.json()
    assert data['total_books'] == 2
    assert data['current_page'] == 1
    assert data['page_size'] == 50
    assert len(data['books']) == 2
    returned_ids = { book['id'] for book in data['books'] }
    assert str(book_id_1) in returned_ids
    assert str(book_id_2) in returned_ids

  def test_get_books_invalid_page_size(self, context: Context):
    response = context.client.get("/v1/books", params = { "page_size": 7 }, headers = get_auth_headers(self.auth_token))
    assert response.status_code == 400
    data = response.json()
    assert data == { 'detail': 'INVALID_PAGE_SIZE' }

  def test_get_books_no_results(self, context: Context):
    author_id = uuid4()
    insert_author(context.db_url, author_id, 'J. K. Rowling')
    insert_book(context.db_url, uuid4(), 'Harry Potter', author_id)
    response = context.client.get("/v1/books", params = { "search_term": "NonExistent" }, headers = get_auth_headers(self.auth_token))
    assert response.status_code == 200
    data = response.json()
    assert data['total_books'] == 0
    assert len(data['books']) == 0
    assert data['total_pages'] == 0
