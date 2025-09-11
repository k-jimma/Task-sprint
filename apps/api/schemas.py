from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from .models import TaskStatus, TaskPriority

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
        
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=120)
    description: Optional[str] = Field("", max_length=2000)
    status: Optional[TaskStatus] = TaskStatus.todo
    priority: Optional[TaskPriority] = TaskPriority.medium
    due_date: Optional[datetime] = None
    assignee: Optional[str] = Field(None, max_length=120)
    labels: Optional[str] = Field("", max_length=240)


class TaskCreate(TaskBase):
    title: str = Field(..., min_length=1, max_length=120)


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=120)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    assignee: Optional[str] = Field(None, max_length=120)
    labels: Optional[str] = Field(None, max_length=240)

class TaskOut(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    status: str
    priority: str
    due_date: Optional[datetime]
    assignee: Optional[str]
    labels: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        