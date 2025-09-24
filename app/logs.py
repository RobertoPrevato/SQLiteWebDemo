import logging
import logging.handlers
import os
import sys
from pathlib import Path

from blacksheep.server.otel.otlp import use_open_telemetry
from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader


def _configure_otlp(app, logger):
    otel_exporter_otlp_endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")

    if otel_exporter_otlp_endpoint is None:
        return

    if "OTEL_RESOURCE_ATTRIBUTES" not in os.environ:
        os.environ["OTEL_RESOURCE_ATTRIBUTES"] = (
            "service.name=fortunecookies,service.namespace=fortunecookies,"
            "deployment.environment=production"
        )

    logger.info("Configuring OTLP Exporters…")
    use_open_telemetry(app, OTLPLogExporter(), OTLPSpanExporter())

    # For the sake of the OTEL example, configure also a Metric Exporter.
    # Set up the OTLP exporter to send to your collector (default localhost:4317)
    exporter = OTLPMetricExporter(insecure=True)
    reader = PeriodicExportingMetricReader(exporter, export_interval_millis=5000)
    provider = MeterProvider(metric_readers=[reader])
    metrics.set_meter_provider(provider)

    # The following is just an example to collect metrics and
    # test sending metrics to the OTLP endpoint:
    meter = metrics.get_meter(__name__)
    request_counter = meter.create_counter(
        name="otel_web_requests",
        description="Requests count",
        unit="1",
    )

    async def req_count_middleware(request, handler):
        request_counter.add(1, {"endpoint": request.route})
        return await handler(request)

    app.middlewares.append(req_count_middleware)


def configure_logging(app):
    """
    Configures a logger named 'app' that writes to a log file.

    If OTEL_EXPORTER_OTLP_ENDPOINT env variable is set, it configures OpenTelemetry
    logs using the OTLP protocol.
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Create logger
    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)

    # Create file handler with rotation
    log_file = log_dir / "app.log"
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
    )

    # Create stdout handler for info and warnings
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    stdout_handler.addFilter(lambda record: record.levelno < logging.ERROR)

    # Create stderr handler for errors and exceptions only
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    stdout_handler.setFormatter(formatter)
    stderr_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)

    # Try configurin OTLP exporter
    _configure_otlp(app, logger)

    return logger
