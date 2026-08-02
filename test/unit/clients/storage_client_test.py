from unittest.mock import MagicMock
from clients.storage_client import StorageClient, USER_CONTENT_PATH
from objects.stored_object import StoredObject, StoredObjectUploadResult


class FakeStorageClient(StorageClient):
  def source(self) -> str:
    return "fake"

  def health_check(self) -> bool:
    return True

  def get_object(self, key: str) -> StoredObject | None:
    pass

  def upload_object(self, name: str, data: bytes, content_type: str, public: bool = False) -> StoredObjectUploadResult:
    pass

  def delete_objects(self, names: list) -> None:
    pass


class TestStorageClient():
  def test_upload_user_content_calls_upload_with_correct_path(self):
    instance = FakeStorageClient()
    instance.upload_object = MagicMock(return_value = StoredObjectUploadResult(public_url = "https://example.com/file.jpg", path = "public/user-content/images/123"))
    result = instance.upload_user_content("images/123", b"data", "image/jpeg")
    instance.upload_object.assert_called_once_with(f"{USER_CONTENT_PATH}/images/123", b"data", "image/jpeg", public = True)
    assert result.public_url == "https://example.com/file.jpg"
    assert result.path == "public/user-content/images/123"
