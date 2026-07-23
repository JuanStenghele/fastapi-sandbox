from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide
from sqlmodel import Session
from constants import Tags
from inject import Container
from objects.display import AuthorCreationHTTPRequest, AuthorCreationHTTPResponse, AuthorsHTTPResponse
from objects.error import ValidationError
from services.author_service import AuthorService
from logging import Logger
from controllers.dependencies import get_session, get_admin_auth_claims, get_user_auth_claims
from objects.author import Author
from objects.auth import AuthClaims


router = APIRouter()


@router.post("/authors", response_model = AuthorCreationHTTPResponse, tags = [Tags.AUTHORS])
@inject
def create_author(
  author: AuthorCreationHTTPRequest,
  _: AuthClaims = Depends(get_admin_auth_claims),
  author_service: AuthorService = Depends(Provide[Container.author_service]),
  session: Session = Depends(get_session),
  logger: Logger = Depends(Provide[Container.logger])
):
  try:
    result: Author = author_service.create_author(session, author.name)
    return AuthorCreationHTTPResponse.from_author(result)
  except Exception as e:
    logger.error(f"Error creating author: {e}")
    raise HTTPException(detail = "UNKNOWN_ERROR", status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/authors", response_model = AuthorsHTTPResponse, tags = [Tags.AUTHORS])
@inject
def get_authors(
  search_term: str | None = None,
  page: int = 1,
  page_size: int = 10,
  _: AuthClaims = Depends(get_user_auth_claims),
  author_service: AuthorService = Depends(Provide[Container.author_service]),
  session: Session = Depends(get_session),
  logger: Logger = Depends(Provide[Container.logger])
):
  try:
    result = author_service.get_authors_paginated(session, search_term, page, page_size)
  except ValidationError as e:
    raise HTTPException(detail = e.detail, status_code = status.HTTP_400_BAD_REQUEST)
  except Exception as e:
    logger.error(f"Error getting authors: {e}")
    raise HTTPException(detail = "UNKNOWN_ERROR", status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)
  return AuthorsHTTPResponse.from_authors_result(result)
