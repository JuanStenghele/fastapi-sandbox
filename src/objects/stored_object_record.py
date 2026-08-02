from datetime import datetime
from uuid import UUID
from objects.base import OrmObj


class StoredObject(OrmObj):
  id: UUID
  source: str
  key: str
  public_url: str | None = None
  created_at: datetime
  updated_at: datetime
  deleted_at: datetime | None = None
