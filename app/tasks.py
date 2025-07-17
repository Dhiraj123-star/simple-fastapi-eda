from celery import Celery,Task
from celery.exceptions import Retry
import time

celery_app = Celery(
    "simple_fastapi_eda",
    broker="redis://redis:6379/0",
    backend="db+sqlite:///results.sqlite3",  # SQLite as result backend
)

class BaseTaskWithRetry(Task):
    autoretry_for = (Exception,) #retry for all exceptions
    retry_kwargs={
        "max_retries":3,
        "countdown":5
    } # retry upto 3 times,wait for 5s

    retry_backoff=True # exponential backoff(5s,10s,15s)
    retry_jitter=True # Random jitter to avoid thundering herd



@celery_app.task(bind=True, base=BaseTaskWithRetry)
def add_task(self, x: int, y: int) -> int:
    print(f"[Worker] Adding {x} + {y}")
    try:
        if x == 0:
            raise ValueError("Simulated failure: x should not be 0")
        return x + y
    except Exception as exc:
        raise self.retry(exc=exc)
