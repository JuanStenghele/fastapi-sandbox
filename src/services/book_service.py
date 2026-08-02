import uuid


from math import ceil
from uuid import UUID
from constants import DEFAULT_PAGE_SIZES
from dal.book_dal import BookDAL
from objects.book import Book, GetBooksResult, GetBooksPaginatedResult
from objects.book_creation import BookCreationRequest
from objects.book_update import BookUpdateRequest
from objects.error import ValidationError
from services.cover_image_service import CoverImageService
from services.date_provider import DateProvider
from sqlmodel import Session
from validators.book_validator import BookValidator


class BookService():
  def __init__(self, book_dal: BookDAL, cover_image_service: CoverImageService, book_validator: BookValidator, date_provider: DateProvider) -> None:
    self.book_dal: BookDAL = book_dal
    self.cover_image_service = cover_image_service
    self.book_validator: BookValidator = book_validator
    self.date_provider = date_provider

  def create_book(self, session: Session, request: BookCreationRequest) -> Book:
    self.book_validator.validate_creation(session, request)
    now = self.date_provider.now()
    book = Book(
      id = uuid.uuid4(),
      title = request.title,
      author_id = request.author_id,
      description = request.description,
      isbn = request.isbn,
      publication_date = request.publication_date,
      created_at = now,
      updated_at = now
    )
    self.book_dal.create_book(session, book)
    if request.cover_image:
      book.cover_image = self.cover_image_service.create_book_cover(session, book.id, request.cover_image)
    return book

  def get_book(self, session: Session, id: UUID) -> Book | None:
    return self.book_dal.get_book(session, id)

  def get_books(self, session: Session, search_term: str | None, limit: int, offset: int) -> GetBooksResult:
    if offset < 0:
      raise ValidationError(detail = "INVALID_OFFSET")
    total_books = self.book_dal.count_books(session, search_term)
    books = self.book_dal.get_books(session, limit, offset, search_term = search_term)
    return GetBooksResult(books = books, total_books = total_books)

  def get_books_paginated(self, session: Session, search_term: str | None, page: int, page_size: int) -> GetBooksPaginatedResult:
    if page_size not in DEFAULT_PAGE_SIZES:
      raise ValidationError(detail = "INVALID_PAGE_SIZE")
    if page < 1:
      raise ValidationError(detail = "INVALID_PAGE")
    offset = (page - 1) * page_size
    result = self.get_books(session, search_term, page_size, offset)
    return GetBooksPaginatedResult(
      books = result.books,
      total_books = result.total_books,
      total_pages = ceil(result.total_books / page_size),
      current_page = page,
      page_size = page_size
    )

  def update_book(self, session: Session, id: UUID, request: BookUpdateRequest) -> Book | None:
    self.book_validator.validate_update(session, request)
    now = self.date_provider.now()
    return self.book_dal.update_book(session, id, request.title, request.author_id, request.description, request.isbn, request.publication_date, now)

  def delete_books(self, session: Session, book_ids: list) -> None:
    self.book_validator.validate_deletion(session, book_ids)
    self.cover_image_service.delete_book_covers(session, book_ids)
    now = self.date_provider.now()
    self.book_dal.soft_delete_books(session, book_ids, now)
