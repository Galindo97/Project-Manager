from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)  # ✅ AGREGADO
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="activo")  # activo, completado, archivado
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String, default="medium")  # low, medium, high
    status = Column(String, default="pending")  # pending, completed
    category = Column(String, nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Campos adicionales para la vista de detalle
    notes = Column(Text, nullable=True)  # JSON string de notas
    progress = Column(Integer, default=0)  # Progreso 0-100
    critical_points = Column(Text, nullable=True)  # JSON string de puntos críticos
    
    # Relationships
    owner = relationship("User", back_populates="tasks")
    project = relationship("Project", back_populates="tasks")