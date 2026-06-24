import boto3


from logging import getLogger
from jwt import PyJWKClient
from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from services.auth import AuthService
from dal.author_dal import AuthorDAL
from dal.book_dal import BookDAL
from validators.book_validator import BookValidator
from dal.health_check_dal import HealthCheckDAL
from database import Database
from services.author_service import AuthorService
from services.book_service import BookService
from services.observability import ObservabilityService
from services.cover_image_service import CoverImageService
from services.storage_proxy import StorageProxy
from validators.cover_image_validator import CoverImageValidator
from clients.s3_client import S3Client
from dal.book_cover_dal import BookCoverDAL
from utils.database import build_db_url
from constants import POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_HOST_DEFAULT, POSTGRES_PORT_DEFAULT, POSTGRES_SSLMODE, POSTGRES_SSLMODE_DEFAULT, LOGGER_NAME, OTEL_EXPORTER_OTLP_ENDPOINT, OTEL_EXPORTER_OTLP_ENDPOINT_DEFAULT, ENV, ENV_PRODUCTION, AUTH_AUDIENCE, AUTH_ISSUER, AUTH_JWKS_URI, S3_SERVICE_NAME, STORAGE_SERVICE_URL, STORAGE_PUBLIC_URL, STORAGE_ACCESS_KEY_ID, STORAGE_SECRET_ACCESS_KEY, STORAGE_BUCKET_NAME, STORAGE_REGION, STORAGE_REGION_DEFAULT


class Container(DeclarativeContainer):
  wiring_config = WiringConfiguration(
    modules = [
      "controllers.dependencies",
      "controllers.author_controller",
      "controllers.book_controller",
      "controllers.health_check",
      "controllers.storage_controller"
    ]
  )

  config = providers.Configuration()

  config.env.from_env(ENV, default = ENV_PRODUCTION)

  # DB configuration
  config.db.name.from_env(POSTGRES_DB)
  config.db.user.from_env(POSTGRES_USER)
  config.db.password.from_env(POSTGRES_PASSWORD)
  config.db.host.from_env(POSTGRES_HOST, default = POSTGRES_HOST_DEFAULT)
  config.db.port.from_env(POSTGRES_PORT, default = POSTGRES_PORT_DEFAULT)
  config.db.sslmode.from_env(POSTGRES_SSLMODE, default = POSTGRES_SSLMODE_DEFAULT)

  # OTel configuration
  config.otel.otlp_endpoint.from_env(OTEL_EXPORTER_OTLP_ENDPOINT, default = OTEL_EXPORTER_OTLP_ENDPOINT_DEFAULT)

  # Auth configuration
  config.auth.issuer.from_env(AUTH_ISSUER)
  config.auth.audience.from_env(AUTH_AUDIENCE)
  config.auth.jwks_uri.from_env(AUTH_JWKS_URI)

  # Storage configuration
  config.storage.service_url.from_env(STORAGE_SERVICE_URL, default = None)
  config.storage.public_url.from_env(STORAGE_PUBLIC_URL)
  config.storage.access_key_id.from_env(STORAGE_ACCESS_KEY_ID)
  config.storage.secret_access_key.from_env(STORAGE_SECRET_ACCESS_KEY)
  config.storage.bucket_name.from_env(STORAGE_BUCKET_NAME)
  config.storage.region.from_env(STORAGE_REGION, default = STORAGE_REGION_DEFAULT)

  logger = providers.Callable(
    getLogger,
    name = LOGGER_NAME
  )

  jwks_client = providers.Singleton(
    PyJWKClient,
    config.auth.jwks_uri
  )

  auth_service = providers.Singleton(
    AuthService,
    issuer = config.auth.issuer,
    audience = config.auth.audience,
    jwks_client = jwks_client
  )

  observability_service = providers.Singleton(
    ObservabilityService,
    otlp_endpoint = config.otel.otlp_endpoint,
    env = config.env,
    logger = logger
  )

  db_url = providers.Callable(
    build_db_url,
    user = config.db.user,
    password = config.db.password,
    host = config.db.host,
    port = config.db.port,
    name = config.db.name,
    sslmode = config.db.sslmode
  )

  db = providers.Singleton(
    Database, 
    url = db_url,
    logger = logger
  )

  health_check_dal = providers.Factory(
    HealthCheckDAL,
    logger = logger
  )

  author_dal = providers.Factory(
    AuthorDAL
  )

  book_dal = providers.Factory(
    BookDAL
  )

  author_service = providers.Factory(
    AuthorService,
    author_dal = author_dal
  )

  boto3_client = providers.Singleton(
    boto3.client,
    service_name = S3_SERVICE_NAME,
    service_url = config.storage.service_url,
    aws_access_key_id = config.storage.access_key_id,
    aws_secret_access_key = config.storage.secret_access_key,
    region_name = config.storage.region
  )

  s3_client = providers.Singleton(
    S3Client,
    boto3_client = boto3_client,
    bucket_name = config.storage.bucket_name,
    public_url = config.storage.public_url,
    logger = logger
  )

  storage_proxy = providers.Factory(
    StorageProxy,
    storage_client = s3_client
  )

  book_cover_dal = providers.Factory(
    BookCoverDAL
  )

  cover_image_validator = providers.Singleton(
    CoverImageValidator
  )

  cover_image_service = providers.Singleton(
    CoverImageService,
    storage_client = s3_client,
    book_cover_dal = book_cover_dal,
    cover_image_validator = cover_image_validator
  )

  book_validator = providers.Factory(
    BookValidator,
    author_dal = author_dal
  )

  book_service = providers.Factory(
    BookService,
    book_dal = book_dal,
    cover_image_service = cover_image_service,
    book_validator = book_validator
  )
