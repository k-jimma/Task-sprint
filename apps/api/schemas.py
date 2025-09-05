from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from typing import List

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str] = None
    created_at: datetime
    
    class config:
        orm_mode = True
        
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
    
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = ""
    status: Optional[str] = "todo"
    priority: Optional[str] = "medium"
    due_date: Optional[datetime] = None
    assignee: Optional[str] = None
    labels: Optional[str] = ""
    
    
class TaskCreate(TaskBase):
    title: str
    

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    assignee: Optional[str] = None
    labels: Optional[str] = None
    

class TaskOut(BaseModel):
    id: int
    user_id: int
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