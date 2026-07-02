from datetime import date, datetime
from uuid import UUID
from objects.base import BaseObj, OrmObj
from objects.cover_image import CoverImage


class Book(OrmObj):
  id: UUID
  title: str
  author_id: UUID
  description: str | None = None
  isbn: str | None = None
  publication_date: date | None = None
  cover_image: CoverImage | None = None
  created_at: datetime
  updated_at: datetime
  deleted_at: datetime | None = None


class GetBooksResult(BaseObj):
  books: list
  total_books: int


class GetBooksPaginatedResult(BaseObj):
  books: list
  total_books: int
  total_pages: int
  current_page: int
  page_size: int
