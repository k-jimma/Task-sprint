from sqlalchemy import column, Integer, String, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .database import Base

class TaskStatus(str, enum.Enum):
    todo = "todo"
    doing = "doing"
    done = "done"

class TaskPriority(str, enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"
    
class User(Base):
    __tablename__ = "users"

    id = column(Integer, primary_key=True, index=True)
    email = column(String, unique=True, index=True, nullable=False)
    password_hash = column(String, nullable=False)
    name = column(String, nullable=True)
    created_at = column(DateTime, default=datetime.utcnow)

    tasks = relationship("Task", back_populates="owner")


class Task(Base):
    __tablename__ = "tasks"

    id = column(Integer, primary_key=True, index=True)
    user_id = column(Integer, ForeignKey("users.id"), nullable=False)
    title = column(String, nullable=False)
    description = column(Text, default="")
    status = column(Enum(TaskStatus), default=TaskStatus.todo, nullable=False)
    priority = column(Enum(TaskPriority), default=TaskPriority.medium, nullable=False)
    due_date = column(DateTime, nullable=True)
    assignee = column(String, nullable=True)
    labels = column(String, default="")
    created_at = column(DateTime, default=datetime.utcnow)
    updated_at = column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="tasks")
