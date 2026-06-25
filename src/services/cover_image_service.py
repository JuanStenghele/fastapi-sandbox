import mimetypes


from datetime import datetime, timezone
from uuid import UUID
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

  def build_image_path(self, path: str, content_type: str) -> str:
    extension = mimetypes.guess_extension(content_type)
    if extension is not None and not path.endswith(extension):
      path += extension
    return path

  def create(self, session: Session, book_id: UUID, image: RawImage) -> CoverImage:
    self.cover_image_validator.validate_creation(image)
    image_data = image.file.read()
    path = self.build_image_path(f"{COVER_IMAGES_PATH}/{book_id}", image.content_type)
    url = self.storage_client.upload_user_content(path, image_data, image.content_type)
    now = datetime.now(timezone.utc)
    book_cover = BookCover(
      book_id = book_id,
      source = self.storage_client.source(),
      url = url,
      created_at = now,
      updated_at = now
    )
    self.book_cover_dal.create_book_cover(session, book_cover)
    return CoverImage(book_id = book_id, url = url)
