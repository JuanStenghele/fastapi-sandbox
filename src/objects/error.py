class AuthError(Exception):
  def __init__(self, detail: str):
    self.detail = detail
    super().__init__(detail)


class UnauthenticatedError(AuthError):
  pass


class UnauthorizedError(AuthError):
  pass
