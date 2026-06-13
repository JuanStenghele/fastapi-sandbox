from unittest.mock import MagicMock
from clients.storage_client import StorageClient, USER_CONTENT_PATH


class FakeStorageClient(StorageClient):
  def source(self) -> str:
    return "fake"

  def health_check(self) -> bool:
    return True

  def upload(self, name: str, data: bytes, content_type: str, public: bool = False) -> str:
    pass


class TestStorageClient():
  def test_upload_user_content_calls_upload_with_correct_path(self):
    instance = FakeStorageClient()
    instance.upload = MagicMock(return_value = "https://example.com/file.jpg")
    result = instance.upload_user_content("images/123", b"data", "image/jpeg")
    instance.upload.assert_called_once_with(f"{USER_CONTENT_PATH}/images/123", b"data", "image/jpeg", public = True)
    assert result == "https://example.com/file.jpg"
