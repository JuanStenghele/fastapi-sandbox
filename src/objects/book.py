from datetime import date, datetime
from uuid import UUID
from objects.base import BaseObj, OrmObj
from objects.cover_image import CoverImage
from pydantic import ConfigDict
from objects.image import RawImage
from fastapi import File, Form, UploadFile


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


class BookCreationRequest(BaseObj):
  model_config = ConfigDict(arbitrary_types_allowed = True)

  title: str
  author_id: UUID
  description: str | None = None
  isbn: str | None = None
  publication_date: date | None = None
  cover_image: RawImage | None = None


class GetBooksResult(BaseObj):
  books: list
  total_books: int


class GetBooksPaginatedResult(BaseObj):
  books: list
  total_books: int
  total_pages: int
  current_page: int
  page_size: int


class BookUpdateRequest(BaseObj):
  title: str | None = None
  author_id: UUID | None = None
  description: str | None = None
  isbn: str | None = None
  publication_date: date | None = None


class BookCreationHTTPRequest(BaseObj):
  model_config = ConfigDict(arbitrary_types_allowed = True)

  title: str
  author_id: UUID
  description: str | None = None
  isbn: str | None = None
  publication_date: date | None = None
  cover_image_id: None = None
  cover_image: UploadFile | None = None

  @classmethod
  def as_form(
    cls,
    title: str = Form(...),
    author_id: UUID = Form(...),
    description: str | None = Form(None),
    isbn: str | None = Form(None),
    publication_date: date | None = Form(None),
    cover_image: UploadFile | None = File(None),
  ):
    return cls(
      title = title,
      author_id = author_id,
      description = description,
      isbn = isbn,
      publication_date = publication_date,
      cover_image = cover_image,
    )


class BookCreationHTTPResponse(BaseObj):
  id: UUID
  title: str
  description: str | None = None
  isbn: str | None = None
  publication_date: date | None = None
  cover_image_url: str | None = None

  @classmethod
  def from_book(cls, book: Book):
    return cls(
      id = book.id,
      title = book.title,
      description = book.description,
      isbn = book.isbn,
      publication_date = book.publication_date,
      cover_image_url = book.cover_image.url if book.cover_image else None
    )


class BookUpdateHTTPRequest(BaseObj):
  title: str | None = None
  author_id: UUID | None = None
  description: str | None = None
  isbn: str | None = None
  publication_date: date | None = None


class BookHTTPResponse(BaseObj):
  id: UUID
  title: str
  author_id: UUID
  description: str | None = None
  isbn: str | None = None
  publication_date: date | None = None
  cover_image_url: str | None = None
  created_at: datetime

  @classmethod
  def from_book(cls, book: Book):
    return cls(
      id = book.id,
      title = book.title,
      author_id = book.author_id,
      description = book.description,
      isbn = book.isbn,
      publication_date = book.publication_date,
      cover_image_url = book.cover_image.url if book.cover_image else None,
      created_at = book.created_at
    )


class BooksHTTPResponse(BaseObj):
  books: list
  total_books: int
  total_pages: int
  current_page: int
  page_size: int

  @classmethod
  def from_books_result(cls, result: GetBooksPaginatedResult):
    return cls(
      books = [BookHTTPResponse.from_book(book) for book in result.books],
      total_books = result.total_books,
      total_pages = result.total_pages,
      current_page = result.current_page,
      page_size = result.page_size
    )
