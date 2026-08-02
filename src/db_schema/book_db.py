from datetime import date, datetime
from uuid import UUID
from sqlmodel import SQLModel, Field


class Book(SQLModel, table = True):
  __tablename__: str = "books"

  id: UUID = Field(primary_key = True, index = True)
  title: str = Field(nullable = False)
  description: str | None = Field(default = None, nullable = True)
  isbn: str | None = Field(default = None, nullable = True)
  publication_date: date | None = Field(default = None, nullable = True)
  cover_image_stored_object_id: UUID = Field(foreign_key = "stored_objects.id", nullable = True)
  created_at: datetime = Field(nullable = False)
  updated_at: datetime = Field(nullable = False)
  deleted_at: datetime | None = Field(default = None, nullable = True)
