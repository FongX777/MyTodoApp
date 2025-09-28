from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .routes import todos, projects
from .models import todo, project, tag
from .database import engine, SessionLocal, Base
import time
import logging

logger = logging.getLogger(__name__)


def create_tables_with_retry(max_retries=30, delay=1):
    """Try to create tables with retries to wait for database to be ready"""
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

app = FastAPI()

origins = [
    "*"  # Allow all origins for development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todos.router)
app.include_router(projects.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
