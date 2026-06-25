from unittest.mock import MagicMock
from clients.storage_client import StorageClient, USER_CONTENT_PATH
from objects.stored_object import StoredObject


class FakeStorageClient(StorageClient):
  def source(self) -> str:
    return "fake"

  def health_check(self) -> bool:
    return True

  def get(self, key: str) -> StoredObject | None:
    pass

  def abs_upload(self, name: str, data: bytes, content_type: str, public: bool) -> str:
    pass


class TestStorageClient():
  def test_upload_appends_extension(self):
    instance = FakeStorageClient()
    instance.abs_upload = MagicMock(return_value = "https://example.com/file.jpg")
    result = instance.upload("images/123", b"data", "image/jpeg", public = True)
    instance.abs_upload.assert_called_once_with("images/123.jpg", b"data", "image/jpeg", True)
    assert result == "https://example.com/file.jpg"

  def test_upload_skips_extension_when_present(self):
    instance = FakeStorageClient()
    instance.abs_upload = MagicMock(return_value = "https://example.com/photo.jpg")
    result = instance.upload("images/photo.jpg", b"data", "image/jpeg", public = True)
    instance.abs_upload.assert_called_once_with("images/photo.jpg", b"data", "image/jpeg", True)
    assert result == "https://example.com/photo.jpg"

  def test_upload_skips_unknown_extension(self):
    instance = FakeStorageClient()
    instance.abs_upload = MagicMock(return_value = "https://example.com/file")
    result = instance.upload("images/data", b"data", "application/x-custom", public = True)
    instance.abs_upload.assert_called_once_with("images/data", b"data", "application/x-custom", True)
    assert result == "https://example.com/file"

  def test_upload_user_content_calls_upload_with_correct_path(self):
    instance = FakeStorageClient()
    instance.abs_upload = MagicMock(return_value = "https://example.com/file.jpg")
    result = instance.upload_user_content("images/123", b"data", "image/jpeg")
    instance.abs_upload.assert_called_once_with(f"{USER_CONTENT_PATH}/images/123.jpg", b"data", "image/jpeg", True)
    assert result == "https://example.com/file.jpg"
