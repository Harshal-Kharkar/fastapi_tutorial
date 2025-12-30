from fastapi import FastAPI, APIRouter

sub_app = FastAPI()
router = APIRouter(prefix="/users")

@router.get("/")
def get_users():
    return {"users": ["john", "amy"]}

sub_app.include_router(router)
