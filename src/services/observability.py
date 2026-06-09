import logging


from logging import Logger
from fastapi import FastAPI
from opentelemetry import metrics, trace
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.psycopg import PsycopgInstrumentor
from opentelemetry.instrumentation.botocore import BotocoreInstrumentor
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry._logs import set_logger_provider
from opentelemetry.instrumentation.logging.handler import LoggingHandler
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from constants import OTEL_METRIC_EXPORT_INTERVAL_MILLIS, OTEL_SERVICE_NAME, LOGGER_NAME


class ObservabilityService():
  def __init__(self, otlp_endpoint: str, env: str, logger: Logger):
    self.service_name = OTEL_SERVICE_NAME
    self.otlp_endpoint = otlp_endpoint
    self.env = env
    self.logger = logger

  def setup(self, app: FastAPI) -> None:
    resource = Resource(attributes = {"service.name": self.service_name, "deployment.environment": self.env})
    self.setup_metrics(resource)
    self.setup_logs(resource)
    self.setup_traces(resource)
    self.setup_instrumentors(app)
    self.logger.info("Observability service setup complete")

  def setup_logs(self, resource: Resource) -> None:
    exporter = OTLPLogExporter(endpoint = f"{self.otlp_endpoint}/v1/logs")
    provider = LoggerProvider(resource = resource)
    provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
    set_logger_provider(provider)
    handler = LoggingHandler(level = logging.NOTSET, logger_provider = provider, log_code_attributes = True)
    for name in [LOGGER_NAME, "uvicorn", "fastapi"]:
      logging.getLogger(name).addHandler(handler)
    self.logger.info("OpenTelemetry log export initialized")

  def setup_instrumentors(self, app: FastAPI) -> None:
    FastAPIInstrumentor.instrument_app(app)
    self.logger.info("FastAPI instrumented with OpenTelemetry")
    PsycopgInstrumentor().instrument(enable_commenter = True, capture_parameters = True)
    self.logger.info("Psycopg instrumented with OpenTelemetry")
    BotocoreInstrumentor().instrument()
    self.logger.info("Botocore instrumented with OpenTelemetry")

  def setup_traces(self, resource: Resource) -> None:
    exporter = OTLPSpanExporter(endpoint = f"{self.otlp_endpoint}/v1/traces")
    provider = TracerProvider(resource = resource)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    self.logger.info("OpenTelemetry trace export initialized")

  def setup_metrics(self, resource: Resource) -> None:
    exporter = OTLPMetricExporter(endpoint = f"{self.otlp_endpoint}/v1/metrics")
    reader = PeriodicExportingMetricReader(exporter, export_interval_millis = OTEL_METRIC_EXPORT_INTERVAL_MILLIS)
    provider = MeterProvider(resource = resource, metric_readers = [reader])
    metrics.set_meter_provider(provider)
    self.meter = metrics.get_meter(self.service_name)
    self.logger.info(f"OpenTelemetry metrics initialized for service: {self.service_name}")

  def create_counter(self, name: str, description: str):
    return self.meter.create_counter(name = name, description = description)

  def create_histogram(self, name: str, description: str):
    return self.meter.create_histogram(name = name, description = description)
