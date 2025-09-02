from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

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
    
class loginRequest(BaseModel):
    email: EmailStr
    password: str
    