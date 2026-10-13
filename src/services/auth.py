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

  def verify_token(self, token: str, permission: str | None = None) -> AuthClaims:
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
    if permission is not None:
      self.verify_permission(claims, permission)
    return claims

  def verify_permission(self, claims: AuthClaims, permission: str) -> None:
    if claims.permissions is None or permission not in claims.permissions:
      raise UnauthorizedError(detail = "INSUFFICIENT_PERMISSIONS")
