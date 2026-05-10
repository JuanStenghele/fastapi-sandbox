import json, httpx


def get_mock_oauth2_server_config() -> str:
  return json.dumps({
    "tokenCallbacks": [
      {
        "issuerId": "fastapi-sandbox",
        "requestMappings": [
          {
            "requestParam": "scope",
            "match": "admin",
            "claims": {
              "sub": "${clientId}",
              "aud": ["fastapi-sandbox"],
              "scope": "admin"
            }
          },
          {
            "requestParam": "client_id",
            "match": ".*",
            "claims": {
              "sub": "${clientId}",
              "aud": ["fastapi-sandbox"]
            }
          }
        ]
      }
    ]
  })


def get_auth_headers(token: str) -> dict:
  return {"Authorization": f"Bearer {token}"}


def get_auth_token(token_url: str, user_id: str, scope: str | None = None) -> str:
  data = {"grant_type": "client_credentials", "client_id": user_id, "client_secret": "secret"}
  if scope is not None:
    data["scope"] = scope
  response = httpx.post(
    token_url,
    data = data
  )
  return response.json()["access_token"]


def get_user_auth_token(token_url: str, user_id: str) -> str:
  return get_auth_token(token_url, user_id)


def get_admin_auth_token(token_url: str, user_id: str) -> str:
  return get_auth_token(token_url, user_id, "admin")
