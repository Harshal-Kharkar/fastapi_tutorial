from fastapi import APIRouter , Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Annotated    

Router = APIRouter(prefix="/query-params", tags=["Query Parameters"])

class ItemQueryParams(BaseModel):
    item_id: int
    q: str

    

@Router.get("/items")
async def read_item(item_id: int, q: str):
    return {"item_id": item_id, "q": q}

@Router.get("/items-model")
async def read_item(item:Annotated[ItemQueryParams,Query()] ):
    return {"item_id": item.item_id, "q": item.q}


@Router.get("/users/{user_id}/items/{item_name}")
async def read_user_item(user_id: int, item_name: str, short: bool = False,username: str = "guest"):
    item = {"item_name": item_name, "owner_id": user_id, "username": username}
    if short:
       return item
    else:
        return HTMLResponse("short must be true") 
    