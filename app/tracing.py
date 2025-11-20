"""
OpenTelemetry Distributed Tracing
Tracks request flow through the application
"""
import logging
import socket
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME

logger = logging.getLogger(__name__)

def check_port_open(host, port, timeout=2):
    """Check if a port is open and accepting connections"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False

def init_tracing(app, db_engine):
    """
    Initialize OpenTelemetry tracing (optional - only if Tempo is available)
    """
    try:
        # Check if Tempo is running
        if not check_port_open('localhost', 4317):
            logger.info("ℹ️  Tempo not available - running without distributed tracing")
            logger.info("   To enable tracing: cd monitoring && docker-compose up -d")
            return None
        
        # Tempo is available, proceed with tracing setup
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
        from opentelemetry.instrumentation.flask import FlaskInstrumentor
        from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
        
        # Set service name
        resource = Resource(attributes={
            SERVICE_NAME: "ecommerce-app"
        })
        
        # Set up tracer provider with resource
        trace.set_tracer_provider(TracerProvider(resource=resource))
        tracer = trace.get_tracer(__name__)
        
        # Export traces to Tempo via OTLP
        otlp_exporter = OTLPSpanExporter(
            endpoint="http://localhost:4317",
            insecure=True
        )
        span_processor = SimpleSpanProcessor(otlp_exporter)
        trace.get_tracer_provider().add_span_processor(span_processor)
        
        # Instrument Flask - automatically trace all requests
        FlaskInstrumentor().instrument_app(app)
        
        # Instrument SQLAlchemy - trace database queries
        SQLAlchemyInstrumentor().instrument(engine=db_engine)
        
        logger.info("✅ OpenTelemetry tracing initialized with Tempo export")
        return tracer
        
    except ImportError as e:
        logger.info(f"ℹ️  OpenTelemetry packages not fully installed - tracing disabled: {e}")
        return None
    except Exception as e:
        logger.warning(f"⚠️  Could not initialize tracing: {e}")
        return None