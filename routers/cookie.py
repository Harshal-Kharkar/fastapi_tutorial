from fastapi import APIRouter,Cookie,Response

Router = APIRouter(prefix="/cookie", tags=["Cookie"])

@Router.get("/set-cookie/")
async def set_cookie(response: Response):
    response.set_cookie(key="ads_id", value="fastapi_cookie_value", httponly=True )
    return {"message": "cookie set"}

@Router.get("/validate-cookie/")
async def validate_cookie(ads_id: str = Cookie(default=None)):
    if ads_id == "fastapi_cookie_value":
        return {"message": "Valid cookie"}
    else:
        return {"message": "Invalid or missing cookie"}