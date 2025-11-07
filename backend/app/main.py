from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .routes import todos, projects
from .models import todo, project, tag
from .database import engine, SessionLocal, Base
from .middleware.request_id import add_request_id_middleware
from .metrics import setup_metrics
from .logging_config import setup_logging, setup_request_logging
import time
import logging
import os

# Initialize structured logging
setup_logging(service_name="mytodoapp-api")
logger = logging.getLogger(__name__)


def create_tables_with_retry(max_retries=30, delay=1):
    """Try to create tables with retries to wait for database to be ready"""
    # Skip database setup during testing
    if os.getenv("TESTING") == "1":
        logger.info("Skipping database setup in test mode")
        return

    for attempt in range(max_retries):
        try:
            # Create database tables
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created successfully")
            return
        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"Database not ready (attempt {attempt + 1}/{max_retries}): {e}")
                time.sleep(delay)
            else:
                logger.error(f"Failed to create database tables after {max_retries} attempts: {e}")
                raise


# Create database tables with retry logic
create_tables_with_retry()

app = FastAPI(
    title="MyTodoApp API",
    description="""
    A modern todo list application API with project management capabilities.
    
    ## Features
    
    * **Todos**: Create, read, update, and delete todo items
    * **Projects**: Organize todos into projects
    * **Ordering**: Reorder todos within projects via drag-and-drop
    * **Scheduling**: Set deadlines and scheduled dates for todos
    * **Priority Management**: Assign priority levels (low, medium, high)
    * **Status Tracking**: Track todo completion status
    
    ## Observability
    
    * Prometheus metrics available at `/metrics`
    * Structured JSON logging to Elasticsearch
    * Request tracing with X-Request-ID headers
    """,
    version="1.0.0",
    contact={
        "name": "MyTodoApp Team",
        "email": "support@mytodoapp.com",
    },
    license_info={
        "name": "MIT",
    },
)

origins = [
    "*"  # Allow all origins for development
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request_id middleware (must come before request logging)
add_request_id_middleware(app)

# Add request logging middleware
setup_request_logging(app)

# Setup Prometheus metrics endpoint and middleware
setup_metrics(
    app,
    service_name="mytodoapp-api",
    endpoint_path="/metrics",
    exclude_paths=["/metrics", "/", "/docs", "/redoc", "/openapi.json"],
)

# Include API routers
app.include_router(todos.router)
app.include_router(projects.router)


@app.get("/")
def read_root():
    # Log messages of different levels to demonstrate Elasticsearch integration
    logger.debug("This is a debug message from the root endpoint")
    logger.info("Root endpoint accessed")
    logger.warning("This is a warning message from the root endpoint")

    # Every 5th request will generate an error log
    import random

    if random.random() < 0.2:
        try:
            # Intentionally cause an error for demonstration
            1 / 0
        except Exception as e:
            logger.error(f"Simulated error in root endpoint: {str(e)}")

    return {"Hello": "World", "Logs": "Check Elasticsearch/Kibana for logs"}
