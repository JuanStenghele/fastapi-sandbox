import pytest


from unittest.mock import MagicMock
from uuid import uuid4
from sqlmodel import Session
from clients.storage_client import StorageClient
from dal.book_cover_dal import BookCoverDAL
from objects.error import ValidationError
from objects.image import RawImage
from services.cover_image_service import CoverImageService, COVER_IMAGES_PATH
from validators.cover_image_validator import CoverImageValidator


class TestCoverImageService():
  def test_create_success(self):
    storage_client_mock = MagicMock(spec = StorageClient)
    storage_client_mock.source.return_value = "s3"
    storage_client_mock.upload_user_content.return_value = "https://example.com/cover.jpg"
    book_cover_dal_mock = MagicMock(spec = BookCoverDAL)
    cover_image_validator_mock = MagicMock(spec = CoverImageValidator)
    session_mock = MagicMock(spec = Session)
    file_mock = MagicMock()
    file_mock.read.return_value = b"data"
    book_id = uuid4()
    image = RawImage.model_construct(file = file_mock, content_type = "image/jpeg")
    instance = CoverImageService(storage_client_mock, book_cover_dal_mock, cover_image_validator_mock)
    result = instance.create(session_mock, book_id, image)
    cover_image_validator_mock.validate_creation.assert_called_once_with(image)
    storage_client_mock.upload_user_content.assert_called_once_with(
      f"{COVER_IMAGES_PATH}/{book_id}", b"data", "image/jpeg"
    )
    book_cover_dal_mock.create_book_cover.assert_called_once()
    assert result.book_id == book_id
    assert result.url == "https://example.com/cover.jpg"

  def test_create_validation_fail(self):
    storage_client_mock = MagicMock(spec = StorageClient)
    book_cover_dal_mock = MagicMock(spec = BookCoverDAL)
    cover_image_validator_mock = MagicMock(spec = CoverImageValidator)
    cover_image_validator_mock.validate_creation.side_effect = ValidationError("INVALID_IMAGE")
    session_mock = MagicMock(spec = Session)
    image = RawImage.model_construct(file = MagicMock(), content_type = "image/bmp")
    instance = CoverImageService(storage_client_mock, book_cover_dal_mock, cover_image_validator_mock)
    with pytest.raises(ValidationError) as exc_info:
      instance.create(session_mock, uuid4(), image)
    assert exc_info.value.detail == "INVALID_IMAGE"
    storage_client_mock.upload_user_content.assert_not_called()
    book_cover_dal_mock.create_book_cover.assert_not_called()

  def test_create_upload_fail(self):
    storage_client_mock = MagicMock(spec = StorageClient)
    storage_client_mock.upload_user_content.side_effect = Exception("upload failed")
    book_cover_dal_mock = MagicMock(spec = BookCoverDAL)
    cover_image_validator_mock = MagicMock(spec = CoverImageValidator)
    session_mock = MagicMock(spec = Session)
    file_mock = MagicMock()
    file_mock.read.return_value = b"data"
    image = RawImage.model_construct(file = file_mock, content_type = "image/jpeg")
    instance = CoverImageService(storage_client_mock, book_cover_dal_mock, cover_image_validator_mock)
    with pytest.raises(Exception) as exc_info:
      instance.create(session_mock, uuid4(), image)
    assert str(exc_info.value) == "upload failed"
    book_cover_dal_mock.create_book_cover.assert_not_called()
