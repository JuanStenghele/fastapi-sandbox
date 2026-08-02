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


class AuthorUpsertHTTPRequest(BaseObj):
  name: str


class AuthorCreationHTTPResponse(AuthorUpsertHTTPRequest):
  id: UUID

  @classmethod
  def from_author(cls, author: Author):
    return cls(
      id = author.id,
      name = author.name
    )


class AuthorHTTPResponse(BaseObj):
  id: UUID
  name: str

  @classmethod
  def from_author(cls, author: Author):
    return cls(
      id = author.id,
      name = author.name
    )


class AuthorsHTTPResponse(BaseObj):
  authors: list
  total_authors: int
  total_pages: int
  current_page: int
  page_size: int

  @classmethod
  def from_authors_result(cls, result: GetAuthorsPaginatedResult):
    return cls(
      authors = [AuthorHTTPResponse.from_author(author) for author in result.authors],
      total_authors = result.total_authors,
      total_pages = result.total_pages,
      current_page = result.current_page,
      page_size = result.page_size
    )
