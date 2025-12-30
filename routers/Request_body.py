from fastapi import APIRouter
from pydantic import BaseModel,Field

Router=APIRouter(prefix="/body-params", tags=["body Parameters"])

class Requestclass(BaseModel):
    name: str  = Field(default=None, examples=["A very nice Item"])
    phone: int = Field(default=None, examples=[1234567890])
    add: str

   


@Router.get('/user_data')
async def user_data(data:Requestclass):
    return data


