from constants import DEFAULT_CONTENT_TYPE
from objects.base import BaseObj


class StoredObject(BaseObj):
  def __init__(self, body: bytes, content_type: str = DEFAULT_CONTENT_TYPE):
    self.body = body
    self.content_type = content_type
