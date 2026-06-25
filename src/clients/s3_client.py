from logging import Logger
from botocore.client import BaseClient
from botocore.exceptions import BotoCoreError, ClientError
from clients.storage_client import StorageClient, StorageClientError
from constants import DEFAULT_CONTENT_TYPE, PUBLIC_PATH, PRIVATE_PATH
from objects.stored_object import StoredObject
from botocore.response import StreamingBody


class S3Client(StorageClient):
  def __init__(self, boto3_client: BaseClient, bucket_name: str, public_url: str, logger: Logger):
    self.boto3_client = boto3_client
    self.bucket_name = bucket_name
    self.public_url = public_url
    self.logger = logger

  def source(self) -> str:
    return "s3"

  def health_check(self) -> bool:
    try:
      self.boto3_client.head_bucket(Bucket = self.bucket_name)
      return True
    except (BotoCoreError, ClientError) as e:
      self.logger.error(f"Error checking storage health: {e}")
      return False

  def upload(self, name: str, data: bytes, content_type: str, public: bool = False) -> str | None:
    key = f"{PUBLIC_PATH}/{name}" if public else f"{PRIVATE_PATH}/{name}"
    self.boto3_client.put_object(
      Bucket = self.bucket_name,
      Key = key,
      Body = data,
      ContentType = content_type
    )
    return f"{self.public_url}/{name}" if public else None

  def get(self, name: str) -> StoredObject | None:
    try:
      object: dict = self.boto3_client.get_object(
        Bucket = self.bucket_name,
        Key = name
      )
      body: StreamingBody = object.get("Body")
      if body is None:
        raise StorageClientError("No body in S3 object")
      return StoredObject(
        body = body,
        content_type = object.get("ContentType", DEFAULT_CONTENT_TYPE)
      )
    except ClientError as e:
      if e.response["Error"]["Code"] == "NoSuchKey":
        return None
      raise StorageClientError from e
    except BotoCoreError as e:
      raise StorageClientError from e
