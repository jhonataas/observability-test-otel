import logging
import os
from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler

from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor


def setup_telemetry(service_name: str):

    OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")

    resource = Resource.create({
        "service.name": service_name
    })

    # -------- TRACES --------
    trace_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(trace_provider)

    span_exporter = OTLPSpanExporter(endpoint=OTLP_ENDPOINT, insecure=True)
    trace_provider.add_span_processor(
        BatchSpanProcessor(span_exporter)
    )

    # -------- METRICS --------
    metric_exporter = OTLPMetricExporter(endpoint=OTLP_ENDPOINT, insecure=True)
    metric_reader = PeriodicExportingMetricReader(metric_exporter)

    meter_provider = MeterProvider(
        resource=resource,
        metric_readers=[metric_reader]
    )
    metrics.set_meter_provider(meter_provider)

    # -------- LOGS --------
    log_exporter = OTLPLogExporter(endpoint=OTLP_ENDPOINT, insecure=True)
    logger_provider = LoggerProvider(resource=resource)

    logger_provider.add_log_record_processor(
        BatchLogRecordProcessor(log_exporter)
    )

    handler = LoggingHandler(
        level=logging.INFO,
        logger_provider=logger_provider
    )

    logging.basicConfig(
        level=logging.INFO,
        handlers=[handler],
        format="%(message)s"
    )

    LoggingInstrumentor().instrument(set_logging_format=True)

    # -------- HTTP CLIENT --------
    HTTPXClientInstrumentor().instrument()

    return logger_provider
