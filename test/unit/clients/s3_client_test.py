import pytest


from unittest.mock import MagicMock
from clients.s3_client import S3Client, PUBLIC_PATH, PRIVATE_PATH


class TestS3Client():
  def test_source(self):
    boto3_mock = MagicMock()
    instance = S3Client(boto3_mock, "my-bucket", "https://example.com")
    assert instance.source() == "s3"

  def test_upload_public(self):
    boto3_mock = MagicMock()
    instance = S3Client(boto3_mock, "my-bucket", "https://example.com")
    result = instance.upload("images/cover.jpg", b"data", "image/jpeg", public = True)
    boto3_mock.put_object.assert_called_once_with(
      Bucket = "my-bucket",
      Key = f"{PUBLIC_PATH}/images/cover.jpg",
      Body = b"data",
      ContentType = "image/jpeg"
    )
    assert result == f"https://example.com/my-bucket/{PUBLIC_PATH}/images/cover.jpg"

  def test_upload_private(self):
    boto3_mock = MagicMock()
    instance = S3Client(boto3_mock, "my-bucket", "https://example.com")
    result = instance.upload("images/cover.jpg", b"data", "image/jpeg", public = False)
    boto3_mock.put_object.assert_called_once_with(
      Bucket = "my-bucket",
      Key = f"{PRIVATE_PATH}/images/cover.jpg",
      Body = b"data",
      ContentType = "image/jpeg"
    )
    assert result == f"https://example.com/my-bucket/{PRIVATE_PATH}/images/cover.jpg"

  def test_upload_fail(self):
    boto3_mock = MagicMock()
    boto3_mock.put_object.side_effect = Exception("upload failed")
    instance = S3Client(boto3_mock, "my-bucket", "https://example.com")
    with pytest.raises(Exception) as exc_info:
      instance.upload("images/cover.jpg", b"data", "image/jpeg", public = True)
    assert str(exc_info.value) == "upload failed"
