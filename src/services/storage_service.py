import uuid


from sqlmodel import Session
from clients.storage_client import StorageClient, StorageClientError
from dal.stored_object_dal import StoredObjectDAL
from dal.book_dal import BookDAL
from objects.stored_object import ObjectToStore, StoredObject
from services.date_provider import DateProvider


class StorageService():
  def __init__(self, date_provider: DateProvider, book_dal: BookDAL, stored_object_dal: StoredObjectDAL) -> None:
    self.date_provider = date_provider
    self.book_dal = book_dal
    self.stored_object_dal = stored_object_dal

  def store_object(self, session: Session, storage_client: StorageClient, object: ObjectToStore) -> StoredObject:
    id = uuid.uuid4()
    result = storage_client.upload_object(
      object.key(id), 
      object.data, 
      object.content_type,
      public = True
    )
    now = self.date_provider.now()
    stored_object = StoredObject(
      id = id,
      source = storage_client.source(),
      key = result.path,
      public_url = result.public_url,
      created_at = now,
      updated_at = now
    )
    self.stored_object_dal.create_stored_object(session, stored_object)
    return stored_object

  def delete_stored_objects(self, session: Session, storage_client: StorageClient, ids: list) -> None:
    stored_objects = self.stored_object_dal.get_stored_objects(session, len(ids), 0, ids = ids)
    if len(stored_objects) == 0:
      return
    now = self.date_provider.now()
    self.stored_object_dal.soft_delete_stored_objects(session, ids, now)
    storage_client.delete_objects([object.key for object in stored_objects])
