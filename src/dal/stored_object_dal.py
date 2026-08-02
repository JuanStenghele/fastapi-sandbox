from datetime import datetime
from uuid import UUID
from sqlmodel import select, update, Session
from db_schema.stored_object_db import StoredObject as DBStoredObject
from objects.stored_object_record import StoredObject


class StoredObjectDAL():
  def create_stored_object(self, session: Session, stored_object: StoredObject) -> StoredObject:
    db_stored_object = DBStoredObject(
      id = stored_object.id,
      source = stored_object.source,
      key = stored_object.key,
      public_url = stored_object.public_url,
      created_at = stored_object.created_at,
      updated_at = stored_object.updated_at
    )
    session.add(db_stored_object)
    return stored_object

  def get_stored_object(self, session: Session, id: UUID) -> StoredObject | None:
    query = select(DBStoredObject).where(DBStoredObject.id == id, DBStoredObject.deleted_at == None)
    result = session.exec(query).first()
    if result is None:
      return None
    return StoredObject.model_validate(result)

  def get_stored_objects_by_ids(self, session: Session, ids: list) -> list[StoredObject]:
    query = select(DBStoredObject).where(DBStoredObject.id.in_(ids), DBStoredObject.deleted_at == None)
    results = session.exec(query).all()
    return [StoredObject.model_validate(result) for result in results]

  def soft_delete_stored_objects(self, session: Session, ids: list, deleted_at: datetime) -> None:
    query = update(DBStoredObject).where(DBStoredObject.id.in_(ids)).values(deleted_at = deleted_at)
    session.exec(query)
