from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .routes import todos, projects
from .models import todo, project, tag

DATABASE_URL = "postgresql://user:password@db:5432/tododb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Create database tables
# This is for demonstration purposes. In a real application, you would use Alembic for migrations.
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(todos.router)
app.include_router(projects.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
