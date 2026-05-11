from datetime import date, datetime
from uuid import UUID
from objects.base import OrmObj


class Book(OrmObj):
  id: UUID
  title: str
  description: str | None = None
  isbn: str | None = None
  publication_date: date | None = None
  cover_image_id: UUID | None = None
  cover_image_url: str | None = None
  created_at: datetime
  updated_at: datetime
  deleted_at: datetime | None = None
