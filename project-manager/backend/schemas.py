from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str  # ✅ AGREGADO

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Project Schemas
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: str = "activo"

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class Project(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Task Schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    status: str = "pending"
    category: Optional[str] = None
    due_date: Optional[datetime] = None
    project_id: Optional[int] = None
    notes: Optional[str] = None  # ✅ AGREGADO
    progress: Optional[int] = 0  # ✅ AGREGADO
    critical_points: Optional[str] = None  # ✅ AGREGADO

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    category: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: Optional[bool] = None
    project_id: Optional[int] = None
    notes: Optional[str] = None  # ✅ AGREGADO
    progress: Optional[int] = None  # ✅ AGREGADO
    critical_points: Optional[str] = None  # ✅ AGREGADO

class Task(TaskBase):
    id: int
    completed: bool
    completed_at: Optional[datetime] = None
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True