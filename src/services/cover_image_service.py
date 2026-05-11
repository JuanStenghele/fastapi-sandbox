import uuid
from datetime import datetime, timezone
from sqlmodel import Session
from clients.storage_client import StorageClient
from dal.book_cover_dal import BookCoverDAL
from objects.book_cover import BookCover
from objects.image import RawImage
from validators.cover_image_validator import CoverImageValidator


class CoverImageService():
  def __init__(self, storage_client: StorageClient, book_cover_dal: BookCoverDAL, cover_image_validator: CoverImageValidator):
    self.storage_client = storage_client
    self.book_cover_dal = book_cover_dal
    self.cover_image_validator = cover_image_validator

  def create(self, session: Session, image: RawImage) -> BookCover:
    self.cover_image_validator.validate(image)
    id = uuid.uuid4()
    url = self.storage_client.upload(str(id), image.data, image.content_type)
    now = datetime.now(timezone.utc)
    book_cover = BookCover(
      id = id,
      source = self.storage_client.source,
      url = url,
      created_at = now,
      updated_at = now
    )
    return self.book_cover_dal.create_book_cover(session, book_cover)
