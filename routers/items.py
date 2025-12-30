from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Union
from fastapi.routing import APIRoute
from fastapi.responses import RedirectResponse, JSONResponse

# Router = APIRouter(prefix="/itmes",tags=["Items"],route_class=ConditionalRedirectRoute)

class Items(BaseModel):
    id: str
    title: Union[str, None] = None
    customer: str
    total: float

# Step 1️⃣: Create a custom APIRoute
class ConditionalRedirectRoute(APIRoute):
    def get_route_handler(self):
        original_handler = super().get_route_handler()

        async def custom_handler(request: Request):
            query = request.query_params
            mode = query.get("mode")

            # Condition: redirect dynamically to another endpoint
            if mode == "special":
                return RedirectResponse(url="/items/special")
            elif mode == "normal":
                return RedirectResponse(url="/items/normal")

            # Default behavior if no redirect condition met
            return await original_handler(request)

        return custom_handler

# NOTE: fix typo in prefix (was "/itmes") so routes are available under /items
Router = APIRouter(prefix="/items", tags=["Items"], route_class=ConditionalRedirectRoute)
# Step 3️⃣: Routes
@Router.get("/route", )
async def main_entry():
    return {"message": "No redirect condition met"}

@Router.get("/special")
async def special_item():
    return {"message": "✨ Special item endpoint"}

@Router.get("/normal")
async def normal_item():
    return {"message": "🧾 Normal item endpoint"}

# @Router.post("/items/")
# async def read_item(Items: Items):
#     return {"invoice_data": Items}