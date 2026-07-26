import uuid


from math import ceil
from datetime import datetime, timezone
from uuid import UUID
from dal.author_dal import AuthorDAL
from objects.author import Author, GetAuthorsResult, GetAuthorsPaginatedResult
from objects.error import ValidationError
from constants import DEFAULT_PAGE_SIZES
from sqlmodel import Session
from validators.author_validator import AuthorValidator


class AuthorService():
  def __init__(self, author_dal: AuthorDAL, author_validator: AuthorValidator) -> None:
    self.author_dal: AuthorDAL = author_dal
    self.author_validator: AuthorValidator = author_validator

  def create_author(self, session: Session, author_name: str) -> Author:
    now = datetime.now(timezone.utc)
    author = Author(
      id = uuid.uuid4(),
      name = author_name,
      created_at = now,
      updated_at = now,
      deleted_at = None
    )
    self.author_dal.create_author(session, author)
    return author

  def get_authors(self, session: Session, search_term: str | None, limit: int, offset: int) -> GetAuthorsResult:
    if offset < 0:
      raise ValidationError(detail = "INVALID_OFFSET")
    total_authors = self.author_dal.count_authors(session, search_term)
    authors = self.author_dal.get_authors(session, search_term, limit, offset)
    return GetAuthorsResult(authors = authors, total_authors = total_authors)

  def get_author(self, session: Session, id: UUID) -> Author | None:
    return self.author_dal.get_author(session, id)

  def get_authors_paginated(self, session: Session, search_term: str | None, page: int, page_size: int) -> GetAuthorsPaginatedResult:
    if page_size not in DEFAULT_PAGE_SIZES:
      raise ValidationError(detail = "INVALID_PAGE_SIZE")
    if page < 1:
      raise ValidationError(detail = "INVALID_PAGE")
    offset = (page - 1) * page_size
    result = self.get_authors(session, search_term, page_size, offset)
    return GetAuthorsPaginatedResult(
      authors = result.authors,
      total_authors = result.total_authors,
      total_pages = ceil(result.total_authors / page_size),
      current_page = page,
      page_size = page_size
    )

  def delete_authors(self, session: Session, author_ids: list) -> None:
    self.author_validator.validate_deletion(session, author_ids)
    now = datetime.now(timezone.utc)
    self.author_dal.soft_delete_authors(session, author_ids, now)
