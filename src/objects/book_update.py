from datetime import date
from uuid import UUID
from objects.base import BaseObj


class BookUpdateRequest(BaseObj):
  title: str | None = None
  author_id: UUID | None = None
  description: str | None = None
  isbn: str | None = None
  publication_date: date | None = None
