class AppError(Exception):
  def __init__(self, detail: str):
    self.detail = detail
    super().__init__(detail)


class AuthError(AppError):
  pass


class UnauthenticatedError(AuthError):
  pass


class UnauthorizedError(AuthError):
  pass


class ValidationError(AppError):
  pass
