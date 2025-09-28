from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .routes import todos, projects
from .models import todo, project, tag
from .database import engine, SessionLocal, Base

# Create database tables
# This is for demonstration purposes. In a real application, you would use Alembic for migrations.
Base.metadata.create_all(bind=engine)

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
