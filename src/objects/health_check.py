from objects.base import BaseObj


class HealthCheckResponse(BaseObj):
  api: str


class DeepHealthCheckResponse(BaseObj):
  api: str
  postgres_database: str
  storage: str
