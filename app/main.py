from fastapi import FastAPI
from app.tasks import add_task,celery_app
from celery.result import AsyncResult
from sqlalchemy import create_engine,MetaData,Table,select
import pickle

app = FastAPI(title="Simple FastAPI EDA")

@app.get("/")
def read_root():
    return {"message": "Welcome to Simple FastAPI Event-Driven Architecture!"}

@app.post("/add/{x}/{y}")
def add(x: int, y: int):
    task = add_task.delay(x, y)
    return {"task_id": task.id, "status": "Task submitted"}


@app.get("/result/{task_id}")
def get_result(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None
    }

@app.get("/history")
def get_history():
    engine = create_engine("sqlite:///results.sqlite3")
    metadata = MetaData()
    metadata.reflect(bind=engine)  # Reflect tables from DB

    taskmeta = metadata.tables["celery_taskmeta"]

    with engine.connect() as conn:
        query = select(taskmeta).order_by(taskmeta.c.date_done.desc())
        rows = conn.execute(query).fetchall()

    history = []
    for row in rows:
        try:
            result = pickle.loads(row.result) if row.result else None
        except Exception:
            result = str(row.result)  # fallback

        history.append({
            "task_id": row.task_id,
            "status": row.status,
            "result": result,
            "date_done": row.date_done.isoformat() if row.date_done else None
        })

    return history
