from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from constants import RATE_LIMIT_DEFAULT
from slowapi.errors import RateLimitExceeded


def setup_rate_limiting(app: FastAPI):
  limiter = Limiter(
    key_func = get_remote_address, 
    default_limits = [RATE_LIMIT_DEFAULT]
  )
  app.state.limiter = limiter
  app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
  app.add_middleware(SlowAPIMiddleware)
