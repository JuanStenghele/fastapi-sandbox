import jwt


from jwt import PyJWKClient
from constants import AUTH_ALGORITHM
from objects.auth import AuthClaims
from objects.error import UnauthenticatedError, UnauthorizedError


class AuthService():
  def __init__(self, issuer: str, audience: str, jwks_client: PyJWKClient):
    self.issuer = issuer
    self.audience = audience
    self.jwks_client = jwks_client

  def verify_token(self, token: str, scope: str | None = None) -> AuthClaims:
    signing_key = self.jwks_client.get_signing_key_from_jwt(token)
    try:
      payload = jwt.decode(
        token,
        signing_key.key,
        algorithms = [AUTH_ALGORITHM],
        audience = self.audience,
        issuer = self.issuer
      )
    except Exception:
      raise UnauthenticatedError(detail = "INVALID_TOKEN")
    claims = AuthClaims.model_validate(payload)
    if scope is not None:
      self.verify_permissions(claims, scope)
    return claims

  def verify_permissions(self, claims: AuthClaims, scope: str) -> None:
    if claims.scope is None or scope not in claims.scope.split():
      raise UnauthorizedError(detail = "INSUFFICIENT_PERMISSIONS")
