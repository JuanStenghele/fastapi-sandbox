import logging, logging.config


from fastapi import FastAPI
from controllers.author_controller import router as author_router
from controllers.book_controller import router as book_router
from controllers.health_check import router as health_check_router
from controllers.storage_controller import router as storage_proxy_router
from inject import Container
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from constants import RATE_LIMIT_DEFAULT, CORS_PREFLIGHT_MAX_AGE_SECONDS, CORS_ALLOW_METHODS, CORS_ALLOW_HEADERS
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware
from services.logger import LOGGING_CONFIG


class AppBuilder():
  def build(self) -> FastAPI:
    app = FastAPI()
    self.setup_logger()
    container = self.setup_dependency_injection(app)
    self.setup_observability(app, container)
    self.setup_rate_limiting(app)
    if container.config.cors.middleware_enabled():
      self.setup_cors_middleware(app, container)
    self.add_routers(app)
    return app

  def setup_logger(self) -> None:
    logging.config.dictConfig(LOGGING_CONFIG)

  def setup_dependency_injection(self, app: FastAPI) -> Container:
    # Config load should be done before instantiation due to wiring
    Container.load_config()
    container = Container()
    app.container = container
    return container

  def setup_observability(self, app: FastAPI, container: Container) -> None:
    container.observability_service().setup(app)

  def setup_rate_limiting(self, app: FastAPI) -> None:
    limiter = Limiter(
      key_func = get_remote_address, 
      default_limits = [RATE_LIMIT_DEFAULT]
    )
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)

  def setup_cors_middleware(self, app: FastAPI, container: Container) -> None:
    origins = container.config.cors.allowed_origins()
    app.add_middleware(
      CORSMiddleware,
      allow_origins = origins,
      allow_credentials = True,
      allow_methods = CORS_ALLOW_METHODS,
      allow_headers = CORS_ALLOW_HEADERS,
      max_age = CORS_PREFLIGHT_MAX_AGE_SECONDS
    )

  def add_routers(self, app: FastAPI) -> None:
    app.include_router(author_router, prefix = "/v1")
    app.include_router(book_router, prefix = "/v1")
    app.include_router(health_check_router, prefix = "/v1")
    app.include_router(storage_proxy_router, prefix = "/storage")
