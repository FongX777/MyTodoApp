from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Get the DATABASE_URL from the environment or use the default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/mytodoapp")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def ensure_completed_at_column():
    """Ensure the todos table has completed_at column (idempotent)."""
    # Skip migration during testing
    if os.getenv("TESTING") == "1" or "pytest" in os.getenv("_", ""):
        return

    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE todos ADD COLUMN IF NOT EXISTS completed_at TIMESTAMP NULL"))
            conn.commit()
        except Exception as e:
            # Log but don't crash app startup
            print(f"[migration] Could not ensure completed_at column: {e}")


# Attempt lightweight migration on import (skip in test environment)
ensure_completed_at_column()
