import pytest


from system.utils.db_utils import delete_all_authors
from system.utils.auth_utils import get_admin_auth_token, get_auth_headers, get_user_auth_token
from system.conftest import Context


class TestAuthorController():
  @pytest.fixture(autouse = True)
  def after_each(self, context: Context):
    self.auth_token = get_admin_auth_token(context.auth_token_url, "test-admin")
    yield
    delete_all_authors(context.db_url)

  def test_create_author(self, context: Context):
    author_name = 'J. K. Rowling'
    response = context.client.post("/v1/authors", json = { "name": author_name }, headers = get_auth_headers(self.auth_token))
    assert response.status_code == 200
    data = response.json()
    assert data['id'] is not None
    assert data['name'] == author_name

  def test_create_author_with_duplicate_name(self, context: Context):
    author_name = 'J. K. Rowling'
    auth_header = get_auth_headers(self.auth_token)
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
