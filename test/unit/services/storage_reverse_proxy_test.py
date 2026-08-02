from unittest.mock import MagicMock
from clients.s3_client import S3Client
from objects.stored_object import StoredObjectContent
from services.storage_reverse_proxy import S3StorageReverseProxy
from services.storage_service import StorageService
from constants import PUBLIC_PATH


class TestS3StorageReverseProxy():
  def test_get_stored_object_returns_result(self):
    storage_service_mock = MagicMock(spec = StorageService)
    s3_storage_client_mock = MagicMock(spec = S3Client)
    stored_object = StoredObjectContent(body = iter([b"data"]), content_type = "image/png")
    storage_service_mock.get_stored_object_content_by_key.return_value = stored_object
    instance = S3StorageReverseProxy(storage_service_mock, s3_storage_client_mock)

    result = instance.get_stored_object("images/photo.png")

    storage_service_mock.get_stored_object_content_by_key.assert_called_once_with(s3_storage_client_mock, f"{PUBLIC_PATH}/images/photo.png")
    assert result == stored_object

  def test_get_stored_object_returns_none(self):
    storage_service_mock = MagicMock(spec = StorageService)
    s3_storage_client_mock = MagicMock(spec = S3Client)
    storage_service_mock.get_stored_object_content_by_key.return_value = None
    instance = S3StorageReverseProxy(storage_service_mock, s3_storage_client_mock)

    result = instance.get_stored_object("missing.txt")

    storage_service_mock.get_stored_object_content_by_key.assert_called_once_with(s3_storage_client_mock, f"{PUBLIC_PATH}/missing.txt")
    assert result is None
