from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Get CORS origins from environment variable
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:8080").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load database configuration from environment variables
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "example")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "textsdb")

# Load application configuration
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8000"))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

def get_db():
    # Add retry logic for database connection
    max_retries = 5
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
            if attempt == max_retries - 1:
                raise e
            time.sleep(2)
    return None

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
    if text:
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
    raise HTTPException(status_code=400, detail="No text provided")

@app.get("/texts")
async def get_texts():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM texts ORDER BY id DESC')
    texts = cursor.fetchall()
    cursor.close()
    conn.close()
    return texts

def init_db():
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
            print("Database initialized successfully")
            break
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Failed to initialize database: {e}")
                raise e
            print(f"Database connection attempt {attempt + 1} failed, retrying...")
            time.sleep(3)

# Initialize database on startup
init_db()