from datetime import date
from uuid import UUID
from fastapi import File, Form, UploadFile
from pydantic import ConfigDict
from objects.base import BaseObj
from objects.author import Author
from objects.book import Book


class BookCreationRequest(BaseObj):
  model_config = ConfigDict(arbitrary_types_allowed = True)

  title: str
  description: str | None = None
  isbn: str | None = None
  publication_date: date | None = None
  cover_image_id: None = None
  cover_image: UploadFile | None = None

  @classmethod
  def as_form(
    cls,
    title: str = Form(...),
    description: str | None = Form(None),
    isbn: str | None = Form(None),
    publication_date: date | None = Form(None),
    cover_image: UploadFile | None = File(None),
  ):
    return cls(
      title = title,
      description = description,
      isbn = isbn,
      publication_date = publication_date,
      cover_image = cover_image,
    )


class BookCreationResponse(BaseObj):
  id: UUID
  title: str
  description: str | None = None
  isbn: str | None = None
  publication_date: date | None = None
  cover_image_id: UUID | None = None
  cover_image_url: str | None = None

  @classmethod
  def from_book(cls, book: Book):
    return cls(
      id = book.id,
      title = book.title,
      description = book.description,
      isbn = book.isbn,
      publication_date = book.publication_date,
      cover_image_id = book.cover_image_id,
      cover_image_url = book.cover_image_url
    )


class AuthorCreationRequest(BaseObj):
  name: str


class AuthorCreationResponse(AuthorCreationRequest):
  id: UUID

  @classmethod
  def from_author(cls, author: Author):
    return cls(
      id = author.id,
      name = author.name
    )
