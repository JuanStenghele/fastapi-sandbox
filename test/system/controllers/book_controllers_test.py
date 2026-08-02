import pytest

from uuid import uuid4
from system.test_utils.db_utils import insert_author, insert_book, clean_all_tables
from system.test_utils.auth_utils import get_auth_headers, get_user_auth_token, get_admin_auth_token
from system.test_utils.storage_utils import get_test_image_path, clean_bucket, file_exists
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
    assert data['cover_image_url'] is not None
    assert "cover-images/" in data['cover_image_url']
    stored_object_id = data['cover_image_url'].split("cover-images/")[1].split(".")[0]
    cover_image_key = f"public/cover-images/{stored_object_id}.jpg"
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

  def test_delete_books_success(self, context: Context):
    author_id = uuid4()
    insert_author(context.db_url, author_id, 'J. K. Rowling')
    book_id_1 = uuid4()
    book_id_2 = uuid4()
    insert_book(context.db_url, book_id_1, 'Harry Potter', author_id)
    insert_book(context.db_url, book_id_2, 'The Lord of the Rings', author_id)
    response = context.client.delete("/v1/books", params = { "ids": [str(book_id_1), str(book_id_2)] }, headers = get_auth_headers(self.admin_auth_token))
    assert response.status_code == 204

  def test_delete_books_without_admin_scope(self, context: Context):
    auth_token = get_user_auth_token(context.auth_token_url, "test-user")
    response = context.client.delete("/v1/books", params = { "ids": [str(uuid4())] }, headers = get_auth_headers(auth_token))
    assert response.status_code == 403
    data = response.json()
    assert data == { 'detail': 'INSUFFICIENT_PERMISSIONS' }

  def test_delete_books_no_auth(self, context: Context):
    response = context.client.delete("/v1/books", params = { "ids": [str(uuid4())] })
    assert response.status_code == 401
    data = response.json()
    assert data == { 'detail': 'MISSING_TOKEN' }

  def test_delete_books_nonexistent_ids(self, context: Context):
    author_id = uuid4()
    insert_author(context.db_url, author_id, 'J. K. Rowling')
    book_id = uuid4()
    insert_book(context.db_url, book_id, 'Harry Potter', author_id)
    nonexistent_id = uuid4()
    response = context.client.delete("/v1/books", params = { "ids": [str(book_id), str(nonexistent_id)] }, headers = get_auth_headers(self.admin_auth_token))
    assert response.status_code == 400
    data = response.json()
    assert data['detail'] == f"BOOKS_NOT_FOUND: {str(nonexistent_id)}"

  def test_delete_books_too_many_ids(self, context: Context):
    too_many_ids = [str(uuid4()) for _ in range(101)]
    response = context.client.delete("/v1/books", params = { "ids": too_many_ids }, headers = get_auth_headers(self.admin_auth_token))
    assert response.status_code == 400
    data = response.json()
    assert data == { 'detail': 'INVALID_BOOK_IDS_COUNT' }

  def test_delete_books_invalid_uuid(self, context: Context):
    response = context.client.delete("/v1/books", params = { "ids": ["not-a-uuid"] }, headers = get_auth_headers(self.admin_auth_token))
    assert response.status_code == 400
    data = response.json()
    assert data['detail'] == 'INVALID_UUID: badly formed hexadecimal UUID string'

  def test_delete_book_already_deleted(self, context: Context):
    author_id = uuid4()
    insert_author(context.db_url, author_id, 'J. K. Rowling')
    book_id = uuid4()
    insert_book(context.db_url, book_id, 'Harry Potter', author_id)
    context.client.delete("/v1/books", params = { "ids": [str(book_id)] }, headers = get_auth_headers(self.admin_auth_token))
    response = context.client.delete("/v1/books", params = { "ids": [str(book_id)] }, headers = get_auth_headers(self.admin_auth_token))
    assert response.status_code == 400
    data = response.json()
    assert data['detail'].startswith('BOOKS_NOT_FOUND')

  def test_update_book_success(self, context: Context):
    author_id = uuid4()
    insert_author(context.db_url, author_id, 'J. K. Rowling')
    book_id = uuid4()
    insert_book(context.db_url, book_id, 'Harry Potter', author_id)
    response = context.client.patch(f"/v1/books/{book_id}", json = { "title": "New Title" }, headers = get_auth_headers(self.admin_auth_token))
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == str(book_id)
    assert data['title'] == 'New Title'

  def test_update_book_change_author(self, context: Context):
    author_id_1 = uuid4()
    author_id_2 = uuid4()
    insert_author(context.db_url, author_id_1, 'J. K. Rowling')
    insert_author(context.db_url, author_id_2, 'Robert Galbraith')
    book_id = uuid4()
    insert_book(context.db_url, book_id, 'Harry Potter', author_id_1)
    response = context.client.patch(f"/v1/books/{book_id}", json = { "author_id": str(author_id_2) }, headers = get_auth_headers(self.admin_auth_token))
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == str(book_id)
    assert data['author_id'] == str(author_id_2)

  def test_update_book_not_found(self, context: Context):
    response = context.client.patch(f"/v1/books/{uuid4()}", json = { "title": "New Title" }, headers = get_auth_headers(self.admin_auth_token))
    assert response.status_code == 404
    data = response.json()
    assert data == { 'detail': 'BOOK_NOT_FOUND' }

  def test_update_book_invalid_author(self, context: Context):
    author_id = uuid4()
    insert_author(context.db_url, author_id, 'J. K. Rowling')
    book_id = uuid4()
    insert_book(context.db_url, book_id, 'Harry Potter', author_id)
    response = context.client.patch(f"/v1/books/{book_id}", json = { "author_id": str(uuid4()) }, headers = get_auth_headers(self.admin_auth_token))
    assert response.status_code == 400
    data = response.json()
    assert data == { 'detail': 'AUTHOR_NOT_FOUND' }

  def test_update_book_without_admin_scope(self, context: Context):
    auth_token = get_user_auth_token(context.auth_token_url, "test-user")
    response = context.client.patch(f"/v1/books/{uuid4()}", json = { "title": "New Title" }, headers = get_auth_headers(auth_token))
    assert response.status_code == 403
    data = response.json()
    assert data == { 'detail': 'INSUFFICIENT_PERMISSIONS' }

  def test_update_book_no_auth(self, context: Context):
    response = context.client.patch(f"/v1/books/{uuid4()}", json = { "title": "New Title" })
    assert response.status_code == 401
    data = response.json()
    assert data == { 'detail': 'MISSING_TOKEN' }

  def test_delete_book_cover_success(self, context: Context):
    author_id = uuid4()
    insert_author(context.db_url, author_id, 'J. K. Rowling')
    cover_image = open(get_test_image_path("harry_potter_cover.jpg"), "rb")
    create_response = context.client.post(
      "/v1/books",
      data = { "title": "Harry Potter", "author_id": str(author_id) },
      files = { "cover_image": ("harry_potter_cover.jpg", cover_image, "image/jpeg") },
      headers = get_auth_headers(self.admin_auth_token)
    )
    cover_image.close()
    book_id = create_response.json()['id']
    response = context.client.delete(f"/v1/books/{book_id}/cover-images", headers = get_auth_headers(self.admin_auth_token))
    assert response.status_code == 204

  def test_delete_book_cover_book_not_found(self, context: Context):
    response = context.client.delete(f"/v1/books/{uuid4()}/cover-images", headers = get_auth_headers(self.admin_auth_token))
    assert response.status_code == 404
    data = response.json()
    assert data['detail'].startswith('BOOKS_NOT_FOUND')

  def test_delete_book_cover_without_admin_scope(self, context: Context):
    auth_token = get_user_auth_token(context.auth_token_url, "test-user")
    response = context.client.delete(f"/v1/books/{uuid4()}/cover-images", headers = get_auth_headers(auth_token))
    assert response.status_code == 403
    data = response.json()
    assert data == { 'detail': 'INSUFFICIENT_PERMISSIONS' }

  def test_delete_book_cover_no_auth(self, context: Context):
    response = context.client.delete(f"/v1/books/{uuid4()}/cover-images")
    assert response.status_code == 401
    data = response.json()
    assert data == { 'detail': 'MISSING_TOKEN' }

  def test_update_book_cover_success(self, context: Context):
    author_id = uuid4()
    insert_author(context.db_url, author_id, 'J. K. Rowling')
    cover_image = open(get_test_image_path("harry_potter_cover.jpg"), "rb")
    create_response = context.client.post(
      "/v1/books",
      data = { "title": "Harry Potter", "author_id": str(author_id) },
      files = { "cover_image": ("harry_potter_cover.jpg", cover_image, "image/jpeg") },
      headers = get_auth_headers(self.admin_auth_token)
    )
    cover_image.close()
    book_id = create_response.json()['id']
    new_cover = open(get_test_image_path("harry_potter_cover.jpg"), "rb")
    response = context.client.put(
      f"/v1/books/{book_id}/cover-images",
      files = { "cover_image": ("harry_potter_cover.jpg", new_cover, "image/jpeg") },
      headers = get_auth_headers(self.admin_auth_token)
    )
    new_cover.close()
    assert response.status_code == 200
    data = response.json()
    assert data['book_id'] == book_id
    assert data['url'] is not None

  def test_update_book_cover_book_not_found(self, context: Context):
    cover_image = open(get_test_image_path("harry_potter_cover.jpg"), "rb")
    response = context.client.put(
      f"/v1/books/{uuid4()}/cover-images",
      files = { "cover_image": ("harry_potter_cover.jpg", cover_image, "image/jpeg") },
      headers = get_auth_headers(self.admin_auth_token)
    )
    cover_image.close()
    assert response.status_code == 404
    data = response.json()
    assert data['detail'].startswith("BOOKS_NOT_FOUND")

  def test_update_book_cover_without_admin_scope(self, context: Context):
    auth_token = get_user_auth_token(context.auth_token_url, "test-user")
    cover_image = open(get_test_image_path("harry_potter_cover.jpg"), "rb")
    response = context.client.put(
      f"/v1/books/{uuid4()}/cover-images",
      files = { "cover_image": ("harry_potter_cover.jpg", cover_image, "image/jpeg") },
      headers = get_auth_headers(auth_token)
    )
    cover_image.close()
    assert response.status_code == 403

  def test_update_book_cover_no_auth(self, context: Context):
    cover_image = open(get_test_image_path("harry_potter_cover.jpg"), "rb")
    response = context.client.put(
      f"/v1/books/{uuid4()}/cover-images",
      files = { "cover_image": ("harry_potter_cover.jpg", cover_image, "image/jpeg") }
    )
    cover_image.close()
    assert response.status_code == 401
