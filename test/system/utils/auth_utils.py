import httpx


def get_auth_headers(token: str) -> dict:
  return {"Authorization": f"Bearer {token}"}


def get_auth_token(token_url: str, user_id: str) -> str:
  response = httpx.post(
    token_url,
    data = {"grant_type": "client_credentials", "client_id": user_id, "client_secret": "secret"}
  )
  return response.json()["access_token"]
