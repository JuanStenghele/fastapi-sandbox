from abc import ABC, abstractmethod
from clients.s3_client import S3Client
from services.storage_service import StorageService
from objects.stored_object import StoredObjectContent
from constants import PUBLIC_PATH


class StorageReverseProxy(ABC):
  @abstractmethod
  def get_stored_object(self, path: str) -> StoredObjectContent | None:
    pass


class S3StorageReverseProxy(StorageReverseProxy):
  def __init__(self, storage_service: StorageService, s3_storage_client: S3Client) -> None:
    self.storage_service = storage_service
    self.s3_storage_client = s3_storage_client

  def get_stored_object(self, path: str) -> StoredObjectContent | None:
    key = f"{PUBLIC_PATH}/{path}"
    return self.storage_service.get_stored_object_content_by_key(self.s3_storage_client, key)
