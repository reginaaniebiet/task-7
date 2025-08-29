from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db, get_session
from app.models import Student
from app.auth import authenticate_user, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
from app.crud import create_student, get_students, get_student, update_student, delete_student
from app.middleware import log_requests

from datetime import timedelta
from sqlmodel import Session

app = FastAPI()

# Init DB on startup
@app.on_event("startup")
def on_startup():
    init_db()

# Middleware for logging
app.middleware("http")(log_requests)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth token endpoint
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Create student (auth required)
@app.post("/students/", response_model=Student)
async def api_create_student(student: Student, current_user=Depends(get_current_user), session: Session = Depends(get_session)):
    return create_student(session, student)

# List students (public)
@app.get("/students/", response_model=list[Student])
async def api_get_students(session: Session = Depends(get_session)):
    return get_students(session)

# Get student by id (public)
@app.get("/students/{student_id}", response_model=Student)
async def api_get_student(student_id: int, session: Session = Depends(get_session)):
    return get_student(session, student_id)

# Update student (auth required)
@app.put("/students/{student_id}", response_model=Student)
async def api_update_student(student_id: int, student: Student, current_user=Depends(get_current_user), session: Session = Depends(get_session)):
    return update_student(session, student_id, student)

# Delete student (auth required)
@app.delete("/students/{student_id}")
async def api_delete_student(student_id: int, current_user=Depends(get_current_user), session: Session = Depends(get_session)):
    delete_student(session, student_id)
    return {"detail": "Student deleted"}
