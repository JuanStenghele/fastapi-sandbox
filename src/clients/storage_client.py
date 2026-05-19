from abc import ABC, abstractmethod


USER_CONTENT_PATH = "user-content"

class StorageClient(ABC):
  @property
  @abstractmethod
  def source(self) -> str:
    pass

  @abstractmethod
  def upload(self, name: str, data: bytes, content_type: str, public: bool = False) -> str:
    pass

  def upload_user_content(self, name: str, data: bytes, content_type: str) -> str:
    return self.upload(f"{USER_CONTENT_PATH}/{name}", data, content_type, public=True)
