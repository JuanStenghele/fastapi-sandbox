from fastapi import FastAPI
from app_builder import AppBuilder


def app() -> FastAPI:
  app_builder = AppBuilder()
  app = app_builder.build()
  return app
