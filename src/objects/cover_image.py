from uuid import UUID
from objects.base import BaseObj


class CoverImage(BaseObj):
  book_id: UUID
  url: str
