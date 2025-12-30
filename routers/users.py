from fastapi import APIRouter
from pydantic import BaseModel
import requests

Router = APIRouter(prefix="/users",tags=["users"])


class Users(BaseModel):
    id: str
    name: str
    email: str

@Router.post("/users/")
async def create_user(user: Users):
    return {"user_data": user}