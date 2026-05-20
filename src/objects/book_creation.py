from datetime import date
from uuid import UUID
from pydantic import ConfigDict
from objects.base import BaseObj
from objects.image import RawImage


class BookCreationRequest(BaseObj):
  model_config = ConfigDict(arbitrary_types_allowed = True)

  title: str
  author_id: UUID
  description: str | None = None
  isbn: str | None = None
  publication_date: date | None = None
  cover_image: RawImage | None = None
