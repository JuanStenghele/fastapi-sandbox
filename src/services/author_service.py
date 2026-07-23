import uuid


from math import ceil
from datetime import datetime, timezone
from dal.author_dal import AuthorDAL
from objects.author import Author, GetAuthorsResult, GetAuthorsPaginatedResult
from objects.error import ValidationError
from constants import DEFAULT_PAGE_SIZES
from sqlmodel import Session


class AuthorService():
  def __init__(self, author_dal: AuthorDAL) -> None:
    self.author_dal: AuthorDAL = author_dal

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
