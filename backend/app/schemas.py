from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    manager = "manager"
    developer = "developer"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[RoleEnum] = RoleEnum.developer

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: RoleEnum

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None
    role: Optional[RoleEnum] = None

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    member_ids: Optional[List[int]] = []

class ProjectOut(ProjectBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "todo"
    due_date: Optional[datetime] = None
    assignee_id: Optional[int] = None
    project_id: Optional[int] = None

class TaskOut(TaskBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
