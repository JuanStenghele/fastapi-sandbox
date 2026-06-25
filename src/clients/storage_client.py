import mimetypes
from abc import ABC, abstractmethod
from objects.stored_object import StoredObject


USER_CONTENT_PATH = "user-content"


class StorageClientError(Exception):
  pass


class StorageClient(ABC):
  @abstractmethod
  def source(self) -> str:
    pass

  @abstractmethod
  def health_check(self) -> bool:
    pass

  @abstractmethod
  def upload(self, name: str, data: bytes, content_type: str, public: bool = False) -> str | None:
    pass

  @abstractmethod
  def get(self, key: str) -> StoredObject | None:
    pass

  @abstractmethod
  def abs_upload(self, name: str, data: bytes, content_type: str, public: bool) -> str | None:
    pass

  def upload(self, name: str, data: bytes, content_type: str, public: bool = False) -> str | None:
    extension = mimetypes.guess_extension(content_type)
    if extension is not None and not name.endswith(extension):
      name = f"{name}{extension}"
    return self.abs_upload(name, data, content_type, public)

  def upload_user_content(self, name: str, data: bytes, content_type: str) -> str:
    return self.upload(f"{USER_CONTENT_PATH}/{name}", data, content_type, public = True)
