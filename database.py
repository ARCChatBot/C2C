import sqlite3

DB_NAME = "operation_semi.db"

def init_db():
    #your database creation code here
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Students & Credentials table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            clearance_level TEXT DEFAULT 'Trainee',
            created_at TEXT
        )
    """)
    
    # Module completions & workforce hours tracking table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            module_name TEXT NOT NULL,
            score REAL,
            status TEXT,
            workforce_hours REAL DEFAULT 1.5,
            completed_at TEXT,
            FOREIGN KEY (student_id) REFERENCES students (student_id)
        )
    """)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Operation SEMI database initialized successfully.")