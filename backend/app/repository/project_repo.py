from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException
from ..models.project import Project
from ..schemas.project import ProjectCreate, ProjectStatus


def _normalize_status(status: ProjectStatus | None) -> str | None:
    """Map API/status values to DB enum values."""
    if status is None:
        return None
    mapping = {
        ProjectStatus.undone: "active",
        ProjectStatus.done: "completed",
        ProjectStatus.cancelled: "cancelled",
    }
    return mapping.get(status, "active")


def _migrate_legacy_statuses(db: Session):
    """Convert any lingering 'undone'/'done' values to new DB enum values.

    Safe to run each request; will no-op when values already migrated.
    """
    try:
        db.execute(text("UPDATE projects SET status='active' WHERE status='undone'"))
        db.execute(text("UPDATE projects SET status='completed' WHERE status='done'"))
        db.commit()
    except Exception:
        db.rollback()


def get_project(db: Session, project_id: int):
    _migrate_legacy_statuses(db)
    return db.query(Project).filter(Project.id == project_id).first()


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    _migrate_legacy_statuses(db)
    return db.query(Project).offset(skip).limit(limit).all()


def create_project(db: Session, project: ProjectCreate):
    db_project = Project(
        name=project.name,
        description=project.description,
        status=_normalize_status(project.status) or "active",
    )
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
    db_project.status = _normalize_status(project.status) or db_project.status  # type: ignore[assignment]
    db.commit()
    db.refresh(db_project)
    return db_project
