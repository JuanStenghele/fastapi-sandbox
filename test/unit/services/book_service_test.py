import pytest


from datetime import datetime, timezone
from unittest.mock import MagicMock, call
from uuid import uuid4
from services.book_service import BookService
from services.date_provider import DateProvider
from services.cover_image_service import CoverImageService
from dal.book_dal import BookDAL
from objects.book import Book, GetBooksResult, GetBooksPaginatedResult
from objects.book_creation import BookCreationRequest
from objects.book_update import BookUpdateRequest
from objects.error import ValidationError
from objects.image import RawImage
from objects.image import RawImage
from validators.book_validator import BookValidator
from sqlmodel import Session


class TestBookService():
  def test_create_book_success(self):
    book_title = 'Harry Potter'
    author_id = uuid4()
    book_dal_mock = MagicMock(spec = BookDAL)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    session_mock = MagicMock(spec = Session)
    date_provider_mock = MagicMock(spec = DateProvider)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock, date_provider_mock)
    request = BookCreationRequest(title = book_title, author_id = author_id)
    result = instance.create_book(session_mock, request)
    assert result.id is not None
    assert result.title == book_title
    assert result.author_id == author_id
    book_validator_mock.validate_creation.assert_called_once()
    cover_image_service_mock.create_book_cover.assert_not_called()

  def test_create_book_success_with_cover(self):
    book_title = 'Harry Potter'
    author_id = uuid4()
    book_dal_mock = MagicMock(spec = BookDAL)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    session_mock = MagicMock(spec = Session)
    raw_image = RawImage.model_construct(file = MagicMock(), content_type = "image/jpeg")
    date_provider_mock = MagicMock(spec = DateProvider)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock, date_provider_mock)
    request = BookCreationRequest(title = book_title, author_id = author_id, cover_image = raw_image)
    instance.create_book(session_mock, request)
    cover_image_service_mock.create_book_cover.assert_called_once()
    call_args = cover_image_service_mock.create_book_cover.call_args[0]
    assert call_args[0] == session_mock
    assert call_args[2] == raw_image

  def test_create_book_fail(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    book_dal_mock.create_book.side_effect = Exception('error')
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    session_mock = MagicMock(spec = Session)
    date_provider_mock = MagicMock(spec = DateProvider)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock, date_provider_mock)
    request = BookCreationRequest(title = 'Harry Potter', author_id = uuid4())
    with pytest.raises(Exception) as exc_info:
      instance.create_book(session_mock, request)
    assert str(exc_info.value) == 'error'

  def test_create_book_validation_fail(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    book_validator_mock.validate_creation.side_effect = Exception('validation error')
    session_mock = MagicMock(spec = Session)
    date_provider_mock = MagicMock(spec = DateProvider)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock, date_provider_mock)
    request = BookCreationRequest(title = 'Harry Potter', author_id = uuid4())
    with pytest.raises(Exception) as exc_info:
      instance.create_book(session_mock, request)
    assert str(exc_info.value) == 'validation error'
    book_dal_mock.create_book.assert_not_called()

  def test_get_book_success(self):
    now = datetime.now(timezone.utc)
    book_id = uuid4()
    book_title = 'Harry Potter'
    book_dal_mock = MagicMock(spec = BookDAL)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    book_dal_mock.get_book.return_value = Book(id = book_id, title = book_title, author_id = uuid4(), created_at = now, updated_at = now)
    session_mock = MagicMock(spec = Session)
    date_provider_mock = MagicMock(spec = DateProvider)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock, date_provider_mock)
    result = instance.get_book(session_mock, book_id)
    assert result is not None
    assert result.id == book_id
    assert result.title == book_title

  def test_get_book_fail(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    book_dal_mock.get_book.side_effect = Exception('error')
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    session_mock = MagicMock(spec = Session)
    date_provider_mock = MagicMock(spec = DateProvider)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock, date_provider_mock)
    with pytest.raises(Exception) as exc_info:
      instance.get_book(session_mock, uuid4())
    assert str(exc_info.value) == 'error'

  def test_get_books_success(self):
    now = datetime.now(timezone.utc)
    book_dal_mock = MagicMock(spec = BookDAL)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    session_mock = MagicMock(spec = Session)
    book_1 = Book(id = uuid4(), title = 'Harry Potter', author_id = uuid4(), created_at = now, updated_at = now)
    book_2 = Book(id = uuid4(), title = 'The Lord of the Rings', author_id = uuid4(), created_at = now, updated_at = now)
    book_dal_mock.count_books.return_value = 2
    book_dal_mock.get_books.return_value = [book_1, book_2]
    date_provider_mock = MagicMock(spec = DateProvider)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock, date_provider_mock)
    result = instance.get_books(session_mock, None, 10, 0)
    assert result.books == [book_1, book_2]
    assert result.total_books == 2
    book_dal_mock.count_books.assert_called_once()
    book_dal_mock.get_books.assert_called_once_with(session_mock, 10, 0, search_term = None)

  def test_get_books_success_with_search_term(self):
    now = datetime.now(timezone.utc)
    book_dal_mock = MagicMock(spec = BookDAL)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    session_mock = MagicMock(spec = Session)
    book = Book(id = uuid4(), title = 'Harry Potter', author_id = uuid4(), created_at = now, updated_at = now)
    book_dal_mock.count_books.return_value = 1
    book_dal_mock.get_books.return_value = [book]
    date_provider_mock = MagicMock(spec = DateProvider)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock, date_provider_mock)
    result = instance.get_books(session_mock, 'Harry', 10, 0)
    assert len(result.books) == 1
    assert result.books[0].title == 'Harry Potter'
    assert result.total_books == 1
    book_dal_mock.get_books.assert_called_once_with(session_mock, 10, 0, search_term = 'Harry')

  def test_get_books_empty_results(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    session_mock = MagicMock(spec = Session)
    book_dal_mock.count_books.return_value = 0
    book_dal_mock.get_books.return_value = []
    date_provider_mock = MagicMock(spec = DateProvider)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock, date_provider_mock)
    result = instance.get_books(session_mock, None, 10, 0)
    assert result.books == []
    assert result.total_books == 0

  def test_get_books_invalid_offset(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    session_mock = MagicMock(spec = Session)
    date_provider_mock = MagicMock(spec = DateProvider)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock, date_provider_mock)
    with pytest.raises(ValidationError) as exc_info:
      instance.get_books(session_mock, None, 10, -1)
    assert exc_info.value.detail == 'INVALID_OFFSET'

  def test_get_books_fail(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    book_dal_mock.count_books.side_effect = Exception('error')
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    session_mock = MagicMock(spec = Session)
    date_provider_mock = MagicMock(spec = DateProvider)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock, date_provider_mock)
    with pytest.raises(Exception) as exc_info:
      instance.get_books(session_mock, None, 10, 0)
    assert str(exc_info.value) == 'error'

  def test_get_books_paginated_success(self):
    now = datetime.now(timezone.utc)
    book_dal_mock = MagicMock(spec = BookDAL)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    session_mock = MagicMock(spec = Session)
    book_1 = Book(id = uuid4(), title = 'Harry Potter', author_id = uuid4(), created_at = now, updated_at = now)
    book_2 = Book(id = uuid4(), title = 'The Lord of the Rings', author_id = uuid4(), created_at = now, updated_at = now)
    book_dal_mock.count_books.return_value = 5
    book_dal_mock.get_books.return_value = [book_1, book_2]
    date_provider_mock = MagicMock(spec = DateProvider)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock, date_provider_mock)
    result = instance.get_books_paginated(session_mock, None, 1, 10)
    assert result.books == [book_1, book_2]
    assert result.total_books == 5
    assert result.total_pages == 1
    assert result.current_page == 1
    assert result.page_size == 10
    book_dal_mock.count_books.assert_called_once()
    book_dal_mock.get_books.assert_called_once_with(session_mock, 10, 0, search_term = None)

  def test_get_books_paginated_invalid_page_size(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    session_mock = MagicMock(spec = Session)
    date_provider_mock = MagicMock(spec = DateProvider)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock, date_provider_mock)
    with pytest.raises(ValidationError) as exc_info:
      instance.get_books_paginated(session_mock, None, 1, 7)
    assert exc_info.value.detail == 'INVALID_PAGE_SIZE'

  def test_get_books_paginated_invalid_page(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    session_mock = MagicMock(spec = Session)
    date_provider_mock = MagicMock(spec = DateProvider)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock, date_provider_mock)
    with pytest.raises(ValidationError) as exc_info:
      instance.get_books_paginated(session_mock, None, 0, 10)
    assert exc_info.value.detail == 'INVALID_PAGE'

  def test_get_books_paginated_fail(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    book_dal_mock.count_books.side_effect = Exception('error')
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    session_mock = MagicMock(spec = Session)
    date_provider_mock = MagicMock(spec = DateProvider)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock, date_provider_mock)
    with pytest.raises(Exception) as exc_info:
      instance.get_books_paginated(session_mock, None, 1, 10)
    assert str(exc_info.value) == 'error'

  def test_delete_books_success(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    session_mock = MagicMock(spec = Session)
    book_ids = [uuid4(), uuid4()]
    date_provider_mock = MagicMock(spec = DateProvider)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock, date_provider_mock)
    instance.delete_books(session_mock, book_ids)
    book_validator_mock.validate_deletion.assert_called_once_with(session_mock, book_ids)
    cover_image_service_mock.delete_book_covers.assert_called_once_with(session_mock, book_ids)
    assert book_dal_mock.soft_delete_books.call_count == 1

  def test_delete_books_validation_error(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    book_validator_mock.validate_deletion.side_effect = ValidationError(detail = "BOOKS_NOT_FOUND")
    session_mock = MagicMock(spec = Session)
    book_ids = [uuid4()]
    date_provider_mock = MagicMock(spec = DateProvider)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock, date_provider_mock)
    with pytest.raises(ValidationError) as exc_info:
      instance.delete_books(session_mock, book_ids)
    assert exc_info.value.detail == 'BOOKS_NOT_FOUND'
    assert book_dal_mock.soft_delete_books.call_count == 0

  def test_delete_books_fail(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    book_dal_mock.soft_delete_books.side_effect = Exception('error')
    session_mock = MagicMock(spec = Session)
    book_ids = [uuid4()]
    date_provider_mock = MagicMock(spec = DateProvider)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock, date_provider_mock)
    with pytest.raises(Exception) as exc_info:
      instance.delete_books(session_mock, book_ids)
    assert str(exc_info.value) == 'error'

  def test_update_book_success(self):
    now = datetime.now(timezone.utc)
    book_id = uuid4()
    author_id = uuid4()
    book_dal_mock = MagicMock(spec = BookDAL)
    expected_book = Book(id = book_id, title = 'New Title', author_id = author_id, created_at = now, updated_at = now)
    book_dal_mock.update_book.return_value = expected_book
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    session_mock = MagicMock(spec = Session)
    request = BookUpdateRequest(title = 'New Title')
    date_provider_mock = MagicMock(spec = DateProvider)
    date_provider_mock.now.return_value = now
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock, date_provider_mock)

    result = instance.update_book(session_mock, book_id, request)
    assert result == expected_book
    book_validator_mock.validate_update.assert_called_once()
    book_dal_mock.update_book.assert_called_once()

  def test_update_book_validation_error(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    book_validator_mock.validate_update.side_effect = ValidationError(detail = "AUTHOR_NOT_FOUND")
    session_mock = MagicMock(spec = Session)
    request = BookUpdateRequest(author_id = uuid4())
    date_provider_mock = MagicMock(spec = DateProvider)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock, date_provider_mock)
    with pytest.raises(ValidationError) as exc_info:
      instance.update_book(session_mock, uuid4(), request)
    assert exc_info.value.detail == 'AUTHOR_NOT_FOUND'

  def test_update_book_not_found(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    book_dal_mock.update_book.return_value = None
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    session_mock = MagicMock(spec = Session)
    request = BookUpdateRequest(title = 'New Title')
    date_provider_mock = MagicMock(spec = DateProvider)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock, date_provider_mock)
    result = instance.update_book(session_mock, uuid4(), request)
    assert result is None

  def test_update_book_fail(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    book_dal_mock.update_book.side_effect = Exception('error')
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    session_mock = MagicMock(spec = Session)
    request = BookUpdateRequest(title = 'New Title')
    date_provider_mock = MagicMock(spec = DateProvider)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock, date_provider_mock)
    with pytest.raises(Exception) as exc_info:
      instance.update_book(session_mock, uuid4(), request)
    assert str(exc_info.value) == 'error'
