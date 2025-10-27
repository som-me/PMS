from sqlalchemy.orm import Session
from app import models
from passlib.context import CryptContext
from typing import List, Optional
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- User CRUD ---

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, name: str, email: str, password: str, role: str):
    hashed = pwd_context.hash(password)
    user = models.User(name=name, email=email, hashed_password=hashed, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# --- Project CRUD ---

def create_project(db: Session, name: str, description: str, member_ids: List[int] = []):
    project = models.Project(name=name, description=description)
    if member_ids:
        users = db.query(models.User).filter(models.User.id.in_(member_ids)).all()
        project.members = users
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

def list_projects(db: Session):
    return db.query(models.Project).all()

# --- Task CRUD ---

def create_task(
    db: Session, 
    title: str, 
    description: str | None, 
    status: str, 
    due_date: datetime | None, 
    assignee_id: int | None, 
    project_id: int | None
) -> models.Task:
    """Creates a new Task record in the database."""
    db_task = models.Task(
        title=title,
        description=description,
        status=status,
        due_date=due_date,
        assignee_id=assignee_id,
        project_id=project_id,
        # Note: This requires the 'created_at' column in the tasks table to exist.
        created_at=datetime.utcnow() 
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def list_tasks(db: Session, project_id: int | None = None) -> list[models.Task]:
    """Retrieves all tasks, optionally filtered by project ID."""
    query = db.query(models.Task)
    if project_id is not None:
        query = query.filter(models.Task.project_id == project_id)
    return query.all()
