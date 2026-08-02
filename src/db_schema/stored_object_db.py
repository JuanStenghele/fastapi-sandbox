from datetime import datetime
from uuid import UUID
from sqlmodel import SQLModel, Field


class StoredObject(SQLModel, table = True):
  __tablename__: str = "stored_objects"

  id: UUID = Field(primary_key = True, index = True)
  source: str = Field(nullable = False)
  key: str = Field(nullable = False)
  public_url: str = Field(nullable = True)
  created_at: datetime = Field(nullable = False)
  updated_at: datetime = Field(nullable = False)
  deleted_at: datetime | None = Field(default = None, nullable = True)
