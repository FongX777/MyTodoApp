import os

# Ensure tests run in isolated SQLite database
os.environ.setdefault("TESTING", "1")
# Allow overriding via environment; if not provided force sqlite file DB
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
