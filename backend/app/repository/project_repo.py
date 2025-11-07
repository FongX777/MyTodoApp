from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.project import Project
from ..schemas.project import ProjectCreate


def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Project).offset(skip).limit(limit).all()


def create_project(db: Session, project: ProjectCreate):
    db_project = Project(name=project.name, description=project.description, status=project.status)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(db: Session, project_id: int, project: ProjectCreate):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    db_project.name = project.name  # type: ignore[assignment]
    db_project.description = project.description  # type: ignore[assignment]
    db_project.status = project.status  # type: ignore[assignment]
    db.commit()
    db.refresh(db_project)
    return db_project
