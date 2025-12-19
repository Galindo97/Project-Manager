from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
import shutil
import os

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel

# Crear la app antes de usarla

from fastapi.staticfiles import StaticFiles
app = FastAPI()

UPLOAD_DIR = "uploads"
app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")
# ==================== ENDPOINT PARA SUBIR ARCHIVOS ====================
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel
import os

# Importar Gemini
import google.generativeai as genai

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
        "http://localhost:5174",
        "https://br03lvnr-5173.usw3.devtunnels.ms"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== CONFIGURAR GEMINI ====================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    print("✅ Gemini API configurada correctamente")
else:
    print("⚠️ GEMINI_API_KEY no encontrada. El chat con IA no funcionará.")

# ==================== MODELOS PARA CHAT ====================
class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[dict]] = []

class ChatResponse(BaseModel):
    response: str
    model_used: str

# ==================== AUTENTICACIÓN ====================

@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = auth.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = auth.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
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
    return db.query(models.Task).filter(
        models.Task.owner_id == current_user.id
    ).all()

@app.get("/tasks/completed", response_model=List[schemas.Task])
def get_completed_tasks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    tasks = db.query(models.Task).filter(
        models.Task.owner_id == current_user.id,
        models.Task.completed == True
    ).all()
    for t in tasks:
        t.completed = bool(t.completed)
    return tasks

@app.post("/tasks", response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task: schemas.TaskCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
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
    print(f"🔎 Buscando tarea con id={task_id} para usuario id={current_user.id} ({current_user.username})")
    task = db.query(models.Task).filter(
        models.Task.id == task_id, 
        models.Task.owner_id == current_user.id
    ).first()
    if not task:
        print(f"❌ Tarea no encontrada o no pertenece al usuario. id={task_id}, usuario={current_user.username}")
        raise HTTPException(status_code=404, detail="Task not found")
    print(f"✅ Tarea encontrada: {task.title} (id={task.id}) para usuario {current_user.username}")
    return task

@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(
    task_id: int, 
    task_update: schemas.TaskUpdate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id, 
        models.Task.owner_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_update.dict(exclude_unset=True)
    
    if "completed" in update_data and update_data["completed"]:
        update_data["completed_at"] = datetime.utcnow()
        update_data["status"] = "completed"
    elif "completed" in update_data and not update_data["completed"]:
        update_data["completed_at"] = None
        update_data["status"] = "pending"
    
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
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return None

@app.post("/tasks/mark_all_completed", status_code=200)
def mark_all_tasks_completed(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    tasks = db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()
    for task in tasks:
        task.completed = True
        task.completed_at = datetime.utcnow()
        task.status = "completed"
    db.commit()
    return {"detail": f"{len(tasks)} tareas marcadas como completadas"}

# ==================== PROYECTOS ====================

@app.get("/projects", response_model=List[schemas.Project])
def get_projects(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return db.query(models.Project).filter(
        models.Project.owner_id == current_user.id
    ).all()

@app.post("/projects", response_model=schemas.Project, status_code=status.HTTP_201_CREATED)
def create_project(
    project: schemas.ProjectCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
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
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(project)
    db.commit()
    return None

# ==================== CHAT CON IA (GEMINI) ====================

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(
    chat_request: ChatRequest,
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Endpoint de chat con IA usando Gemini.
    Requiere autenticación.
    """
    try:
        if not GEMINI_API_KEY:
            raise HTTPException(
                status_code=503,
                detail="El servicio de IA no está disponible. Contacta al administrador."
            )
        
        # Inicializar modelo
        model = genai.GenerativeModel('gemini-pro')
        
        # Construir contexto con historial de conversación
        conversation_context = f"Eres un asistente de gestión de proyectos y tareas para el usuario {current_user.username}.\n\n"
        
        if chat_request.conversation_history:
            for msg in chat_request.conversation_history[-5:]:  # Últimos 5 mensajes
                role = msg.get("role", "user")
                content = msg.get("content", "")
                conversation_context += f"{role}: {content}\n"
        
        # Prompt completo
        full_prompt = f"{conversation_context}user: {chat_request.message}\n\nassistant:"
        
        # Generar respuesta
        response = model.generate_content(full_prompt)
        
        return ChatResponse(
            response=response.text,
            model_used="gemini-pro"
        )
        
    except Exception as e:
        print(f"❌ Error en chat: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar tu mensaje: {str(e)}"
        )