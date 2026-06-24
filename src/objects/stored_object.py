from constants import DEFAULT_CONTENT_TYPE
from objects.base import BaseObj


class StoredObject(BaseObj):
  body: bytes
  content_type: str = DEFAULT_CONTENT_TYPE
