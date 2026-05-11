from objects.base import BaseObj


class RawImage(BaseObj):
  data: bytes
  content_type: str
