from datetime import datetime
from uuid import UUID
from sqlmodel import SQLModel, Field


class BookAuthor(SQLModel, table = True):
  __tablename__: str = "book_authors"

  book_id: UUID = Field(foreign_key = "books.id", primary_key = True)
  author_id: UUID = Field(foreign_key = "authors.id", primary_key = True)
  created_at: datetime = Field(nullable = False)
  deleted_at: datetime | None = Field(default = None, nullable = True)
