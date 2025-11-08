from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .routes import todos, projects, flaky

from .database import engine, Base
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
    """Create tables, retrying if necessary for external databases.

    In testing mode (using SQLite) we create tables immediately without retries.
    """
    if os.getenv("TESTING") == "1":
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created successfully (test mode)")
        except Exception as e:
            logger.error(f"Failed to create test database tables: {e}")
            raise
        return

    for attempt in range(max_retries):
        try:
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
    "http://localhost:3001",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "*",  # Allow all origins for development
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
    service_name="mytodoapp",
    endpoint_path="/metrics",
    exclude_paths=["/metrics", "/", "/docs", "/redoc", "/openapi.json"],
)

# Include API routers
app.include_router(todos.router)
app.include_router(projects.router)
app.include_router(flaky.router)


@app.get("/")
def read_root():
    # Log messages of different levels to demonstrate Elasticsearch integration
    logger.debug("This is a debug message from the root endpoint")
    logger.info("Root endpoint accessed")
    logger.warning("This is a warning message from the root endpoint")
    return {"Hello": "World", "Logs": "Check Elasticsearch/Kibana for logs"}


@app.get("/healthz")
def health_check():
    # Log messages of different levels to demonstrate Elasticsearch integration
    logger.debug("This is a debug message from the health check endpoint")
    logger.info("Health check endpoint accessed")
    logger.warning("This is a warning message from the health check endpoint")
    return {"status": "healthy", "Logs": "Check Elasticsearch/Kibana for logs"}
