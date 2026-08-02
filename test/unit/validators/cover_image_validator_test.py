import pytest


from unittest.mock import MagicMock
from uuid import uuid4
from constants import COVER_IMAGE_ALLOWED_CONTENT_TYPES, COVER_IMAGE_MAX_SIZE_BYTES
from dal.book_dal import BookDAL
from objects.book import Book
from objects.error import ValidationError
from objects.image import RawImage
from sqlmodel import Session
from validators.cover_image_validator import CoverImageValidator


class TestCoverImageValidator():
  def test_validate_upsert_success(self):
    book_id = uuid4()
    book_dal_mock = MagicMock(spec = BookDAL)
    book_dal_mock.get_book.return_value = MagicMock(spec = Book)
    session_mock = MagicMock(spec = Session)
    image = RawImage.model_construct(file = MagicMock(), content_type = "image/jpeg", size = 1024)
    instance = CoverImageValidator(book_dal_mock)
    instance.validate_upsert(session_mock, book_id, image)

  def test_validate_upsert_book_not_found(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    book_dal_mock.get_book.return_value = None
    session_mock = MagicMock(spec = Session)
    image = RawImage.model_construct(file = MagicMock(), content_type = "image/jpeg", size = 1024)
    instance = CoverImageValidator(book_dal_mock)
    with pytest.raises(ValidationError) as exc_info:
      instance.validate_upsert(session_mock, uuid4(), image)
    assert exc_info.value.detail == "BOOK_NOT_FOUND"

  def test_validate_upsert_invalid_content_type(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    book_dal_mock.get_book.return_value = MagicMock(spec = Book)
    session_mock = MagicMock(spec = Session)
    image = RawImage.model_construct(file = MagicMock(), content_type = "image/bmp", size = 1024)
    instance = CoverImageValidator(book_dal_mock)
    with pytest.raises(ValidationError) as exc_info:
      instance.validate_upsert(session_mock, uuid4(), image)
    assert "image/bmp" in exc_info.value.detail
    assert all(ct in exc_info.value.detail for ct in COVER_IMAGE_ALLOWED_CONTENT_TYPES)

  def test_validate_upsert_exceeds_max_size(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    book_dal_mock.get_book.return_value = MagicMock(spec = Book)
    session_mock = MagicMock(spec = Session)
    image = RawImage.model_construct(file = MagicMock(), content_type = "image/jpeg", size = 20 * 1024 * 1024)
    instance = CoverImageValidator(book_dal_mock)
    with pytest.raises(ValidationError) as exc_info:
      instance.validate_upsert(session_mock, uuid4(), image)
    assert str(COVER_IMAGE_MAX_SIZE_BYTES // (1024 * 1024)) in exc_info.value.detail

  def test_validate_deletion_success(self):
    book_id = uuid4()
    book_dal_mock = MagicMock(spec = BookDAL)
    book_dal_mock.get_books.return_value = [MagicMock(spec = Book, id = book_id)]
    session_mock = MagicMock(spec = Session)
    instance = CoverImageValidator(book_dal_mock)
    instance.validate_deletion(session_mock, [book_id])
    book_dal_mock.get_books.assert_called_once_with(session_mock, 1, 0, ids = [book_id])

  def test_validate_deletion_not_found(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    book_dal_mock.get_books.return_value = []
    session_mock = MagicMock(spec = Session)
    missing_id = uuid4()
    instance = CoverImageValidator(book_dal_mock)
    with pytest.raises(ValidationError) as exc_info:
      instance.validate_deletion(session_mock, [missing_id])
    assert exc_info.value.detail == f"BOOKS_NOT_FOUND: {str(missing_id)}"
