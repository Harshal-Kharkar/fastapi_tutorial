from fastapi import FastAPI,APIRouter
from .tasks import long_task,send_email_task_new,shared_task_test,say_hello

Router = APIRouter(prefix="/celery",tags=["celery"])

@Router.get("/")
def root():
    return {"message": "FastAPI + Celery is running"}

@Router.post("/start-task/")
def start_task(name: str):
    task = long_task.delay(name)  # async task
    return {
        "task_id": task.id,
        "status": "Task started"
    }

@Router.post("/send-email/")
def send_email(email: str, subject: str, message: str):
    task = send_email_task_new.apply_async(args=[email, subject, message])
    task_shared = shared_task_test.delay()
    return {
        "task_id": task.id,
        "status": "Email sent",
        "task_shared_id": task_shared.id,
        "status_shared": "Shared task started"
    }

@Router.get("/say-hello/")
def root():
    # Trigger Celery task manually
    say_hello.delay("FastAPI User")
    return {"message": "Task has been sent to Celery!"}


