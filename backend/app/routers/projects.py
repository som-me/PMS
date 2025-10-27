from fastapi import APIRouter, Depends
from typing import List
from app.deps import get_db, require_roles, get_current_user
from sqlalchemy.orm import Session
from app import crud
from app.schemas import ProjectBase, ProjectOut, UserOut

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.get("/", response_model=List[ProjectOut])
def read_projects(db: Session = Depends(get_db), user = Depends(get_current_user)):
    return crud.list_projects(db)

@router.post("/", response_model=ProjectOut)
def create_project(project: ProjectBase, db: Session = Depends(get_db), user = Depends(require_roles("manager", "admin"))):
    return crud.create_project(db, project.name, project.description, project.member_ids)
