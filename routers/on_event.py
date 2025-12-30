from fastapi import APIRouter, FastAPI

Router = APIRouter(prefix="/onevent", tags=["onevent"],)

items = {}


@Router.on_event("startup")
async def startup_event():
    items["foo"] = {"name": "Fighters"}
    items["bar"] = {"name": "Tenders"}
    print("using on_event startup")
    print("🚀 Application startup: Items initialized with",items)

@Router.on_event("shutdown")
def shutdown_event():
    items.clear()
    print("using on_event shutdown")
    print("🛑 Application shutdown: Cleaning up resources...",items)

@Router.get("/items/{item_id}")
async def read_items(item_id: str):
    return items[item_id]