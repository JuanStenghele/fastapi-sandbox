import mimetypes


from collections.abc import Iterator
from pydantic import ConfigDict
from constants import DEFAULT_CONTENT_TYPE
from objects.base import BaseObj
from abc import ABC, abstractmethod


class StoredObject(BaseObj):
  model_config = ConfigDict(arbitrary_types_allowed = True)

  body: Iterator[bytes]
  content_type: str = DEFAULT_CONTENT_TYPE


class StoredObjectUploadResult(BaseObj):
  url: str | None
  path: str


class ObjectToStore(ABC):
  def __init__(self, data: bytes, content_type: str = DEFAULT_CONTENT_TYPE):
    self.data = data
    self.content_type = content_type

  @abstractmethod
  def key(self, id: str) -> str:
    pass


class ObjectToStoreInS3(ObjectToStore):
  ID = '{id}'
  EXT = '{ext}'

  def __init__(self, key: str | None, data: bytes, key_template: str | None = None, content_type: str = DEFAULT_CONTENT_TYPE):
    super().__init__(data, content_type)
    self.s3_key = key
    self.key_template = key_template

  @classmethod
  def with_key_template(cls, key_template: str, data: bytes, content_type: str = DEFAULT_CONTENT_TYPE):
    return cls(None, data, key_template, content_type)

  def key(self, id: str) -> str:
    if self.s3_key is not None:
      return self.s3_key
    key = self.key_template.replace(self.ID, id)
    if self.EXT in key:
      ext = mimetypes.guess_extension(self.content_type) or ''
      key = self.key_template.replace(self.EXT, ext.lstrip('.'))
    return key
