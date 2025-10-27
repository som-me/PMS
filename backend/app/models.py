from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base import Base
from sqlalchemy import Table

class RoleEnum(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    developer = "developer"

project_members = Table(
    'project_members', Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    email = Column(String(256), unique=True, index=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.developer)
    created_at = Column(DateTime, default=datetime.utcnow)

    tasks = relationship("Task", back_populates="assignee")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    members = relationship("User", secondary=project_members, backref="projects")

class TaskStatusEnum(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatusEnum), default=TaskStatusEnum.todo)
    due_date = Column(DateTime, nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    assignee = relationship("User", back_populates="tasks")
