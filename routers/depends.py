from fastapi import APIRouter, Depends,HTTPException

from typing import Annotated
import time

Router = APIRouter(prefix="/depends", tags=["Depends"])


# using this funtion for data validation as dependieces  
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@Router.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@Router.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


class as_class:
    def __init__(self,name : str ,age : int):
        self.name=name
        self.age=age

#directly pass class as dependencies 
# @Router.get("/as_class/")
# async def read_users(commons: Annotated[dict, Depends(as_class)]):
#     return commons
#passing as callable 
@Router.get("/as_class/")
async def read_users(commons: Annotated[as_class, Depends()]):
    return commons


# nested dependencies 
async def first_d(q: str | None = None, skip: int = 0, limit: int = 100)-> dict:
    return {"q": q, "skip": skip, "limit": limit}

async def second_d(comman : Annotated[dict ,Depends(first_d)]):
    print("----",comman)
    if comman["q"] == "harshal":
        return comman
    else:
        return {}
    
@Router.get("/deep-depends/")
async def read_users(commons: Annotated[dict , Depends(second_d)]):
    return commons


# before and after  for request 

def get_db():
    try:
        print("📌 Connecting to DB...")
        db = {"conn": "connected"}   # mock DB
        yield db 
    finally:                    # send DB to endpoint
        print("📌 Closing DB connection...")

@Router .get("/after_before/")
def read_items(db = Depends(get_db)):
    print("➡ Using DB:", db)
    return {"message": "Items fetched"}

def timer():
    start = time.time()
    yield
    end = time.time()
    print(f"⏱ Total time = {end - start:.4f} seconds")

@Router.get("/calc")
def calculate(dep = Depends(timer)):
    v = sum(range(1_000_000))
    return {"result": v}


def get_username():
    print('soething')
    try:
        yield "Rick"
    finally:
        print("Cleanup up before response is sent")


@Router.get("/users/me")
def get_user_me(username: Annotated[str, Depends(get_username, scope="requests")]):
    return username

