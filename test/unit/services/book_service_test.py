import pytest


from datetime import datetime, timezone
from unittest.mock import MagicMock
from uuid import uuid4
from services.book_service import BookService
from services.cover_image_service import CoverImageService
from dal.book_dal import BookDAL
from objects.book import Book, GetBooksResult, GetBooksPaginatedResult
from objects.book_creation import BookCreationRequest
from objects.error import ValidationError
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
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock)
    request = BookCreationRequest(title = book_title, author_id = author_id)
    result = instance.create_book(session_mock, request)
    assert result.id is not None
    assert result.title == book_title
    assert result.author_id == author_id
    book_validator_mock.validate_creation.assert_called_once()
    cover_image_service_mock.create.assert_not_called()

  def test_create_book_success_with_cover(self):
    book_title = 'Harry Potter'
    author_id = uuid4()
    book_dal_mock = MagicMock(spec = BookDAL)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    session_mock = MagicMock(spec = Session)
    raw_image = RawImage.model_construct(file = MagicMock(), content_type = "image/jpeg")
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock)
    request = BookCreationRequest(title = book_title, author_id = author_id, cover_image = raw_image)
    instance.create_book(session_mock, request)
    cover_image_service_mock.create.assert_called_once()
    call_args = cover_image_service_mock.create.call_args[0]
    assert call_args[0] == session_mock
    assert call_args[2] == raw_image

  def test_create_book_fail(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    book_dal_mock.create_book.side_effect = Exception('error')
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    session_mock = MagicMock(spec = Session)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock)
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
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock)
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
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock)
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
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock)
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
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock)
    result = instance.get_books(session_mock, None, 10, 0)
    assert result.books == [book_1, book_2]
    assert result.total_books == 2
    book_dal_mock.count_books.assert_called_once()
    book_dal_mock.get_books.assert_called_once_with(session_mock, None, 10, 0)

  def test_get_books_success_with_search_term(self):
    now = datetime.now(timezone.utc)
    book_dal_mock = MagicMock(spec = BookDAL)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    session_mock = MagicMock(spec = Session)
    book = Book(id = uuid4(), title = 'Harry Potter', author_id = uuid4(), created_at = now, updated_at = now)
    book_dal_mock.count_books.return_value = 1
    book_dal_mock.get_books.return_value = [book]
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock)
    result = instance.get_books(session_mock, 'Harry', 10, 0)
    assert len(result.books) == 1
    assert result.books[0].title == 'Harry Potter'
    assert result.total_books == 1
    book_dal_mock.get_books.assert_called_once_with(session_mock, 'Harry', 10, 0)

  def test_get_books_empty_results(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    session_mock = MagicMock(spec = Session)
    book_dal_mock.count_books.return_value = 0
    book_dal_mock.get_books.return_value = []
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock)
    result = instance.get_books(session_mock, None, 10, 0)
    assert result.books == []
    assert result.total_books == 0

  def test_get_books_invalid_offset(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    session_mock = MagicMock(spec = Session)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock)
    with pytest.raises(ValidationError) as exc_info:
      instance.get_books(session_mock, None, 10, -1)
    assert exc_info.value.detail == 'INVALID_OFFSET'

  def test_get_books_fail(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    book_dal_mock.count_books.side_effect = Exception('error')
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    session_mock = MagicMock(spec = Session)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock)
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
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock)
    result = instance.get_books_paginated(session_mock, None, 1, 10)
    assert result.books == [book_1, book_2]
    assert result.total_books == 5
    assert result.total_pages == 1
    assert result.current_page == 1
    assert result.page_size == 10
    book_dal_mock.count_books.assert_called_once()
    book_dal_mock.get_books.assert_called_once_with(session_mock, None, 10, 0)

  def test_get_books_paginated_invalid_page_size(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    session_mock = MagicMock(spec = Session)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock)
    with pytest.raises(ValidationError) as exc_info:
      instance.get_books_paginated(session_mock, None, 1, 7)
    assert exc_info.value.detail == 'INVALID_PAGE_SIZE'

  def test_get_books_paginated_invalid_page(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    session_mock = MagicMock(spec = Session)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock)
    with pytest.raises(ValidationError) as exc_info:
      instance.get_books_paginated(session_mock, None, 0, 10)
    assert exc_info.value.detail == 'INVALID_PAGE'

  def test_get_books_paginated_fail(self):
    book_dal_mock = MagicMock(spec = BookDAL)
    book_dal_mock.count_books.side_effect = Exception('error')
    cover_image_service_mock = MagicMock(spec = CoverImageService)
    book_validator_mock = MagicMock(spec = BookValidator)
    session_mock = MagicMock(spec = Session)
    instance = BookService(book_dal_mock, cover_image_service_mock, book_validator_mock)
    with pytest.raises(Exception) as exc_info:
      instance.get_books_paginated(session_mock, None, 1, 10)
    assert str(exc_info.value) == 'error'
