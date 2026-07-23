from datetime import datetime
from uuid import UUID
from objects.base import BaseObj, OrmObj


class Author(OrmObj):
  id: UUID
  name: str
  created_at: datetime
  updated_at: datetime
  deleted_at: datetime | None


class GetAuthorsResult(BaseObj):
  authors: list
  total_authors: int


class GetAuthorsPaginatedResult(BaseObj):
  authors: list
  total_authors: int
  total_pages: int
  current_page: int
  page_size: int
