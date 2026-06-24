from fastapi import FastAPI

from controllers.author_controller import router as author_router
from controllers.book_controller import router as book_router
from controllers.health_check import router as health_check_router
from controllers.storage_controller import router as storage_proxy_router
from services.logger import setup_logger
from inject import Container
from utils.rate_limiting import setup_rate_limiting


setup_logger()

app = FastAPI()
container: Container = Container()
app.container = container

# Initialize observability
observability_service = container.observability_service()
observability_service.setup(app)

setup_rate_limiting(app)

# Add routers
app.include_router(author_router, prefix = "/v1")
app.include_router(book_router, prefix = "/v1")
app.include_router(health_check_router, prefix = "/v1")
app.include_router(storage_proxy_router, prefix = "/storage")
