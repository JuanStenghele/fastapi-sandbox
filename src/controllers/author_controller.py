from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide
from sqlmodel import Session
from constants import Tags
from inject import Container
from objects.display import AuthorCreationRequest, AuthorCreationResponse
from services.author_service import AuthorService
from logging import Logger
from controllers.dependencies import get_session, get_admin_auth_claims
from objects.author import Author
from objects.auth import AuthClaims


router = APIRouter()


@router.post("/authors", response_model = AuthorCreationResponse, tags = [Tags.AUTHORS])
@inject
def create_author(
  author: AuthorCreationRequest,
  _: AuthClaims = Depends(get_admin_auth_claims),
  author_service: AuthorService = Depends(Provide[Container.author_service]),
  session: Session = Depends(get_session),
  logger: Logger = Depends(Provide[Container.logger])
):
  try:
    result: Author = author_service.create_author(session, author.name)
    return AuthorCreationResponse.from_author(result)
  except Exception as e:
    logger.error(f"Error creating author: {e}")
    raise HTTPException(detail = "UNKNOWN_ERROR", status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)
