from datetime import date
from uuid import UUID
from objects.base import BaseObj
from objects.author import Author
from objects.book import Book


class BookCreationRequest(BaseObj):
  title: str
  description: str | None = None
  isbn: str | None = None
  publication_date: date | None = None
  cover_image_id: None = None


class BookCreationResponse(BookCreationRequest):
  id: UUID

  @classmethod
  def from_book(cls, book: Book):
    return cls(
      id = book.id,
      title = book.title,
      description = book.description,
      isbn = book.isbn,
      publication_date = book.publication_date,
      cover_image_id = None
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
