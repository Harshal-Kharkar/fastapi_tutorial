from fastapi import BackgroundTasks, FastAPI,APIRouter
import time


Router = APIRouter(prefix="/background_task",tags=["background_task"],)


def write_notification(email: str, message=""):
    print("Notification sent in the background")
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@Router.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}



@Router.get("/bad")
async def bad():
    time.sleep(10)   # BLOCKS server
    return {"msg": "slow"}

@Router.get("/good")
async def good(background_tasks: BackgroundTasks):
    background_tasks.add_task(time.sleep, 10)
    return {"msg": "fast"}

def run_yolo(video_path: str):
    print(f"Running YOLO on {video_path}")
    # load model
    # run inference
    # save results

@Router.post("/upload-video")
async def upload_video(
    background_tasks: BackgroundTasks,
    file_path: str
):
    background_tasks.add_task(run_yolo, file_path)
    return {"msg": "Video received, processing started"}


