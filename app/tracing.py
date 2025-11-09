"""
OpenTelemetry Distributed Tracing
Tracks request flow through the application
"""
import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

logger = logging.getLogger(__name__)

def init_tracing(app, db_engine):
    """
    Initialize OpenTelemetry tracing
    """
    try:
        # Set up tracer provider
        trace.set_tracer_provider(TracerProvider())
        tracer = trace.get_tracer(__name__)
        
        # Export traces to console (for now)
        span_processor = SimpleSpanProcessor(ConsoleSpanExporter())
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