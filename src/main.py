from fastapi import FastAPI
from controllers.book_controller import router as book_router
from controllers.health_check import router as health_check_router
from services.logger import setup_logger
from inject import Container


setup_logger()

app = FastAPI()
container: Container = Container()
app.container = container

# Initialize observability
observability_service = container.observability_service()
observability_service.setup(app, container.db().engine)

# Add routers
app.include_router(book_router, prefix = "/v1")
app.include_router(health_check_router, prefix = "/v1")
