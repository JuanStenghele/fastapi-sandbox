from uuid import UUID
from objects.base import BaseObj


class CoverImage(BaseObj):
  stored_object_id: UUID
  book_id: UUID
  url: str
