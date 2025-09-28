from fastapi import APIRouter, Depends
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
    return repository.project_repo.create_project(db=db, project=project)

@router.get("/projects", response_model=list[Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = repository.project_repo.get_projects(db, skip=skip, limit=limit)
    return projects

@router.get("/projects/{project_id}", response_model=Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = repository.project_repo.get_project(db, project_id=project_id)
    return db_project

@router.put("/projects/{project_id}", response_model=Project)
def update_project_endpoint(project_id: int, project: ProjectCreate, db: Session = Depends(get_db)):
    return repository.project_repo.update_project(db=db, project_id=project_id, project=project)
