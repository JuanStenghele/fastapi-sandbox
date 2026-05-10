from datetime import datetime
from uuid import UUID
from sqlmodel import SQLModel, Field


class BookCover(SQLModel, table = True):
  __tablename__: str = "book_covers"

  id: UUID = Field(primary_key = True, index = True)
  source: str = Field(nullable = False)
  url: str = Field(nullable = False)
  created_at: datetime = Field(nullable = False)
  updated_at: datetime = Field(nullable = False)
  deleted_at: datetime | None = Field(default = None, nullable = True)
