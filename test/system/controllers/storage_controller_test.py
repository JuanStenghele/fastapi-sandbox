import pytest


from system.utils.storage_utils import get_test_image_path, save_file, clean_bucket
from system.conftest import Context


class TestStorageController():
  @pytest.fixture(autouse = True)
  def after_each(self, context: Context):
    yield
    clean_bucket(context.storage_service_url, context.storage_access_key_id, context.storage_secret_access_key, context.storage_bucket_name)

  def test_get_public_image(self, context: Context):
    cover_image = open(get_test_image_path("harry_potter_cover.jpg"), "rb")
    image_data = cover_image.read()
    cover_image.close()
    save_file(
      context.storage_service_url,
      context.storage_access_key_id,
      context.storage_secret_access_key,
      context.storage_bucket_name,
      "public/test-image.jpg",
      image_data,
      "image/jpeg"
    )
    response = context.client.get("/storage/test-image.jpg")
    assert response.status_code == 200
    assert response.content == image_data
    assert response.headers["content-type"] == "image/jpeg"

  def test_get_private_file_not_accessible(self, context: Context):
    save_file(
      context.storage_service_url,
      context.storage_access_key_id,
      context.storage_secret_access_key,
      context.storage_bucket_name,
      "private/secret.txt",
      b"secret content",
      "text/plain"
    )
    response = context.client.get("/storage/secret.txt")
    assert response.status_code == 404
    assert response.json() == {"detail": "OBJECT_NOT_FOUND"}

  def test_get_not_found(self, context: Context):
    response = context.client.get("/storage/nonexistent.txt")
    assert response.status_code == 404
    assert response.json() == {"detail": "OBJECT_NOT_FOUND"}
