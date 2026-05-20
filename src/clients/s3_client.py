from botocore.client import BaseClient
from clients.storage_client import StorageClient


PUBLIC_PATH = "public"
PRIVATE_PATH = "private"

class S3Client(StorageClient):
  def __init__(self, boto3_client: BaseClient, bucket_name: str, public_url: str):
    self.boto3_client = boto3_client
    self.bucket_name = bucket_name
    self.public_url = public_url

  def source(self) -> str:
    return "s3"

  def upload(self, name: str, data: bytes, content_type: str, public: bool = False) -> str:
    key = f"{PUBLIC_PATH}/{name}" if public else f"{PRIVATE_PATH}/{name}"
    self.boto3_client.put_object(
      Bucket = self.bucket_name,
      Key = key,
      Body = data,
      ContentType = content_type
    )
    return f"{self.public_url}/{self.bucket_name}/{key}"
