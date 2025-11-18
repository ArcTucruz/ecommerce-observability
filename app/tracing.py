"""
OpenTelemetry Distributed Tracing
Tracks request flow through the application
"""
import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

logger = logging.getLogger(__name__)

def init_tracing(app, db_engine):
    """
    Initialize OpenTelemetry tracing
    """
    try:
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
        
        logger.info("✅ OpenTelemetry tracing initialized")
        return tracer
        
    except Exception as e:
        logger.warning(f"⚠️ Could not initialize tracing: {e}")
        return None
