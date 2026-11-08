from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sqlite3
from datetime import datetime

app = FastAPI(title="Operation SEMI Training System API", version="1.0")

# Mount the static frontend folder
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
async def read_index():
    return FileResponse("../static/index.html")

@app.get("/cbt")
async def read_cbt():
    return FileResponse("../static/cbt.html")

# Keep your existing /api/students and /api/completions routes below...

DB_NAME = "operation_semi.db"

class StudentCreate(BaseModel):
    student_id: str
    full_name: str
    clearance_level: str = "Trainee"

class CompletionCreate(BaseModel):
    student_id: str
    module_name: str
    score: float
    status: str
    workforce_hours: float = 1.5

@app.on_event("startup")
def startup_event():
    import database
    database.init_db()

@app.post("/api/students")
def register_student(student: StudentCreate):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO students (student_id, full_name, clearance_level, created_at) VALUES (?, ?, ?, ?)",
            (student.student_id, student.full_name, student.clearance_level, datetime.utcnow().isoformat())
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Student ID already exists.")
    conn.close()
    return {"message": "Student credential profile created", "student_id": student.student_id}

@app.post("/api/completions")
def log_completion(data: CompletionCreate):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM students WHERE student_id = ?", (data.student_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Student ID not found.")
        
    cursor.execute(
        """INSERT INTO completions (student_id, module_name, score, status, workforce_hours, completed_at) 
           VALUES (?, ?, ?, ?, ?, ?)""",
        (data.student_id, data.module_name, data.score, data.status, data.workforce_hours, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()
    return {"message": "Training module logged successfully", "module": data.module_name}

@app.get("/api/students/{student_id}")
def get_student_record(student_id: str):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
    student = cursor.fetchone()
    if not student:
        conn.close()
        raise HTTPException(status_code=404, detail="Student not found.")
        
    cursor.execute("SELECT module_name, score, status, workforce_hours, completed_at FROM completions WHERE student_id = ?", (student_id,))
    completions = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return {
        "student": dict(student),
        "completions": completions
    }
