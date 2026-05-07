import pytest, jwt


from unittest.mock import MagicMock
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from jwt import PyJWKClient
from services.auth import AuthService
from objects.error import UnauthenticatedError, UnauthorizedError


issuer = "https://example.com"
audience = "default"


def generate_rsa_key_pair():
  private_key = rsa.generate_private_key(
    public_exponent = 65537,
    key_size = 2048,
    backend = default_backend()
  )
  return private_key, private_key.public_key()


class TestAuthService():
  def test_verify_token_success(self):
    private_key, public_key = generate_rsa_key_pair()
    token = jwt.encode({"sub": "user1", "iss": issuer, "aud": audience}, private_key, algorithm = "RS256")
    signing_key_mock = MagicMock()
    signing_key_mock.key = public_key
    jwks_client_mock = MagicMock(spec = PyJWKClient)
    jwks_client_mock.get_signing_key_from_jwt.return_value = signing_key_mock
    instance = AuthService(issuer, audience, jwks_client_mock)
    claims = instance.verify_token(token)
    assert claims.sub == "user1"

  def test_verify_token_signing_key_error(self):
    jwks_client_mock = MagicMock(spec = PyJWKClient)
    jwks_client_mock.get_signing_key_from_jwt.side_effect = Exception("key not found")
    instance = AuthService(issuer, audience, jwks_client_mock)
    with pytest.raises(Exception) as e:
      instance.verify_token("some_token")
    assert str(e.value) == "key not found"

  def test_verify_token_invalid_token(self):
    jwks_client_mock = MagicMock(spec = PyJWKClient)
    jwks_client_mock.get_signing_key_from_jwt.return_value = MagicMock()
    instance = AuthService(issuer, audience, jwks_client_mock)
    with pytest.raises(UnauthenticatedError) as e:
      instance.verify_token("invalid.token.string")
    assert e.value.detail == "INVALID_TOKEN"

  def test_verify_token_scope_is_none(self):
    private_key, public_key = generate_rsa_key_pair()
    token = jwt.encode({"sub": "user1", "iss": issuer, "aud": audience}, private_key, algorithm = "RS256")
    signing_key_mock = MagicMock()
    signing_key_mock.key = public_key
    jwks_client_mock = MagicMock(spec = PyJWKClient)
    jwks_client_mock.get_signing_key_from_jwt.return_value = signing_key_mock
    instance = AuthService(issuer, audience, jwks_client_mock)
    with pytest.raises(UnauthorizedError) as e:
      instance.verify_token(token, scope = "admin")
    assert e.value.detail == "INSUFFICIENT_PERMISSIONS"

  def test_verify_token_scope_not_in_claims(self):
    private_key, public_key = generate_rsa_key_pair()
    token = jwt.encode({"sub": "user1", "iss": issuer, "aud": audience, "scope": "user"}, private_key, algorithm = "RS256")
    signing_key_mock = MagicMock()
    signing_key_mock.key = public_key
    jwks_client_mock = MagicMock(spec = PyJWKClient)
    jwks_client_mock.get_signing_key_from_jwt.return_value = signing_key_mock
    instance = AuthService(issuer, audience, jwks_client_mock)
    with pytest.raises(UnauthorizedError) as e:
      instance.verify_token(token, scope = "admin")
    assert e.value.detail == "INSUFFICIENT_PERMISSIONS"
