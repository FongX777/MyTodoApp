from sqlalchemy.orm import Session
from ..models.project import Project

def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()

def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Project).offset(skip).limit(limit).all()

def create_project(db: Session, project: Project):
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

def update_project(db: Session, project_id: int, project: Project):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    db_project.name = project.name
    db_project.status = project.status
    db.commit()
    db.refresh(db_project)
    return db_project
