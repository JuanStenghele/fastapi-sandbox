import pytest, os, time, urllib.request, urllib.error


from fastapi.testclient import TestClient
from pytest import FixtureRequest
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs
from opentelemetry import metrics
from constants import (
  POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_SSLMODE,
  OTEL_EXPORTER_OTLP_ENDPOINT, AUTH_ISSUER, AUTH_AUDIENCE, AUTH_JWKS_URI
)
from utils.env_vars import set_env_vars
from utils.auth_utils import get_mock_oauth2_server_config
from alembic.config import Config
from alembic import command


db_name = "db"
db_user = "dev"
db_password = "qwerty123"
db_sslmode = "disable"

class Context():
  def __init__(self, app, client: TestClient, db_name: str, db_user: str, db_password: str, db_host: str, db_port: str, auth_token_url: str):
    self.app = app
    self.client = client
    self.db_name = db_name
    self.db_user = db_user
    self.db_password = db_password
    self.db_host = db_host
    self.db_port = db_port
    self.db_url = f"postgresql+psycopg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    self.auth_token_url = auth_token_url

def otel_collector_instance(request: FixtureRequest) -> str:
  config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "otel-collector-config.yml")

  otel_container = DockerContainer("otel/opentelemetry-collector-contrib:0.115.1")
  otel_container.with_name("test-otel-collector")
  otel_container.with_exposed_ports(4318)
  otel_container.with_volume_mapping(config_path, "/etc/otelcol-contrib/config.yaml", "ro")

  otel_container.start()

  def remove_container():
    otel_container.stop()

  request.addfinalizer(remove_container)
  wait_for_logs(otel_container, r".*Everything is ready.*", timeout = 120)

  host = otel_container.get_container_host_ip()
  port = otel_container.get_exposed_port(4318)
  return f"http://{host}:{port}/v1/metrics"


def postgres_instance(request: FixtureRequest) -> tuple[str, str]:
  postgres_container = DockerContainer("postgres:18.2-alpine")
  postgres_container.with_name("test-postgres-db")

  postgres_container.with_exposed_ports(5432)

  postgres_container.with_env(POSTGRES_DB, db_name)
  postgres_container.with_env(POSTGRES_USER, db_user)
  postgres_container.with_env(POSTGRES_PASSWORD, db_password)

  postgres_container.start()

  def remove_container():
    postgres_container.stop()

  request.addfinalizer(remove_container)
  wait_for_logs(postgres_container, r".*database system is ready to accept connections*", timeout = 120)
  return postgres_container.get_container_host_ip(), str(postgres_container.get_exposed_port(5432))


def mock_oauth2_server_instance(request: FixtureRequest) -> tuple[str, str]:
  container = DockerContainer("ghcr.io/navikt/mock-oauth2-server:3.0.1")
  container.with_name("test-mock-oauth2-server")
  container.with_exposed_ports(8080)
  container.with_env("JSON_CONFIG", get_mock_oauth2_server_config())
  container.start()

  def remove_container():
    container.stop()

  request.addfinalizer(remove_container)

  host = container.get_container_host_ip()
  port = str(container.get_exposed_port(8080))

  for _ in range(30):
    try:
      urllib.request.urlopen(f"http://{host}:{port}/isalive", timeout = 2)
      break
    except (urllib.error.URLError, OSError):
      time.sleep(1)

  return host, port


@pytest.fixture(scope = "session", autouse = True)
def context(request: FixtureRequest):
  db_host, db_port = postgres_instance(request)
  otel_endpoint = otel_collector_instance(request)
  auth_host, auth_port = mock_oauth2_server_instance(request)

  auth_base_url = f"http://{auth_host}:{auth_port}"
  auth_token_url = f"{auth_base_url}/fastapi-sandbox/token"

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
  }):
    # Import app here to ensure env vars are set before app initialization
    from main import app

    # Run DB migrations
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    alembic_ini_path = os.path.join(project_root, "alembic.ini")
    alembic_cfg = Config(alembic_ini_path)
    command.upgrade(alembic_cfg, "head")

    yield Context(app, TestClient(app), db_name, db_user, db_password, db_host, db_port, auth_token_url)

    metrics.get_meter_provider().shutdown()
