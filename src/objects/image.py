from typing import Annotated, BinaryIO
from pydantic import ConfigDict, SkipValidation
from objects.base import BaseObj


class RawImage(BaseObj):
  model_config = ConfigDict(arbitrary_types_allowed = True)

  file: Annotated[BinaryIO, SkipValidation]
  content_type: str
  size: int | None = None

  def get_size(self) -> int:
    if self.size is not None:
      return self.size
    self.file.seek(0, 2)
    size = self.file.tell()
    self.file.seek(0)
    return size
