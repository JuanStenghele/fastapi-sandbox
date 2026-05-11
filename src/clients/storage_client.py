from abc import ABC, abstractmethod


class StorageClient(ABC):
  @property
  @abstractmethod
  def source(self) -> str:
    pass

  @abstractmethod
  def upload(self, key: str, data: bytes, content_type: str) -> str:
    pass
