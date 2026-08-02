import pytest


from unittest.mock import MagicMock
from uuid import uuid4
from sqlmodel import Session
from dal.stored_object_dal import StoredObjectDAL
from db_schema.stored_object_db import StoredObject as DBStoredObject
from objects.stored_object import StoredObjectRecord


class TestStoredObjectDal():
  def test_create_stored_object_success(self):
    session_mock = MagicMock(spec = Session)
    now = MagicMock()
    stored_object_id = uuid4()
    stored_object = StoredObjectRecord.model_construct(
      id = stored_object_id,
      source = "s3",
      key = "public/file.jpg",
      public_url = "https://example.com/file.jpg",
      created_at = now,
      updated_at = now
    )
    instance = StoredObjectDAL()
    result = instance.create_stored_object(session_mock, stored_object)
    assert result == stored_object
    added = session_mock.add.call_args[0][0]
    assert added.id == stored_object_id
    assert added.source == "s3"
    assert added.key == "public/file.jpg"
    assert added.public_url == "https://example.com/file.jpg"

  def test_create_stored_object_fail(self):
    session_mock = MagicMock(spec = Session)
    expected_message = 'Test Exception'
    session_mock.add.side_effect = Exception(expected_message)
    now = MagicMock()
    stored_object = StoredObjectRecord.model_construct(
      id = uuid4(),
      source = "s3",
      key = "public/file.jpg",
      created_at = now,
      updated_at = now
    )
    instance = StoredObjectDAL()
    with pytest.raises(Exception) as exc_info:
      instance.create_stored_object(session_mock, stored_object)
    assert str(exc_info.value) == expected_message
    assert session_mock.add.call_count == 1

  def test_get_stored_object_success(self):
    session_mock = MagicMock(spec = Session)
    now = MagicMock()
    stored_object_id = uuid4()
    db_stored_object = DBStoredObject(
      id = stored_object_id,
      source = "s3",
      key = "public/file.jpg",
      public_url = "https://example.com/file.jpg",
      created_at = now,
      updated_at = now
    )
    exec_mock = MagicMock()
    exec_mock.first.return_value = db_stored_object
    session_mock.exec.return_value = exec_mock
    instance = StoredObjectDAL()
    result = instance.get_stored_object(session_mock, stored_object_id)
    assert result is not None
    assert result.id == stored_object_id
    assert result.source == "s3"
    assert result.key == "public/file.jpg"
    assert result.public_url == "https://example.com/file.jpg"
    assert session_mock.exec.call_count == 1

  def test_get_stored_object_not_found(self):
    session_mock = MagicMock(spec = Session)
    exec_mock = MagicMock()
    exec_mock.first.return_value = None
    session_mock.exec.return_value = exec_mock
    instance = StoredObjectDAL()
    result = instance.get_stored_object(session_mock, uuid4())
    assert result is None
    assert session_mock.exec.call_count == 1

  def test_get_stored_object_fail(self):
    session_mock = MagicMock(spec = Session)
    expected_message = 'Test Exception'
    session_mock.exec.side_effect = Exception(expected_message)
    instance = StoredObjectDAL()
    with pytest.raises(Exception) as exc_info:
      instance.get_stored_object(session_mock, uuid4())
    assert str(exc_info.value) == expected_message
    assert session_mock.exec.call_count == 1

  def test_get_stored_objects_by_ids_success(self):
    session_mock = MagicMock(spec = Session)
    now = MagicMock()
    stored_object_id_1 = uuid4()
    stored_object_id_2 = uuid4()
    db_stored_object_1 = DBStoredObject(
      id = stored_object_id_1,
      source = "s3",
      key = "public/file1.jpg",
      created_at = now,
      updated_at = now
    )
    db_stored_object_2 = DBStoredObject(
      id = stored_object_id_2,
      source = "s3",
      key = "public/file2.jpg",
      created_at = now,
      updated_at = now
    )
    exec_mock = MagicMock()
    exec_mock.all.return_value = [db_stored_object_1, db_stored_object_2]
    session_mock.exec.return_value = exec_mock
    instance = StoredObjectDAL()
    result = instance.get_stored_objects(session_mock, limit = 10, offset = 0, ids = [stored_object_id_1, stored_object_id_2])
    assert len(result) == 2
    assert result[0].id == stored_object_id_1
    assert result[0].source == "s3"
    assert result[1].id == stored_object_id_2
    assert session_mock.exec.call_count == 1

  def test_get_stored_objects_by_ids_empty_results(self):
    session_mock = MagicMock(spec = Session)
    exec_mock = MagicMock()
    exec_mock.all.return_value = []
    session_mock.exec.return_value = exec_mock
    instance = StoredObjectDAL()
    result = instance.get_stored_objects(session_mock, limit = 10, offset = 0, ids = [uuid4()])
    assert result == []
    assert session_mock.exec.call_count == 1

  def test_get_stored_objects_by_ids_fail(self):
    session_mock = MagicMock(spec = Session)
    expected_message = 'Test Exception'
    session_mock.exec.side_effect = Exception(expected_message)
    instance = StoredObjectDAL()
    with pytest.raises(Exception) as exc_info:
      instance.get_stored_objects(session_mock, limit = 10, offset = 0, ids = [uuid4()])
    assert str(exc_info.value) == expected_message
    assert session_mock.exec.call_count == 1

  def test_soft_delete_stored_objects_success(self):
    session_mock = MagicMock(spec = Session)
    now = MagicMock()
    stored_object_id = uuid4()
    instance = StoredObjectDAL()
    instance.soft_delete_stored_objects(session_mock, [stored_object_id], now)
    assert session_mock.exec.call_count == 1

  def test_soft_delete_stored_objects_fail(self):
    session_mock = MagicMock(spec = Session)
    expected_message = 'Test Exception'
    session_mock.exec.side_effect = Exception(expected_message)
    now = MagicMock()
    instance = StoredObjectDAL()
    with pytest.raises(Exception) as exc_info:
      instance.soft_delete_stored_objects(session_mock, [uuid4()], now)
    assert str(exc_info.value) == expected_message
    assert session_mock.exec.call_count == 1
