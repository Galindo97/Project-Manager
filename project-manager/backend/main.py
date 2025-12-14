from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List

import models
import schemas
import auth
from database import engine, get_db

# Crear tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:4173",
        "http://localhost:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== UTILIDAD ADMIN: MARCAR TODAS COMO COMPLETADAS ====================
@app.post("/tasks/mark_all_completed", status_code=200)
def mark_all_tasks_completed(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    """Marca todas las tareas del usuario autenticado como completadas."""
    tasks = db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()
    for task in tasks:
        task.completed = True
        task.completed_at = datetime.utcnow()
        task.status = "completed"
    db.commit()
    return {"detail": f"{len(tasks)} tareas marcadas como completadas"}
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List

import models
import schemas
import auth
from database import engine, get_db

# Crear tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:4173",
        "http://localhost:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== AUTENTICACIÓN ====================

@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Verificar si el email ya existe
    db_user = auth.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Verificar si el username ya existe
    db_user = auth.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Crear usuario
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # form_data.username contiene el email (es estándar OAuth2)
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.User)
def get_current_user_info(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

# ==================== TAREAS ====================

@app.get("/tasks", response_model=List[schemas.Task])
def get_tasks(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    """Obtener todas las tareas del usuario actual"""
    return db.query(models.Task).filter(
        models.Task.owner_id == current_user.id
    ).all()


@app.get("/tasks/completed", response_model=List[schemas.Task])
def get_completed_tasks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Obtener solo las tareas completadas del usuario actual, asegurando que 'completed' sea booleano real."""
    tasks = db.query(models.Task).filter(
        models.Task.owner_id == current_user.id,
        models.Task.completed == True
    ).all()
    # Normalizar el campo completed a booleano real
    for t in tasks:
        t.completed = bool(t.completed)
    return tasks

@app.post("/tasks", response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task: schemas.TaskCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    """Crear una nueva tarea"""
    db_task = models.Task(
        **task.dict(exclude_unset=True),
        owner_id=current_user.id,
        created_at=datetime.utcnow()
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks/{task_id}", response_model=schemas.Task)
def get_task(
    task_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    """Obtener una tarea específica"""
    task = db.query(models.Task).filter(
        models.Task.id == task_id, 
        models.Task.owner_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(
    task_id: int, 
    task_update: schemas.TaskUpdate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    """Actualizar una tarea"""
    task = db.query(models.Task).filter(
        models.Task.id == task_id, 
        models.Task.owner_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_update.dict(exclude_unset=True)
    
    # Si se marca como completada, agregar timestamp
    if "completed" in update_data and update_data["completed"]:
        update_data["completed_at"] = datetime.utcnow()
        update_data["status"] = "completed"
    elif "completed" in update_data and not update_data["completed"]:
        update_data["completed_at"] = None
        update_data["status"] = "pending"
    
    # Actualizar campos
    for key, value in update_data.items():
        setattr(task, key, value)
    
    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Eliminar una tarea"""
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return None

# ==================== PROYECTOS ====================

@app.get("/projects", response_model=List[schemas.Project])
def get_projects(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Obtener todos los proyectos del usuario actual"""  # ✅ AGREGADO
    return db.query(models.Project).filter(
        models.Project.owner_id == current_user.id
    ).all()

@app.post("/projects", response_model=schemas.Project, status_code=status.HTTP_201_CREATED)
def create_project(
    project: schemas.ProjectCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Crear un nuevo proyecto"""
    db_project = models.Project(**project.dict(), owner_id=current_user.id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.get("/projects/{project_id}", response_model=schemas.Project)
def get_project(
    project_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener un proyecto específico"""
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.put("/projects/{project_id}", response_model=schemas.Project)
def update_project(
    project_id: int,
    project_update: schemas.ProjectUpdate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Actualizar un proyecto"""
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    update_data = project_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)
    
    db.commit()
    db.refresh(project)
    return project

@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Eliminar un proyecto"""
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(project)
    db.commit()
    return None