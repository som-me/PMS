# app/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.deps import get_db, require_roles, get_current_user
from app.models import Task, Project, TaskStatusEnum
from app.schemas import TaskBase, TaskOut

router = APIRouter(prefix="/api", tags=["tasks"])


# Utility: Normalize status input to match ENUM format
def normalize_status(status: str | None) -> str:
    if not status:
        return TaskStatusEnum.todo.value
    status = status.strip().lower().replace(" ", "_")
    valid_statuses = [s.value for s in TaskStatusEnum]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status '{status}'. Must be one of {valid_statuses}",
        )
    return status


# 🟢 Create a Task (manager or admin)
@router.post("/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskBase,
    db: Session = Depends(get_db),
    _ = Depends(require_roles("manager", "admin")),  # require manager/admin
):
    if task_in.project_id is None:
        raise HTTPException(status_code=400, detail="project_id is required")

    project = db.query(Project).filter(Project.id == task_in.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    normalized_status = normalize_status(task_in.status)

    new_task = Task(
        title=task_in.title,
        description=task_in.description,
        status=normalized_status,
        due_date=task_in.due_date,
        project_id=task_in.project_id,
        assignee_id=task_in.assignee_id,
        created_at=datetime.utcnow(),
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# 🟡 Get tasks for a specific project (any authenticated user)
@router.get("/projects/{project_id}/tasks", response_model=List[TaskOut])
def get_tasks_for_project(
    project_id: int,
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    tasks = db.query(Task).filter(Task.project_id == project_id).all()
    return tasks


# 🟠 Update (edit) a task (manager or admin)
@router.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    updated_data: TaskBase,
    db: Session = Depends(get_db),
    _=Depends(require_roles("manager", "admin")),
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update fields conditionally
    if updated_data.title is not None:
        task.title = updated_data.title
    if updated_data.description is not None:
        task.description = updated_data.description
    if updated_data.status is not None:
        task.status = normalize_status(updated_data.status)
    if updated_data.due_date is not None:
        task.due_date = updated_data.due_date
    if updated_data.assignee_id is not None:
        task.assignee_id = updated_data.assignee_id
    if updated_data.project_id is not None:
        project = db.query(Project).filter(Project.id == updated_data.project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Target project not found")
        task.project_id = updated_data.project_id

    db.commit()
    db.refresh(task)
    return task
