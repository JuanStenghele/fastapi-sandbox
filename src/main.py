import os


from fastapi import FastAPI
from controllers.book_controller import router as book_router
from controllers.health_check import router as health_check_router
from services.logger import setup_logger
from constants import ENV, ENV_TESTING
from database import Database


setup_logger()

app = FastAPI()
if os.getenv(ENV) != ENV_TESTING:
  from inject import Container
  container: Container = Container()
  setattr(app, 'container', container)
  db: Database = getattr(app, 'container').db()
  db.create_database()

app.include_router(book_router, prefix = "/v1")
app.include_router(health_check_router, prefix = "/v1")
