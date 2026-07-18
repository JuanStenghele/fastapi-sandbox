from starlette.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from constants import CORS_PREFLIGHT_MAX_AGE_SECONDS, CORS_ALLOW_METHODS, CORS_ALLOW_HEADERS
from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from inject import Container


@inject
def build_cors_middleware(
  cors_middleware_enabled: bool =  Depends(Provide[Container.config.cors.middleware_enabled]),
  origins: list = Depends(Provide[Container.config.cors.allowed_origins])
) -> Middleware | None:
  if not cors_middleware_enabled:
    return None
  return Middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = CORS_ALLOW_METHODS,
    allow_headers = CORS_ALLOW_HEADERS,
    max_age = CORS_PREFLIGHT_MAX_AGE_SECONDS
  )
