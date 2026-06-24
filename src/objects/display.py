from datetime import date
from uuid import UUID
from fastapi import File, Form, UploadFile
from pydantic import ConfigDict
from objects.base import BaseObj
from objects.author import Author
from objects.book import Book
from objects.stored_object import StoredObject


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


class AuthorCreationHTTPRequest(BaseObj):
  name: str


class AuthorCreationHTTPResponse(AuthorCreationHTTPRequest):
  id: UUID

  @classmethod
  def from_author(cls, author: Author):
    return cls(
      id = author.id,
      name = author.name
    )
