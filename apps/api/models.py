from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text, Index, UniqueConstraint
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

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    tasks = relationship("Task", back_populates="owner")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(120), nullable=False, index=True)
    description = Column(Text, default="")
    status = Column(Enum(TaskStatus), default=TaskStatus.todo, nullable=False, index=True)
    priority = Column(Enum(TaskPriority), default=TaskPriority.medium, nullable=False, index=True)
    due_date = Column(DateTime, nullable=True, index=True)
    assignee = Column(String(120), nullable=True)
    labels = Column(String(240), default="")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    owner = relationship("User", back_populates="tasks")
    
    
    __table_args__ = (
        # 旧: Index(...) → 新: UniqueConstraint で重複禁止をDBでも保証
        UniqueConstraint("user_id", "title", name="uq_tasks_user_title"),
        # 必要なら検索性能用の追加Indexも残せます
        Index("ix_tasks_user_created_at", "user_id", "created_at"),
    )
