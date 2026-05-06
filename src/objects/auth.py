from pydantic import ConfigDict
from objects.base import BaseObj


class AuthClaims(BaseObj):
  model_config = ConfigDict(extra = "ignore")

  sub: str
  scope: str | None = None
  iss: str | None = None
  aud: str | list[str] | None = None
  exp: int | None = None
  iat: int | None = None
