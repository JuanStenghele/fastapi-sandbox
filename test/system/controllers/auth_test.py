from system.conftest import Context
from system.utils.auth_utils import get_auth_headers, get_user_auth_token


class TestAuth():
  def test_missing_token(self, context: Context):
    response = context.client.get("/v1/books", params = { "id": "123" })
    assert response.status_code == 401
    assert response.json() == { "detail": "MISSING_TOKEN" }

  def test_invalid_token(self, context: Context):
    token = get_user_auth_token(context.auth_token_url, "test-user")
    invalid_token = token[:-10] + "invalid"
    response = context.client.get("/v1/books", params = { "id": "123" }, headers = get_auth_headers(invalid_token))
    assert response.status_code == 401
    assert response.json() == { "detail": "INVALID_TOKEN" }
