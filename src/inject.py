from logging import getLogger
from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dal.book_dal import BookDAL
from dal.health_check_dal import HealthCheckDAL
from database import Database
from services.book_service import BookService
from utils.database import build_db_url
from constants import POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_HOST_DEFAULT, POSTGRES_PORT_DEFAULT, POSTGRES_SSLMODE, POSTGRES_SSLMODE_DEFAULT, LOGGER_NAME


class Container(DeclarativeContainer):
  wiring_config = WiringConfiguration(
    modules = [
      "controllers.dependencies",
      "controllers.book_controller",
      "controllers.health_check"
    ]
  )

  config = providers.Configuration()

  # DB configuration
  config.db.name.from_env(POSTGRES_DB)
  config.db.user.from_env(POSTGRES_USER)
  config.db.password.from_env(POSTGRES_PASSWORD)
  config.db.host.from_env(POSTGRES_HOST, default = POSTGRES_HOST_DEFAULT)
  config.db.port.from_env(POSTGRES_PORT, default = POSTGRES_PORT_DEFAULT)
  config.db.sslmode.from_env(POSTGRES_SSLMODE, default = POSTGRES_SSLMODE_DEFAULT)

  logger = providers.Callable(
    getLogger,
    name = LOGGER_NAME
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

  book_dal = providers.Factory(
    BookDAL
  )

  book_service = providers.Factory(
    BookService,
    book_dal = book_dal
  )
