import os
import sqlite3
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Establish absolute paths so files and database are always found
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "operation_semi.db")

app = FastAPI(title="Operation SEMI Training System API", version="1.0")

# Enable CORS for cross-origin requests from your GitHub Pages frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files correctly from the current directory
app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Ensure your tables exist to prevent 500 errors on startup
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS training_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            score REAL,
            track TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

class StudentRegister(BaseModel):
    student_id: str
    full_name: str

class TrainingCompletion(BaseModel):
    student_id: str
    score: float
    track: str

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/cbt")
async def read_cbt():
    return FileResponse(os.path.join(BASE_DIR, "cbt.html"))

@app.get("/api/students")
async def get_students():
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        students = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return students
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/register")
async def register_student(student: StudentRegister):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO students (student_id, full_name) VALUES (?, ?)", 
            (student.student_id, student.full_name)
        )
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Student registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/complete-training")
async def complete_training(data: TrainingCompletion):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO training_logs (student_id, score, track) VALUES (?, ?, ?)", 
            (data.student_id, data.score, data.track)
        )
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Training progress logged"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
