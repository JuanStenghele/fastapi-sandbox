import httpx


def get_jwks_uri(issuer: str) -> str:
  discovery = httpx.get(f"{issuer.rstrip('/')}/.well-known/openid-configuration").json()
  return discovery["jwks_uri"]
