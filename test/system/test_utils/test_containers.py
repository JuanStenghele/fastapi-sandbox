import os, time, urllib.request, urllib.error


from pytest import FixtureRequest
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs
from constants import POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD
from system.test_utils.auth_utils import get_mock_oauth2_server_config
from system.test_utils.storage_utils import create_bucket


def otel_collector_instance(request: FixtureRequest) -> str:
  config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config", "otel-collector-config.yml")

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


def postgres_instance(request: FixtureRequest, db_name: str, db_user: str, db_password: str) -> tuple[str, str]:
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


def minio_instance(request: FixtureRequest, minio_user: str, minio_password: str, minio_bucket: str) -> tuple[str, str]:
  container = DockerContainer("minio/minio:RELEASE.2025-09-07T16-13-09Z")
  container.with_name("test-minio")
  container.with_exposed_ports(9000)
  container.with_env("MINIO_ROOT_USER", minio_user)
  container.with_env("MINIO_ROOT_PASSWORD", minio_password)
  container.with_command("server /data")
  container.start()

  def remove_container():
    container.stop()

  request.addfinalizer(remove_container)
  wait_for_logs(container, r".*API:.*http://.*", timeout = 120)

  host = container.get_container_host_ip()
  port = str(container.get_exposed_port(9000))
  endpoint_url = f"http://{host}:{port}"

  create_bucket(endpoint_url, minio_user, minio_password, minio_bucket)
  return host, port


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
