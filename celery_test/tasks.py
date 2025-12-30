# from tutorial.Router import app
from .celery_app import celery_app
import time
from celery import group,chord,chain

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def long_task(name: str):
    time.sleep(5)   # simulate heavy work
    return f"Hello {name}, task completed!"


@celery_app.task
def send_email_task_new(email: str, subject: str, message: str):
    time.sleep(1)   # simulate heavy work
    print(f"Sending email to {email} with subject {subject} and message {message}")
    return f"Email sent to {email} with subject {subject} and message {message}"

@celery_app.task(shared=True)
def shared_task_test():
    print("Shared task started")
    time.sleep(1)
    print("Shared task completed")
    return "Shared task completed"

@celery_app.task
def say_hello(name):
    print(f"Hello, {name}!")
    return f"Greeted {name}"



#Periodic ETL job → extract → transform → load
@celery_app.task
def extract():
    print("Extracting data...")
    data = {"data": [1, 2, 3, 4, 5]}
    return data
@celery_app.task
def transform(data):
    print("Transforming data...")
    transformed_data = [x * 2 for x in data["data"]]
    return {"transformed_data": transformed_data}
@celery_app.task
def load(transformed_data):
    print("Loading data...")
    print(f"Data loaded: {transformed_data['transformed_data']}")
    return "Data loading completed"
@celery_app.task
def execute_etl_chain():
    workflow = chain(extract.s(), transform.s(), load.s())
    workflow.delay()


# Grouped Tasks Example
@celery_app.task
def bulk_message(fid):
    return f"hiii {fid}"
@celery_app.task
def run_batch():
    file_ids = range(10)
    job = group(bulk_message.s(fid) for fid in file_ids)
    return job.apply_async()


#chord Tasks Example
@celery_app.task
def process_data(data):
    return data * 2
@celery_app.task
def summarize_results(results):
    return sum(results)
@celery_app.task
def run_chord():
    data_chunks = [1, 2, 3, 4, 5]
    job = chain(
        chord(
            (process_data.s(data) for data in data_chunks),
            summarize_results.s()
        )
    )
    return job.apply_async()

# real-world chord chain and group examples can be more complex
# --------  EXTRACT  --------
@celery_app.task
def extract():
    print("📥 Extracting data...")
    return {"data": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}

# --------  TRANSFORM (parallel shards)  --------
@celery_app.task
def process_partition(partition_id):
    print(f"⚙️ Processing partition {partition_id}")
    return partition_id * 2  # pretend transformation output
# --------  AGGREGATE (after all shards complete) --------
@celery_app.task
def aggregate(results):
    print("🧮 Aggregating results:", results)
    return sum(results)
# --------  LOAD  --------
@celery_app.task
def load_to_db(total):
    print(f"💾 Loading result={total} into database")
    return {"status": "success", "value": total}
# --------  NOTIFY  --------
@celery_app.task
def notify(result):
    print("📢 Pipeline completed:", result)
    return True
# --------  PIPELINE RUNNER (triggered by Beat) --------
@celery_app.task
def run_etl():
    print("🚀 Starting ETL pipeline...")

    pipeline = (
        extract.s()
        | chord(
            group(process_partition.si(p) for p in range(10)),
            aggregate.s(),
        )
        | load_to_db.s()
        | notify.s()
    )

    return pipeline.apply_async()