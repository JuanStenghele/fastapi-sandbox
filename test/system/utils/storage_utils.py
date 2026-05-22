import boto3


from botocore.exceptions import ClientError


def create_bucket(endpoint_url: str, access_key_id: str, secret_access_key: str, bucket_name: str):
  client = boto3.client(
    "s3",
    endpoint_url = endpoint_url,
    aws_access_key_id = access_key_id,
    aws_secret_access_key = secret_access_key,
    region_name = "us-east-1"
  )
  client.create_bucket(Bucket = bucket_name)


def file_exists(endpoint_url: str, access_key_id: str, secret_access_key: str, bucket_name: str, key: str) -> bool:
  client = boto3.client(
    "s3",
    endpoint_url = endpoint_url,
    aws_access_key_id = access_key_id,
    aws_secret_access_key = secret_access_key,
    region_name = "us-east-1"
  )
  try:
    client.head_object(Bucket = bucket_name, Key = key)
    return True
  except ClientError:
    return False


def clean_bucket(endpoint_url: str, access_key_id: str, secret_access_key: str, bucket_name: str):
  client = boto3.client(
    "s3",
    endpoint_url = endpoint_url,
    aws_access_key_id = access_key_id,
    aws_secret_access_key = secret_access_key,
    region_name = "us-east-1"
  )
  response = client.list_objects_v2(Bucket = bucket_name)
  objects = response.get("Contents", [])
  if not objects:
    return
  client.delete_objects(
    Bucket = bucket_name,
    Delete = { "Objects": [{ "Key": obj["Key"] } for obj in objects] }
  )
