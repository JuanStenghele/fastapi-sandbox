from datetime import datetime
from uuid import UUID
from objects.base import OrmObj


class BookAuthor(OrmObj):
  book_id: UUID
  author_id: UUID
  created_at: datetime
  deleted_at: datetime | None = None
