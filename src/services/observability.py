from logging import Logger
from fastapi import FastAPI
from sqlalchemy import Engine
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from constants import OTEL_METRIC_EXPORT_INTERVAL_MILLIS, OTEL_SERVICE_NAME


class ObservabilityService():
  def __init__(self, otlp_endpoint: str, env: str, logger: Logger):
    self.service_name = OTEL_SERVICE_NAME
    self.otlp_endpoint = otlp_endpoint
    self.env = env
    self.logger = logger

  def setup(self, app: FastAPI, engine: Engine) -> None:
    self.setup_metrics()
    FastAPIInstrumentor.instrument_app(app)
    self.logger.info("FastAPI instrumented with OpenTelemetry")
    SQLAlchemyInstrumentor().instrument(engine = engine)
    self.logger.info("SQLAlchemy instrumented with OpenTelemetry")
    self.logger.info("Observability service setup complete")

  def setup_metrics(self) -> None:
    resource = Resource(attributes = {"service.name": self.service_name, "deployment.environment": self.env})
    # OTLP exporter pushes metrics to OTel Collector
    otlp_exporter = OTLPMetricExporter(
      endpoint = self.otlp_endpoint
    )
    reader = PeriodicExportingMetricReader(otlp_exporter, export_interval_millis = OTEL_METRIC_EXPORT_INTERVAL_MILLIS)
    provider = MeterProvider(resource = resource, metric_readers = [reader])
    metrics.set_meter_provider(provider)
    self.meter = metrics.get_meter(self.service_name)
    self.logger.info(f"OpenTelemetry metrics initialized for service: {self.service_name}")

  def create_counter(self, name: str, description: str):
    return self.meter.create_counter(name = name, description = description)

  def create_histogram(self, name: str, description: str):
    return self.meter.create_histogram(name = name, description = description)
