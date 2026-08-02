from abc import ABC, abstractmethod
from objects.stored_object import StoredObjectContent, StoredObjectUploadResult


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
  def get_object(self, key: str) -> StoredObjectContent | None:
    pass

  @abstractmethod
  def upload_object(self, key: str, data: bytes, content_type: str, public: bool = False) -> StoredObjectUploadResult:
    pass

  @abstractmethod
  def delete_objects(self, keys: list) -> None:
    pass

  def upload_user_content(self, name: str, data: bytes, content_type: str) -> StoredObjectUploadResult:
    return self.upload_object(f"{USER_CONTENT_PATH}/{name}", data, content_type, public = True)
