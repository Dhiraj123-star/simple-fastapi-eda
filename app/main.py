from fastapi import FastAPI
from app.tasks import add_task

app = FastAPI(title="Simple FastAPI EDA")

@app.get("/")
def read_root():
    return {"message": "Welcome to Simple FastAPI Event-Driven Architecture!"}

@app.post("/add/{x}/{y}")
def add(x: int, y: int):
    task = add_task.delay(x, y)
    return {"task_id": task.id, "status": "Task submitted"}
