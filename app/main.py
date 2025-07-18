from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from .tasks import add_task, celery_app
from celery.result import AsyncResult
from sqlalchemy import create_engine, MetaData, Table, select
import pickle
from jose import jwt
import datetime
import sqlite3
import os
from dotenv import load_dotenv
import os

load_dotenv()

# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

app = FastAPI(title="Simple FastAPI EDA")

security = HTTPBearer()

# === In-memory DB setup (or use SQLite persistent storage) ===
DB_PATH = os.getenv("DB_PATH", "users.sqlite3")
if not os.path.exists(DB_PATH):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL
            );
        """)


# === Models ===
class User(BaseModel):
    username: str
    password: str


# === Authentication Utils ===
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


# === Routes ===
@app.get("/")
def read_root():
    return {"message": "Welcome to Simple FastAPI Event-Driven Architecture!"}


@app.post("/register")
def register(user: User):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Username already exists")
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, user.password))
        conn.commit()
    return {"message": "User registered successfully"}


@app.post("/token")
def generate_token(user: User):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (user.username, user.password))
        if not cursor.fetchone():
            raise HTTPException(status_code=401, detail="Invalid username or password")

    payload = {
        "sub": user.username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token}


@app.post("/add/{x}/{y}")
def add(x: int, y: int, user=Depends(verify_token)):
    task = add_task.delay(x, y)
    return {"task_id": task.id, "status": "Task submitted"}


@app.get("/result/{task_id}")
def get_result(task_id: str, user=Depends(verify_token)):
    result = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None
    }


@app.get("/history")
def get_history(user=Depends(verify_token)):
    engine = create_engine("sqlite:///results.sqlite3")
    metadata = MetaData()
    metadata.reflect(bind=engine)

    taskmeta = metadata.tables["celery_taskmeta"]

    with engine.connect() as conn:
        query = select(taskmeta).order_by(taskmeta.c.date_done.desc())
        rows = conn.execute(query).fetchall()

    history = []
    for row in rows:
        try:
            result = pickle.loads(row.result) if row.result else None
        except Exception:
            result = str(row.result)

        history.append({
            "task_id": row.task_id,
            "status": row.status,
            "result": result,
            "date_done": row.date_done.isoformat() if row.date_done else None
        })

    return history
