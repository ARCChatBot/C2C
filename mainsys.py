import os
import sqlite3
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Establish absolute paths so files and database are always found
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "operation_semi.db")

app = FastAPI(title="Operation SEMI Training System API", version="1.0")

# Mount static files correctly from the current directory
app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Ensure your tables exist to prevent 500 errors on startup
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

class StudentCreate(BaseModel):
    name: str
    email: str

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/cbt")
async def read_cbt():
    return FileResponse(os.path.join(BASE_DIR, "cbt.html"))

@app.get("/api/students")
async def get_students():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return students

@app.post("/api/students")
async def create_student(student: StudentCreate):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, email) VALUES (?, ?)", (student.name, student.email))
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Student added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
