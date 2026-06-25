from clients.storage_client import StorageClient, StoredObject
from constants import PUBLIC_PATH


class StorageReverseProxy():
  def __init__(self, storage_client: StorageClient):
    self.storage_client = storage_client

  def get_stored_object(self, path: str) -> StoredObject | None:
    key = f"{PUBLIC_PATH}/{path}"
    return self.storage_client.get(key)
