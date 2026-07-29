import mimetypes


from uuid import UUID
from sqlmodel import Session
from clients.storage_client import StorageClient, StorageClientError, USER_CONTENT_PATH
from dal.book_cover_dal import BookCoverDAL
from objects.book_cover import BookCover
from objects.cover_image import CoverImage
from objects.image import RawImage
from services.date_provider import DateProvider
from validators.cover_image_validator import CoverImageValidator


COVER_IMAGES_PATH = "cover-images"

class CoverImageService():
  def __init__(self, storage_client: StorageClient, book_cover_dal: BookCoverDAL, cover_image_validator: CoverImageValidator, date_provider: DateProvider):
    self.storage_client = storage_client
    self.book_cover_dal = book_cover_dal
    self.cover_image_validator = cover_image_validator
    self.date_provider = date_provider

  def build_image_path(self, path: str, content_type: str) -> str:
    extension = mimetypes.guess_extension(content_type)
    if extension is not None and not path.endswith(extension):
      path += extension
    return path

  def create(self, session: Session, book_id: UUID, image: RawImage) -> CoverImage:
    self.cover_image_validator.validate_creation(image)
    image_data = image.file.read()
    path = self.build_image_path(f"{COVER_IMAGES_PATH}/{book_id}", image.content_type)
    result = self.storage_client.upload_user_content(path, image_data, image.content_type)
    now = self.date_provider.now()
    book_cover = BookCover(
      book_id = book_id,
      source = self.storage_client.source(),
      url = result.url,
      path = result.path,
      created_at = now,
      updated_at = now
    )
    self.book_cover_dal.create_book_cover(session, book_cover)
    return CoverImage(book_id = book_id, url = result.url)

  def delete(self, session: Session, book_ids: list) -> None:
    book_covers = self.book_cover_dal.get_book_covers_by_ids(session, book_ids)
    if len(book_covers) != 0:
      try:
        names = [book_cover.path for book_cover in book_covers]
        self.storage_client.delete(names)
      except StorageClientError:
        # Ignore errors, leave objects orphan
        pass
    now = self.date_provider.now()
    self.book_cover_dal.soft_delete_book_covers(session, book_ids, now)

  def update(self, session: Session, book_id: UUID, image: RawImage) -> CoverImage:
    self.cover_image_validator.validate_creation(image)
    image_data = image.file.read()
    path = self.build_image_path(f"{COVER_IMAGES_PATH}/{book_id}", image.content_type)
    result = self.storage_client.upload_user_content(path, image_data, image.content_type)
    now = self.date_provider.now()
    old_cover = self.book_cover_dal.get_book_cover(session, book_id)
    self.book_cover_dal.update_book_cover(session, book_id, result.url, result.path, now)
    if old_cover is not None:
      try:
        self.storage_client.delete([old_cover.path])
      except StorageClientError:
        pass
    return CoverImage(book_id = book_id, url = result.url)
