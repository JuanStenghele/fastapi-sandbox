from logging import Logger
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session
from inject import Container
from database import Database
from services.auth import AuthService
from objects.auth import AuthClaims
from objects.error import UnauthenticatedError, UnauthorizedError


def get_auth_claims(
  scope: str | None = None,
  credentials: HTTPAuthorizationCredentials | None = Depends(HTTPBearer(auto_error = False)),
  auth_service: AuthService = Depends(lambda: Container.auth_service())
) -> AuthClaims:
  try:
    if credentials is None:
      raise UnauthenticatedError(detail = "MISSING_TOKEN")
    return auth_service.verify_token(credentials.credentials, scope)
  except UnauthenticatedError as e:
    raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = e.detail)
  except UnauthorizedError as e:
    raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = e.detail)


def get_session(
  db: Database = Depends(lambda: Container.db()),
  logger: Logger = Depends(lambda: Container.logger())
) -> Generator[Session, None, None]:
  session = Session(db.engine)
  logger.info(f"DB session {id(session)} opened")
  try:
    yield session
    session.commit()
    logger.info(f"DB session {id(session)} committed")
  except Exception:
    session.rollback()
    logger.info(f"DB session {id(session)} rollback")
    raise
  finally:
    session.close()
    logger.info(f"DB session {id(session)} closed")
