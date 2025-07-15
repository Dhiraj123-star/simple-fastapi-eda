from celery import Celery

celery_app = Celery(
    "simple_fastapi_eda",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)

@celery_app.task
def add_task(x: int, y: int) -> int:
    print(f"[Worker] Adding {x} + {y}")
    return x + y
