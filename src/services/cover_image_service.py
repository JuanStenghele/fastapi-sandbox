from uuid import UUID
from sqlmodel import Session
from clients.storage_client import StorageClient
from objects.cover_image import CoverImage
from objects.image import RawImage
from dal.book_dal import BookDAL
from services.date_provider import DateProvider
from services.storage_service import StorageService
from validators.cover_image_validator import CoverImageValidator
from objects.stored_object import ObjectToStoreInS3


COVER_IMAGES_PATH = "cover-images"

class CoverImageService():
  def __init__(self, storage_client: StorageClient, cover_image_validator: CoverImageValidator, date_provider: DateProvider, storage_service: StorageService, book_dal: BookDAL):
    self.storage_client = storage_client
    self.cover_image_validator = cover_image_validator
    self.date_provider = date_provider
    self.storage_service = storage_service
    self.book_dal = book_dal

  def create_book_cover(self, session: Session, book_id: UUID, image: RawImage) -> CoverImage:
    self.cover_image_validator.validate_upsert(session, book_id, image)
    image_data = image.file.read()
    object_to_store = ObjectToStoreInS3.with_key_template(f'{COVER_IMAGES_PATH}/{ObjectToStoreInS3.ID}.{ObjectToStoreInS3.EXT}', image_data, image.content_type)
    result = self.storage_service.store_object(session, self.storage_client, object_to_store)
    self.book_dal.update_book_cover_stored_object_id(session, book_id, result.id, self.date_provider.now())
    return CoverImage(stored_object_id = result.id, book_id = book_id, url = result.public_url)

  def update_book_cover(self, session: Session, book_id: UUID, image: RawImage) -> CoverImage:
    self.delete_book_covers(session, [book_id])
    return self.create_book_cover(session, book_id, image)

  def delete_book_covers(self, session: Session, book_ids: list) -> None:
    self.cover_image_validator.validate_deletion(session, book_ids)
    self.storage_service.delete_stored_objects(session, self.storage_client, book_ids)
    self.book_dal.delete_book_cover_stored_object_ids(session, book_ids, self.date_provider.now())
