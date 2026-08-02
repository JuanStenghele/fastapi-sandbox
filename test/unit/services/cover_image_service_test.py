import pytest


from unittest.mock import MagicMock
from uuid import uuid4
from sqlmodel import Session
from clients.storage_client import StorageClient, StorageClientError
from dal.book_dal import BookDAL
from objects.error import ValidationError
from objects.image import RawImage
from objects.stored_object_record import StoredObject as StoredObjectRecord
from services.cover_image_service import CoverImageService, COVER_IMAGES_PATH
from services.date_provider import DateProvider
from services.storage_service import StorageService
from validators.cover_image_validator import CoverImageValidator


class TestCoverImageService():
  def test_create_success(self):
    now = MagicMock()
    storage_client_mock = MagicMock(spec = StorageClient)
    cover_image_validator_mock = MagicMock(spec = CoverImageValidator)
    session_mock = MagicMock(spec = Session)
    file_mock = MagicMock()
    file_mock.read.return_value = b"data"
    book_id = uuid4()
    image = RawImage.model_construct(file = file_mock, content_type = "image/jpeg")
    date_provider_mock = MagicMock(spec = DateProvider)
    date_provider_mock.now.return_value = now
    storage_service_mock = MagicMock(spec = StorageService)
    stored_object_id = uuid4()
    stored_object = StoredObjectRecord.model_construct(id = stored_object_id, public_url = "https://example.com/cover.jpg")
    storage_service_mock.store_object.return_value = stored_object
    book_dal_mock = MagicMock(spec = BookDAL)
    instance = CoverImageService(storage_client_mock, cover_image_validator_mock, date_provider_mock, storage_service_mock, book_dal_mock)

    result = instance.create_book_cover(session_mock, book_id, image)

    cover_image_validator_mock.validate_upsert.assert_called_once_with(session_mock, book_id, image)
    storage_service_mock.store_object.assert_called_once()
    book_dal_mock.update_book_cover_stored_object_ids.assert_called_once_with(session_mock, [book_id], stored_object_id, now)
    assert result.book_id == book_id
    assert result.url == "https://example.com/cover.jpg"

  def test_create_validation_fail(self):
    storage_client_mock = MagicMock(spec = StorageClient)
    cover_image_validator_mock = MagicMock(spec = CoverImageValidator)
    cover_image_validator_mock.validate_upsert.side_effect = ValidationError("INVALID_IMAGE")
    session_mock = MagicMock(spec = Session)
    image = RawImage.model_construct(file = MagicMock(), content_type = "image/bmp")
    date_provider_mock = MagicMock(spec = DateProvider)
    storage_service_mock = MagicMock(spec = StorageService)
    book_dal_mock = MagicMock(spec = BookDAL)
    instance = CoverImageService(storage_client_mock, cover_image_validator_mock, date_provider_mock, storage_service_mock, book_dal_mock)

    with pytest.raises(ValidationError) as exc_info:
      instance.create_book_cover(session_mock, uuid4(), image)
    assert exc_info.value.detail == "INVALID_IMAGE"
    storage_service_mock.store_object.assert_not_called()
    book_dal_mock.update_book_cover_stored_object_ids.assert_not_called()

  def test_create_storage_service_fail(self):
    storage_client_mock = MagicMock(spec = StorageClient)
    cover_image_validator_mock = MagicMock(spec = CoverImageValidator)
    session_mock = MagicMock(spec = Session)
    file_mock = MagicMock()
    file_mock.read.return_value = b"data"
    image = RawImage.model_construct(file = file_mock, content_type = "image/jpeg")
    date_provider_mock = MagicMock(spec = DateProvider)
    storage_service_mock = MagicMock(spec = StorageService)
    storage_service_mock.store_object.side_effect = StorageClientError("upload failed")
    book_dal_mock = MagicMock(spec = BookDAL)
    instance = CoverImageService(storage_client_mock, cover_image_validator_mock, date_provider_mock, storage_service_mock, book_dal_mock)

    with pytest.raises(StorageClientError) as exc_info:
      instance.create_book_cover(session_mock, uuid4(), image)
    assert str(exc_info.value) == "upload failed"
    book_dal_mock.update_book_cover_stored_object_ids.assert_not_called()

  def test_delete_success(self):
    now = MagicMock()
    storage_client_mock = MagicMock(spec = StorageClient)
    cover_image_validator_mock = MagicMock(spec = CoverImageValidator)
    session_mock = MagicMock(spec = Session)
    book_id = uuid4()
    date_provider_mock = MagicMock(spec = DateProvider)
    date_provider_mock.now.return_value = now
    storage_service_mock = MagicMock(spec = StorageService)
    book_dal_mock = MagicMock(spec = BookDAL)
    instance = CoverImageService(storage_client_mock, cover_image_validator_mock, date_provider_mock, storage_service_mock, book_dal_mock)

    instance.delete_book_covers(session_mock, [book_id])

    cover_image_validator_mock.validate_deletion.assert_called_once_with(session_mock, [book_id])
    storage_service_mock.delete_stored_objects.assert_called_once_with(session_mock, storage_client_mock, [book_id])
    book_dal_mock.update_book_cover_stored_object_ids.assert_called_once_with(session_mock, [book_id], None, now)

  def test_delete_validation_fail(self):
    storage_client_mock = MagicMock(spec = StorageClient)
    cover_image_validator_mock = MagicMock(spec = CoverImageValidator)
    cover_image_validator_mock.validate_deletion.side_effect = ValidationError("BOOKS_NOT_FOUND")
    session_mock = MagicMock(spec = Session)
    date_provider_mock = MagicMock(spec = DateProvider)
    storage_service_mock = MagicMock(spec = StorageService)
    book_dal_mock = MagicMock(spec = BookDAL)
    instance = CoverImageService(storage_client_mock, cover_image_validator_mock, date_provider_mock, storage_service_mock, book_dal_mock)

    with pytest.raises(ValidationError) as exc_info:
      instance.delete_book_covers(session_mock, [uuid4()])
    assert exc_info.value.detail == "BOOKS_NOT_FOUND"
    storage_service_mock.delete_stored_objects.assert_not_called()
    book_dal_mock.update_book_cover_stored_object_ids.assert_not_called()

  def test_delete_storage_service_fail(self):
    storage_client_mock = MagicMock(spec = StorageClient)
    cover_image_validator_mock = MagicMock(spec = CoverImageValidator)
    storage_service_mock = MagicMock(spec = StorageService)
    storage_service_mock.delete_stored_objects.side_effect = StorageClientError("s3 error")
    session_mock = MagicMock(spec = Session)
    book_id = uuid4()
    date_provider_mock = MagicMock(spec = DateProvider)
    book_dal_mock = MagicMock(spec = BookDAL)
    instance = CoverImageService(storage_client_mock, cover_image_validator_mock, date_provider_mock, storage_service_mock, book_dal_mock)

    with pytest.raises(StorageClientError) as exc_info:
      instance.delete_book_covers(session_mock, [book_id])
    assert str(exc_info.value) == "s3 error"
    cover_image_validator_mock.validate_deletion.assert_called_once_with(session_mock, [book_id])
    book_dal_mock.update_book_cover_stored_object_ids.assert_not_called()

  def test_update_book_cover_success(self):
    now = MagicMock()
    storage_client_mock = MagicMock(spec = StorageClient)
    cover_image_validator_mock = MagicMock(spec = CoverImageValidator)
    session_mock = MagicMock(spec = Session)
    file_mock = MagicMock()
    file_mock.read.return_value = b"data"
    book_id = uuid4()
    image = RawImage.model_construct(file = file_mock, content_type = "image/jpeg")
    date_provider_mock = MagicMock(spec = DateProvider)
    date_provider_mock.now.return_value = now
    storage_service_mock = MagicMock(spec = StorageService)
    stored_object_id = uuid4()
    stored_object = StoredObjectRecord.model_construct(id = stored_object_id, public_url = "https://example.com/cover.jpg")
    storage_service_mock.store_object.return_value = stored_object
    book_dal_mock = MagicMock(spec = BookDAL)
    instance = CoverImageService(storage_client_mock, cover_image_validator_mock, date_provider_mock, storage_service_mock, book_dal_mock)

    result = instance.update_book_cover(session_mock, book_id, image)

    storage_service_mock.delete_stored_objects.assert_called_once_with(session_mock, storage_client_mock, [book_id])
    storage_service_mock.store_object.assert_called_once()
    book_dal_mock.update_book_cover_stored_object_ids.assert_called_with(session_mock, [book_id], stored_object_id, now)
    assert result.book_id == book_id
    assert result.url == "https://example.com/cover.jpg"

  def test_update_book_cover_delete_fail(self):
    storage_client_mock = MagicMock(spec = StorageClient)
    cover_image_validator_mock = MagicMock(spec = CoverImageValidator)
    storage_service_mock = MagicMock(spec = StorageService)
    storage_service_mock.delete_stored_objects.side_effect = StorageClientError("s3 error")
    session_mock = MagicMock(spec = Session)
    file_mock = MagicMock()
    file_mock.read.return_value = b"data"
    image = RawImage.model_construct(file = file_mock, content_type = "image/jpeg")
    date_provider_mock = MagicMock(spec = DateProvider)
    book_dal_mock = MagicMock(spec = BookDAL)
    instance = CoverImageService(storage_client_mock, cover_image_validator_mock, date_provider_mock, storage_service_mock, book_dal_mock)

    with pytest.raises(StorageClientError) as exc_info:
      instance.update_book_cover(session_mock, uuid4(), image)
    assert str(exc_info.value) == "s3 error"
    storage_service_mock.store_object.assert_not_called()
