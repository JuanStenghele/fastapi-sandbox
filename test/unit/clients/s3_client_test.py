import pytest


from unittest.mock import MagicMock
from botocore.exceptions import ClientError, BotoCoreError
from clients.s3_client import S3Client
from clients.storage_client import StorageClientError
from constants import DEFAULT_CONTENT_TYPE, PUBLIC_PATH, PRIVATE_PATH


class TestS3Client():
  def test_source(self):
    boto3_mock = MagicMock()
    logger_mock = MagicMock()
    instance = S3Client(boto3_mock, "my-bucket", "https://example.com", logger_mock)
    assert instance.source() == "s3"

  def test_health_check_success(self):
    boto3_mock = MagicMock()
    logger_mock = MagicMock()
    instance = S3Client(boto3_mock, "my-bucket", "https://example.com", logger_mock)
    assert instance.health_check() == True
    boto3_mock.head_bucket.assert_called_once_with(Bucket = "my-bucket")

  def test_health_check_client_error(self):
    boto3_mock = MagicMock()
    boto3_mock.head_bucket.side_effect = ClientError({}, "head_bucket")
    logger_mock = MagicMock()
    instance = S3Client(boto3_mock, "my-bucket", "https://example.com", logger_mock)
    assert instance.health_check() == False
    logger_mock.error.assert_called_once()

  def test_health_check_boto_core_error(self):
    boto3_mock = MagicMock()
    boto3_mock.head_bucket.side_effect = BotoCoreError()
    logger_mock = MagicMock()
    instance = S3Client(boto3_mock, "my-bucket", "https://example.com", logger_mock)
    assert instance.health_check() == False
    logger_mock.error.assert_called_once()

  def test_upload_public(self):
    boto3_mock = MagicMock()
    logger_mock = MagicMock()
    instance = S3Client(boto3_mock, "my-bucket", "https://example.com", logger_mock)
    result = instance.upload("images/cover", b"data", "image/jpeg", public = True)
    boto3_mock.put_object.assert_called_once_with(
      Bucket = "my-bucket",
      Key = f"{PUBLIC_PATH}/images/cover.jpg",
      Body = b"data",
      ContentType = "image/jpeg"
    )
    assert result == "https://example.com/images/cover.jpg"

  def test_upload_private(self):
    boto3_mock = MagicMock()
    logger_mock = MagicMock()
    instance = S3Client(boto3_mock, "my-bucket", "https://example.com", logger_mock)
    result = instance.upload("images/cover", b"data", "image/jpeg", public = False)
    boto3_mock.put_object.assert_called_once_with(
      Bucket = "my-bucket",
      Key = f"{PRIVATE_PATH}/images/cover.jpg",
      Body = b"data",
      ContentType = "image/jpeg"
    )
    assert result is None

  def test_upload_fail(self):
    boto3_mock = MagicMock()
    logger_mock = MagicMock()
    boto3_mock.put_object.side_effect = Exception("upload failed")
    instance = S3Client(boto3_mock, "my-bucket", "https://example.com", logger_mock)
    with pytest.raises(Exception) as exc_info:
      instance.upload("images/cover", b"data", "image/jpeg", public = True)
    assert str(exc_info.value) == "upload failed"

  def test_get_success(self):
    boto3_mock = MagicMock()
    logger_mock = MagicMock()
    body_mock = MagicMock()
    body_mock.read.return_value = b"file content"
    boto3_mock.get_object.return_value = {
      "Body": body_mock,
      "ContentType": "image/png"
    }
    instance = S3Client(boto3_mock, "my-bucket", "https://example.com", logger_mock)
    result = instance.get("public/image.png")
    boto3_mock.get_object.assert_called_once_with(
      Bucket = "my-bucket",
      Key = "public/image.png"
    )
    assert result.body == b"file content"
    assert result.content_type == "image/png"

  def test_get_default_content_type(self):
    boto3_mock = MagicMock()
    logger_mock = MagicMock()
    body_mock = MagicMock()
    body_mock.read.return_value = b"file content"
    boto3_mock.get_object.return_value = {
      "Body": body_mock
    }
    instance = S3Client(boto3_mock, "my-bucket", "https://example.com", logger_mock)
    result = instance.get("public/file.bin")
    assert result.body == b"file content"
    assert result.content_type == DEFAULT_CONTENT_TYPE

  def test_get_no_body(self):
    boto3_mock = MagicMock()
    logger_mock = MagicMock()
    boto3_mock.get_object.return_value = {}
    instance = S3Client(boto3_mock, "my-bucket", "https://example.com", logger_mock)
    with pytest.raises(StorageClientError) as exc_info:
      instance.get("public/missing.txt")
    assert str(exc_info.value) == "No body in S3 object"

  def test_get_not_found(self):
    boto3_mock = MagicMock()
    logger_mock = MagicMock()
    boto3_mock.get_object.side_effect = ClientError(
      {"Error": {"Code": "NoSuchKey"}}, "get_object"
    )
    instance = S3Client(boto3_mock, "my-bucket", "https://example.com", logger_mock)
    result = instance.get("public/nonexistent.txt")
    assert result is None

  def test_get_client_error(self):
    boto3_mock = MagicMock()
    logger_mock = MagicMock()
    boto3_mock.get_object.side_effect = ClientError(
      {"Error": {"Code": "AccessDenied"}}, "get_object"
    )
    instance = S3Client(boto3_mock, "my-bucket", "https://example.com", logger_mock)
    with pytest.raises(StorageClientError):
      instance.get("public/secret.txt")

  def test_get_boto_core_error(self):
    boto3_mock = MagicMock()
    logger_mock = MagicMock()
    boto3_mock.get_object.side_effect = BotoCoreError()
    instance = S3Client(boto3_mock, "my-bucket", "https://example.com", logger_mock)
    with pytest.raises(StorageClientError):
      instance.get("public/broken.txt")
