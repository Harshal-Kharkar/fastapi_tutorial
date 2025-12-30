from contextlib import asynccontextmanager

from fastapi import FastAPI,APIRouter


items = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    items["foo"] = {"name": "Fighters"}
    items["bar"] = {"name": "Tenders"}
    print("using context manager")
    print("🚀 Application startup: Items initialized with",items)
    yield
    # Clean up the ML models and release the resources
    items.clear()
    print("using context manager")
    print("🛑 Application shutdown: Cleaning up resources...",items)


Router = APIRouter(prefix="/contextlib", tags=["contextlib"],lifespan=lifespan)


@Router.get("/predict/{item_id}")
async def predict(item_id:str):
    result = items.get(item_id, {"error": "Item not found"})
    return {"result": result}