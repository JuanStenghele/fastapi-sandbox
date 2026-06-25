from unittest.mock import MagicMock
from clients.storage_client import StorageClient
from objects.stored_object import StoredObject
from services.storage_reverse_proxy import StorageReverseProxy
from constants import PUBLIC_PATH


class TestStorageReverseProxy():
  def test_get_stored_object_returns_result(self):
    storage_client_mock = MagicMock(spec = StorageClient)
    stored_object = StoredObject(body = b"data", content_type = "image/png")
    storage_client_mock.get.return_value = stored_object
    instance = StorageReverseProxy(storage_client_mock)
    result = instance.get_stored_object("images/photo.png")
    storage_client_mock.get.assert_called_once_with(f"{PUBLIC_PATH}/images/photo.png")
    assert result == stored_object

  def test_get_stored_object_returns_none(self):
    storage_client_mock = MagicMock(spec = StorageClient)
    storage_client_mock.get.return_value = None
    instance = StorageReverseProxy(storage_client_mock)
    result = instance.get_stored_object("missing.txt")
    storage_client_mock.get.assert_called_once_with(f"{PUBLIC_PATH}/missing.txt")
    assert result is None
