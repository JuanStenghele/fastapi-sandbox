from uuid import UUID
from objects.base import BaseObj


class CoverImage(BaseObj):
  id: UUID
  url: str
