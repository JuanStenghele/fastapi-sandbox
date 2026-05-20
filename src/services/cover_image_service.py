import uuid


from datetime import datetime, timezone
from sqlmodel import Session
from clients.storage_client import StorageClient
from dal.book_cover_dal import BookCoverDAL
from objects.book_cover import BookCover
from objects.cover_image import CoverImage
from objects.image import RawImage
from validators.cover_image_validator import CoverImageValidator


COVER_IMAGES_PATH = "cover-images"

class CoverImageService():
  def __init__(self, storage_client: StorageClient, book_cover_dal: BookCoverDAL, cover_image_validator: CoverImageValidator):
    self.storage_client = storage_client
    self.book_cover_dal = book_cover_dal
    self.cover_image_validator = cover_image_validator

  def create(self, session: Session, image: RawImage) -> CoverImage:
    self.cover_image_validator.validate_creation(image)
    id = uuid.uuid4()
    image_data = image.file.read()
    url = self.storage_client.upload_user_content(f"{COVER_IMAGES_PATH}/{id}", image_data, image.content_type)
    now = datetime.now(timezone.utc)
    book_cover = BookCover(
      id = id,
      source = self.storage_client.source(),
      url = url,
      created_at = now,
      updated_at = now
    )
    self.book_cover_dal.create_book_cover(session, book_cover)
    return CoverImage(id = id, url = url)
