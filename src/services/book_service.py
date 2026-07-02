import uuid


from math import ceil
from datetime import datetime, timezone
from uuid import UUID
from constants import BOOKS_PAGE_SIZES
from dal.book_dal import BookDAL
from objects.book import Book, GetBooksResult, GetBooksPaginatedResult
from objects.book_creation import BookCreationRequest
from objects.error import ValidationError
from services.cover_image_service import CoverImageService
from sqlmodel import Session
from validators.book_validator import BookValidator


class BookService():
  def __init__(self, book_dal: BookDAL, cover_image_service: CoverImageService, book_validator: BookValidator) -> None:
    self.book_dal: BookDAL = book_dal
    self.cover_image_service = cover_image_service
    self.book_validator: BookValidator = book_validator

  def create_book(self, session: Session, request: BookCreationRequest) -> Book:
    self.book_validator.validate_creation(session, request)
    now = datetime.now(timezone.utc)
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
      book.cover_image = self.cover_image_service.create(session, book.id, request.cover_image)
    return book

  def get_book(self, session: Session, id: UUID) -> Book | None:
    return self.book_dal.get_book(session, id)

  def get_books(self, session: Session, search_term: str | None, limit: int, offset: int) -> GetBooksResult:
    if offset < 0:
      raise ValidationError(detail = "INVALID_OFFSET")
    total_books = self.book_dal.count_books(session, search_term)
    books = self.book_dal.get_books(session, search_term, limit, offset)
    return GetBooksResult(books = books, total_books = total_books)

  def get_books_paginated(self, session: Session, search_term: str | None, page: int, page_size: int) -> GetBooksPaginatedResult:
    if page_size not in BOOKS_PAGE_SIZES:
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
