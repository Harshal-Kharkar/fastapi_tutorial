



from celery import Celery
from datetime import timedelta
from celery.schedules import crontab

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# 👇 IMPORTANT: tell Celery where tasks live
celery_app.autodiscover_tasks([
    "celery_test"
])

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
     task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_soft_time_limit=30,
    task_time_limit=60,
    max_tasks_per_child=100,
    beat_schedule={
        "say-hello-every-2-seconds": {
            "task": "celery_test.tasks.say_hello",
            "schedule": timedelta(seconds=100),
            "args": ("World",)
        },
      
        "nightly_etl": {
            "task": "celery_test.tasks.execute_etl_chain",
            # "schedule": crontab(hour=0, minute=1),
            "schedule": timedelta(seconds=100),
        },

        "batch_processing": {
        "task": "celery_test.tasks.run_batch",
        # "schedule": crontab(hour=0, minute=0),
        "schedule": timedelta(seconds=500),
    },

    "chord_example": {
        "task": "celery_test.tasks.run_chord",
        "schedule": timedelta(seconds=500),
    },
        
    "real-world-etl": {
            "task": "celery_test.tasks.run_etl",
            "schedule": timedelta(seconds=10),
        },

    }
)

# celery_app.setup_security()