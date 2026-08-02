import pytest


from unittest.mock import MagicMock
from uuid import uuid4
from sqlmodel import Session
from clients.storage_client import StorageClient, StorageClientError
from dal.stored_object_dal import StoredObjectDAL
from dal.book_dal import BookDAL
from objects.stored_object import StoredObjectUploadResult, ObjectToStore, StoredObject
from services.date_provider import DateProvider
from services.storage_service import StorageService


class TestStorageService():
  def test_store_object_success(self):
    now = MagicMock()
    date_provider_mock = MagicMock(spec = DateProvider)
    date_provider_mock.now.return_value = now
    book_dal_mock = MagicMock(spec = BookDAL)
    stored_object_dal_mock = MagicMock(spec = StoredObjectDAL)
    session_mock = MagicMock(spec = Session)
    storage_client_mock = MagicMock(spec = StorageClient)
    storage_client_mock.source.return_value = "s3"
    storage_client_mock.upload_object.return_value = StoredObjectUploadResult(public_url = "https://example.com/file.jpg", path = "public/file.jpg")
    object_mock = MagicMock(spec = ObjectToStore)
    expected_key = "public/file.jpg"
    object_mock.key.return_value = expected_key
    object_mock.data = b"data"
    object_mock.content_type = "image/jpeg"
    instance = StorageService(date_provider_mock, book_dal_mock, stored_object_dal_mock)

    result = instance.store_object(session_mock, storage_client_mock, object_mock)

    object_mock.key.assert_called_once()
    storage_client_mock.upload_object.assert_called_once_with(expected_key, b"data", "image/jpeg", public = True)
    storage_client_mock.source.assert_called_once()
    date_provider_mock.now.assert_called_once()
    stored_object_dal_mock.create_stored_object.assert_called_once()
    assert result.id is not None
    assert result.source == "s3"
    assert result.key == "public/file.jpg"
    assert result.public_url == "https://example.com/file.jpg"
    assert result.created_at is not None
    assert result.updated_at is not None

  def test_store_object_upload_fail(self):
    date_provider_mock = MagicMock(spec = DateProvider)
    book_dal_mock = MagicMock(spec = BookDAL)
    stored_object_dal_mock = MagicMock(spec = StoredObjectDAL)
    session_mock = MagicMock(spec = Session)
    storage_client_mock = MagicMock(spec = StorageClient)
    storage_client_mock.upload_object.side_effect = StorageClientError("upload failed")
    object_mock = MagicMock(spec = ObjectToStore)
    object_mock.key.return_value = "public/file.jpg"
    object_mock.data = b"data"
    object_mock.content_type = "image/jpeg"
    instance = StorageService(date_provider_mock, book_dal_mock, stored_object_dal_mock)

    with pytest.raises(StorageClientError) as exc_info:
      instance.store_object(session_mock, storage_client_mock, object_mock)
    assert str(exc_info.value) == "upload failed"
    stored_object_dal_mock.create_stored_object.assert_not_called()

  def test_store_object_dal_fail(self):
    now = MagicMock()
    date_provider_mock = MagicMock(spec = DateProvider)
    date_provider_mock.now.return_value = now
    book_dal_mock = MagicMock(spec = BookDAL)
    stored_object_dal_mock = MagicMock(spec = StoredObjectDAL)
    stored_object_dal_mock.create_stored_object.side_effect = Exception("dal error")
    session_mock = MagicMock(spec = Session)
    storage_client_mock = MagicMock(spec = StorageClient)
    storage_client_mock.source.return_value = "s3"
    storage_client_mock.upload_object.return_value = StoredObjectUploadResult(public_url = "https://example.com/file.jpg", path = "public/file.jpg")
    object_mock = MagicMock(spec = ObjectToStore)
    object_mock.key.return_value = "public/file.jpg"
    object_mock.data = b"data"
    object_mock.content_type = "image/jpeg"
    instance = StorageService(date_provider_mock, book_dal_mock, stored_object_dal_mock)

    with pytest.raises(Exception) as exc_info:
      instance.store_object(session_mock, storage_client_mock, object_mock)
    assert str(exc_info.value) == "dal error"

  def test_delete_stored_objects_success(self):
    now = MagicMock()
    date_provider_mock = MagicMock(spec = DateProvider)
    date_provider_mock.now.return_value = now
    book_dal_mock = MagicMock(spec = BookDAL)
    stored_object_dal_mock = MagicMock(spec = StoredObjectDAL)
    stored_object_id = uuid4()
    stored_object = StoredObject.model_construct(id = stored_object_id, source = "s3", key = "public/file.jpg", created_at = now, updated_at = now)
    stored_object_dal_mock.get_stored_objects.return_value = [stored_object]
    session_mock = MagicMock(spec = Session)
    storage_client_mock = MagicMock(spec = StorageClient)
    instance = StorageService(date_provider_mock, book_dal_mock, stored_object_dal_mock)

    instance.delete_stored_objects(session_mock, storage_client_mock, [stored_object_id])

    stored_object_dal_mock.get_stored_objects.assert_called_once_with(session_mock, 1, 0, ids = [stored_object_id])
    date_provider_mock.now.assert_called_once()
    stored_object_dal_mock.soft_delete_stored_objects.assert_called_once_with(session_mock, [stored_object_id], now)
    storage_client_mock.delete_objects.assert_called_once_with(["public/file.jpg"])

  def test_delete_stored_objects_no_objects(self):
    date_provider_mock = MagicMock(spec = DateProvider)
    book_dal_mock = MagicMock(spec = BookDAL)
    stored_object_dal_mock = MagicMock(spec = StoredObjectDAL)
    stored_object_dal_mock.get_stored_objects.return_value = []
    session_mock = MagicMock(spec = Session)
    storage_client_mock = MagicMock(spec = StorageClient)
    instance = StorageService(date_provider_mock, book_dal_mock, stored_object_dal_mock)

    instance.delete_stored_objects(session_mock, storage_client_mock, [uuid4()])

    stored_object_dal_mock.get_stored_objects.assert_called_once()
    date_provider_mock.now.assert_not_called()
    stored_object_dal_mock.soft_delete_stored_objects.assert_not_called()
    storage_client_mock.delete_objects.assert_not_called()

  def test_delete_stored_objects_dal_fail(self):
    date_provider_mock = MagicMock(spec = DateProvider)
    book_dal_mock = MagicMock(spec = BookDAL)
    stored_object_dal_mock = MagicMock(spec = StoredObjectDAL)
    stored_object_dal_mock.get_stored_objects.side_effect = Exception("dal error")
    session_mock = MagicMock(spec = Session)
    storage_client_mock = MagicMock(spec = StorageClient)
    instance = StorageService(date_provider_mock, book_dal_mock, stored_object_dal_mock)

    with pytest.raises(Exception) as exc_info:
      instance.delete_stored_objects(session_mock, storage_client_mock, [uuid4()])
    assert str(exc_info.value) == "dal error"
    storage_client_mock.delete_objects.assert_not_called()

  def test_delete_stored_objects_storage_delete_fail(self):
    now = MagicMock()
    date_provider_mock = MagicMock(spec = DateProvider)
    date_provider_mock.now.return_value = now
    book_dal_mock = MagicMock(spec = BookDAL)
    stored_object_dal_mock = MagicMock(spec = StoredObjectDAL)
    stored_object = StoredObject.model_construct(id = uuid4(), source = "s3", key = "public/file.jpg", created_at = now, updated_at = now)
    stored_object_dal_mock.get_stored_objects.return_value = [stored_object]
    storage_client_mock = MagicMock(spec = StorageClient)
    storage_client_mock.delete_objects.side_effect = StorageClientError("s3 error")
    session_mock = MagicMock(spec = Session)
    instance = StorageService(date_provider_mock, book_dal_mock, stored_object_dal_mock)

    with pytest.raises(StorageClientError) as exc_info:
      instance.delete_stored_objects(session_mock, storage_client_mock, [stored_object.id])
    assert str(exc_info.value) == "s3 error"
    stored_object_dal_mock.soft_delete_stored_objects.assert_called_once()
    storage_client_mock.delete_objects.assert_called_once()
