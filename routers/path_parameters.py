from fastapi import APIRouter, Path, Depends
from pydantic import BaseModel, Field
from enum import Enum
from typing import Annotated

Router = APIRouter(prefix="/path-params", tags=["Path Parameters"])

# Pydantic model for validation
class ItemPathParams(BaseModel):
    item_id: int = Field(..., gt=0)
    name: str = Field(..., min_length=3)

class NameEnum(str, Enum):
    widget = "widget"
    gadget = "gadget"
    doodad = "doodad"

# Dependency to validate and assemble parameters
def get_item_params(
    item_id: int = Path(..., gt=0),
    name: str = Path(..., min_length=3)
):
    return ItemPathParams(item_id=item_id, name=name)

# Route
@Router.get("/items/{item_id}/{name}",
            summary="Get item by ID and name with validation",
            description="Retrieve an item by its ID and name, ensuring the ID is greater than 0 and the name has at least 3 characters.",)
async def read_item(params: ItemPathParams = Depends(get_item_params)):
    return params


@Router.get("/items-enum/{name}", deprecated=True)
async def read_item_enum(name: NameEnum=Path(description="The name of the item")):
    '''
     Get item by name from predefined set custom docstring
    '''
    return {"name": name, "message": f"You selected the {name}!"}