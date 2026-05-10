from datetime import datetime
from uuid import UUID
from objects.base import OrmObj


class Author(OrmObj):
  id: UUID
  name: str
  created_at: datetime
  updated_at: datetime
  deleted_at: datetime | None
