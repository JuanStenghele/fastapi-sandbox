from datetime import datetime
from uuid import UUID
from objects.base import OrmObj


class BookCover(OrmObj):
  book_id: UUID
  source: str
  url: str
  created_at: datetime
  updated_at: datetime
  deleted_at: datetime | None = None
