"""Database setup utilities.

During tests we want to avoid connecting to the external Postgres service
named 'db'. Instead we force a local SQLite database unless a custom
DATABASE_URL is explicitly provided. This keeps tests self-contained and
fast while production/dev continue to use Postgres.
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
import os


def _select_database_url() -> str:
    """Determine the effective database URL.

    Priority:
    1. Explicit DATABASE_URL env var (always respected if not default docker hostname)
    2. Testing mode -> force sqlite file (unless DATABASE_URL already overridden)
    3. Fallback to default Postgres service hostname for compose
    """
    env_url = os.getenv("DATABASE_URL")
    if os.getenv("TESTING") == "1":
        # If user did not override or they kept the docker default, use sqlite for tests
        if not env_url or env_url.startswith("postgresql://postgres:postgres@db"):
            return "sqlite:///./test.db"
        return env_url
    return env_url or "postgresql://postgres:postgres@db:5432/mytodoapp"


DATABASE_URL = _select_database_url()

# Provide SQLite specific connect_args
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},  # Needed for FastAPI TestClient multithreading
    )
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def ensure_completed_at_column():
    """Ensure the todos table has completed_at column (idempotent) for Postgres.

    Skipped for testing (SQLite) because schema is created from models directly.
    """
    if os.getenv("TESTING") == "1" or DATABASE_URL.startswith("sqlite"):
        return

    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE todos ADD COLUMN IF NOT EXISTS completed_at TIMESTAMP NULL"))
            conn.commit()
        except Exception as e:
            # Log but don't crash app startup
            print(f"[migration] Could not ensure completed_at column: {e}")


# Attempt lightweight migration on import (skip in test mode / sqlite)
ensure_completed_at_column()
