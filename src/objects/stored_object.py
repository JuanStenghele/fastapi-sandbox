from collections.abc import Iterator
from pydantic import ConfigDict
from constants import DEFAULT_CONTENT_TYPE
from objects.base import BaseObj


class StoredObject(BaseObj):
  model_config = ConfigDict(arbitrary_types_allowed = True)

  body: Iterator[bytes]
  content_type: str = DEFAULT_CONTENT_TYPE
