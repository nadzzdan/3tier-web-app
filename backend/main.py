from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import os
import time
from dotenv import load_dotenv

# Load environment variables test
load_dotenv()

app = FastAPI()

# CORS configuration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:8080").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "example")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "textsdb")

# App configuration
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8000"))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

def get_db():
    """Attempt to connect to the database with retries"""
    max_retries = 10
    for attempt in range(max_retries):
        try:
            conn = mysql.connector.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DATABASE
            )
            return conn
        except mysql.connector.Error as e:
            print(f"[DB] Connection attempt {attempt+1}/{max_retries} failed: {e}")
            time.sleep(3)
    raise RuntimeError("Failed to connect to MySQL after multiple attempts")

def init_db():
    """Initialize the database and table"""
    max_retries = 10
    for attempt in range(max_retries):
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS texts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    text TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            cursor.close()
            conn.close()
            print("[DB] Database initialized successfully")
            return
        except Exception as e:
            print(f"[DB] Initialization attempt {attempt+1}/{max_retries} failed: {e}")
            time.sleep(3)
    raise RuntimeError("Failed to initialize database after multiple attempts")

# Initialize DB on startup - make it non-blocking
try:
    init_db()
except Exception as e:
    print(f"[WARNING] Database initialization failed: {e}")
    print("[INFO] Application will start but database features may not work")

@app.get("/")
async def root():
    return {
        "message": "🚀 3-Tier Web App Backend v2.0",
        "version": "2.0",
        "status": "running",
        "timestamp": time.time(),
        "features": ["CI/CD Pipeline", "Docker Hub Integration", "Modern UI"]
    }

@app.post("/submit")
async def submit_text(request: Request):
    data = await request.json()
    text = data.get('text')
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO texts (text) VALUES (%s)', (text,))
    conn.commit()
    cursor.close()
    conn.close()
    return {
        "status": "success",
        "message": "✅ Text saved successfully!",
        "version": "2.0",
        "timestamp": time.time()
    }

@app.get("/texts")
async def get_texts():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM texts ORDER BY id DESC')
    texts = cursor.fetchall()
    cursor.close()
    conn.close()
    return texts

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": time.time()}

# Add this at the end of the file
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)
