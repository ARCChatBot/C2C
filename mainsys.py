import os
import sqlite3
import csv
import io
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "operation_semi.db")

app = FastAPI(title="Operation SEMI Training System API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
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

@app.get("/admin")
async def read_admin():
    return FileResponse(os.path.join(BASE_DIR, "admin.html"))

@app.get("/api/students")
async def get_students():
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students ORDER BY timestamp DESC")
        students = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return students
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/training-logs")
async def get_training_logs():
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.id, t.student_id, 
                   COALESCE(s.full_name, 'Trainee') AS full_name, 
                   t.score, t.track, t.timestamp 
            FROM training_logs t
            LEFT JOIN students s ON t.student_id = s.student_id
            ORDER BY t.timestamp DESC
        ''')
        logs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return logs
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

@app.get("/api/export-csv")
async def export_csv():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT t.id, t.student_id, COALESCE(s.full_name, 'Trainee') AS full_name, t.score, t.track, t.timestamp 
        FROM training_logs t
        LEFT JOIN students s ON t.student_id = s.student_id
        ORDER BY t.timestamp DESC
    ''')
    rows = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Log ID", "Student ID", "Full Name", "Score", "Track / Scheduling Details", "Timestamp"])
    for row in rows:
        writer.writerow(row)
    
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=operation_semi_telemetry.csv"}
    )
