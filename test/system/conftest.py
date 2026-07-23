import pytest, os

from fastapi.testclient import TestClient
from pytest import FixtureRequest
from opentelemetry import metrics, trace
from opentelemetry._logs import get_logger_provider
from constants import (
  POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_SSLMODE,
  OTEL_EXPORTER_OTLP_ENDPOINT, AUTH_ISSUER, AUTH_AUDIENCE, AUTH_JWKS_URI,
  STORAGE_SERVICE_URL, STORAGE_PUBLIC_URL, STORAGE_ACCESS_KEY_ID, STORAGE_SECRET_ACCESS_KEY, STORAGE_BUCKET_NAME
)
from system.test_utils.env_vars import set_env_vars
from system.test_utils.test_containers import otel_collector_instance, postgres_instance, minio_instance, mock_oauth2_server_instance
from alembic.config import Config
from alembic import command
from main import app


db_name = "db"
db_user = "dev"
db_password = "qwerty123"
db_sslmode = "disable"

minio_user = "admin"
minio_password = "qwerty123"
minio_bucket = "fastapi-sandbox-test"

class Context():
  def __init__(self, default_app, client: TestClient, db_name: str, db_user: str, db_password: str, db_host: str, db_port: str, auth_token_url: str, storage_service_url: str, storage_access_key_id: str, storage_secret_access_key: str, storage_bucket_name: str):
    self.app = default_app
    self.client = client
    self.db_name = db_name
    self.db_user = db_user
    self.db_password = db_password
    self.db_host = db_host
    self.db_port = db_port
    self.db_url = f"postgresql+psycopg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    self.auth_token_url = auth_token_url
    self.storage_service_url = storage_service_url
    self.storage_access_key_id = storage_access_key_id
    self.storage_secret_access_key = storage_secret_access_key
    self.storage_bucket_name = storage_bucket_name


@pytest.fixture(scope = "session", autouse = True)
def context(request: FixtureRequest):
  db_host, db_port = postgres_instance(request, db_name, db_user, db_password)
  otel_endpoint = otel_collector_instance(request)
  auth_host, auth_port = mock_oauth2_server_instance(request)
  minio_host, minio_port = minio_instance(request, minio_user, minio_password, minio_bucket)

  auth_base_url = f"http://{auth_host}:{auth_port}"
  auth_token_url = f"{auth_base_url}/fastapi-sandbox/token"
  minio_endpoint = f"http://{minio_host}:{minio_port}"

  with set_env_vars({
    POSTGRES_DB: db_name,
    POSTGRES_USER: db_user,
    POSTGRES_PASSWORD: db_password,
    POSTGRES_HOST: db_host,
    POSTGRES_PORT: db_port,
    POSTGRES_SSLMODE: db_sslmode,
    OTEL_EXPORTER_OTLP_ENDPOINT: otel_endpoint,
    AUTH_ISSUER: f"{auth_base_url}/fastapi-sandbox",
    AUTH_AUDIENCE: "fastapi-sandbox",
    AUTH_JWKS_URI: f"{auth_base_url}/fastapi-sandbox/jwks",
    STORAGE_SERVICE_URL: minio_endpoint,
    STORAGE_PUBLIC_URL: minio_endpoint,
    STORAGE_ACCESS_KEY_ID: minio_user,
    STORAGE_SECRET_ACCESS_KEY: minio_password,
    STORAGE_BUCKET_NAME: minio_bucket,
  }):
    default_app = app()

    # Disable rate limiting
    default_app.state.limiter.enabled = False

    # Run DB migrations
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    alembic_ini_path = os.path.join(project_root, "alembic.ini")
    alembic_cfg = Config(alembic_ini_path)
    command.upgrade(alembic_cfg, "head")

    yield Context(default_app, TestClient(default_app), db_name, db_user, db_password, db_host, db_port, auth_token_url, minio_endpoint, minio_user, minio_password, minio_bucket)

    metrics.get_meter_provider().shutdown()
    trace.get_tracer_provider().shutdown()
    get_logger_provider().shutdown()
