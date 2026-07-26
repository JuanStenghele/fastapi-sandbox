from fastapi import APIRouter, Depends, HTTPException, Query, status
from dependency_injector.wiring import inject, Provide
from sqlmodel import Session
from constants import Tags, MAX_DELETE_IDS
from inject import Container
from objects.display import AuthorCreationHTTPRequest, AuthorCreationHTTPResponse, AuthorHTTPResponse, AuthorsHTTPResponse
from objects.error import ValidationError
from services.author_service import AuthorService
from logging import Logger
from controllers.dependencies import get_session, get_admin_auth_claims, get_user_auth_claims
from objects.author import Author
from objects.auth import AuthClaims
from uuid import UUID


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


@router.get("/authors/{id}", response_model = AuthorHTTPResponse, tags = [Tags.AUTHORS])
@inject
def get_author(
  id: UUID,
  _: AuthClaims = Depends(get_user_auth_claims),
  author_service: AuthorService = Depends(Provide[Container.author_service]),
  session: Session = Depends(get_session),
  logger: Logger = Depends(Provide[Container.logger])
):
  try:
    author = author_service.get_author(session, id)
  except Exception as e:
    logger.error(f"Error getting author: {e}")
    raise HTTPException(detail = "UNKNOWN_ERROR", status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)
  if author is None:
    raise HTTPException(detail = "AUTHOR_NOT_FOUND", status_code = status.HTTP_404_NOT_FOUND)
  return author


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


@router.delete("/authors", status_code = status.HTTP_204_NO_CONTENT, tags = [Tags.AUTHORS])
@inject
def delete_authors(
  ids: list = Query(description = f"List of author IDs to delete (max {MAX_DELETE_IDS})"),
  _: AuthClaims = Depends(get_admin_auth_claims),
  author_service: AuthorService = Depends(Provide[Container.author_service]),
  session: Session = Depends(get_session),
  logger: Logger = Depends(Provide[Container.logger])
):
  try:
    author_service.delete_authors(session, [UUID(str(id)) for id in ids])
  except ValidationError as e:
    raise HTTPException(detail = e.detail, status_code = status.HTTP_400_BAD_REQUEST)
  except ValueError as e:
    raise HTTPException(detail = f"INVALID_UUID: {e}", status_code = status.HTTP_400_BAD_REQUEST)
  except Exception as e:
    logger.error(f"Error deleting authors: {e}")
    raise HTTPException(detail = "UNKNOWN_ERROR", status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)
