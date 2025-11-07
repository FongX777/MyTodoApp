from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import repository
from ..database import SessionLocal
from ..schemas.project import Project, ProjectCreate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/projects", response_model=Project)
def create_project_endpoint(project: ProjectCreate, db: Session = Depends(get_db)):
    """
    Create a new project.

    - **name**: Name of the project (required)
    - **description**: Project description
    - **status**: Project status (active, archived)

    Projects are used to organize todos.
    """
    return repository.project_repo.create_project(db=db, project=project)


@router.get("/projects", response_model=list[Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all projects with optional pagination.

    - **skip**: Number of projects to skip (default: 0)
    - **limit**: Maximum number of projects to return (default: 100)

    Returns a list of all projects.
    """
    projects = repository.project_repo.get_projects(db, skip=skip, limit=limit)
    return projects


@router.get("/projects/{project_id}", response_model=Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific project by ID.

    - **project_id**: The ID of the project to retrieve

    Returns the project if found, otherwise raises 404.
    """
    db_project = repository.project_repo.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@router.put("/projects/{project_id}", response_model=Project)
def update_project_endpoint(project_id: int, project: ProjectCreate, db: Session = Depends(get_db)):
    """
    Update an existing project.

    - **project_id**: The ID of the project to update
    - **project**: Updated project data

    Returns the updated project if found, otherwise raises 404.
    """
    return repository.project_repo.update_project(db=db, project_id=project_id, project=project)
