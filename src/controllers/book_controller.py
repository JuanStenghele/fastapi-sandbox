from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide
from sqlmodel import Session
from constants import Tags
from inject import Container
from objects.book_creation import BookCreationRequest
from objects.display import BookCreationHTTPRequest, BookCreationHTTPResponse, BookHTTPResponse, BooksHTTPResponse
from objects.error import ValidationError
from objects.image import RawImage
from services.book_service import BookService
from logging import Logger
from controllers.dependencies import get_session, get_user_auth_claims
from objects.book import Book
from objects.auth import AuthClaims


router = APIRouter()


@router.get("/books/{id}", response_model = BookHTTPResponse, tags = [Tags.BOOKS])
@inject
def get_book(
	id: UUID,
	_: AuthClaims = Depends(get_user_auth_claims),
	book_service: BookService = Depends(Provide[Container.book_service]),
	session: Session = Depends(get_session),
	logger: Logger = Depends(Provide[Container.logger])
):
	try:
		book = book_service.get_book(session, id)
	except Exception as e:
		logger.error(f"Error getting book: {e}")
		raise HTTPException(detail = "UNKNOWN_ERROR", status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)
	if book is None:
		raise HTTPException(detail = "BOOK_NOT_FOUND", status_code = status.HTTP_404_NOT_FOUND)
	return book


@router.get("/books", response_model = BooksHTTPResponse, tags = [Tags.BOOKS])
@inject
def get_books(
	search_term: str | None = None,
	page: int = 1,
	page_size: int = 10,
	_: AuthClaims = Depends(get_user_auth_claims),
	book_service: BookService = Depends(Provide[Container.book_service]),
	session: Session = Depends(get_session),
	logger: Logger = Depends(Provide[Container.logger])
):
	try:
		result = book_service.get_books_paginated(session, search_term, page, page_size)
	except ValidationError as e:
		raise HTTPException(detail = e.detail, status_code = status.HTTP_400_BAD_REQUEST)
	except Exception as e:
		logger.error(f"Error getting books: {e}")
		raise HTTPException(detail = "UNKNOWN_ERROR", status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)
	return BooksHTTPResponse.from_books_result(result)


@router.post("/books", response_model = BookCreationHTTPResponse, tags = [Tags.BOOKS])
@inject
def create_books(
	http_request: BookCreationHTTPRequest = Depends(BookCreationHTTPRequest.as_form),
	_: AuthClaims = Depends(get_user_auth_claims),
	book_service: BookService = Depends(Provide[Container.book_service]),
	session: Session = Depends(get_session),
	logger: Logger = Depends(Provide[Container.logger])
):
	try:
		cover_image = RawImage(file = http_request.cover_image.file, content_type = http_request.cover_image.content_type, size = http_request.cover_image.size) if http_request.cover_image else None
		request = BookCreationRequest(title = http_request.title, author_id = http_request.author_id, description = http_request.description, isbn = http_request.isbn, publication_date = http_request.publication_date, cover_image = cover_image)
		result: Book = book_service.create_book(session, request)
		return BookCreationHTTPResponse.from_book(result)
	except ValidationError as e:
		raise HTTPException(detail = e.detail, status_code = status.HTTP_400_BAD_REQUEST)
	except Exception as e:
		logger.error(f"Error creating book: {e}")
		raise HTTPException(detail = "UNKNOWN_ERROR", status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)
