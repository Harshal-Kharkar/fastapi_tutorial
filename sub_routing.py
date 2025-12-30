from fastapi import FastAPI,APIRouter
from routers import (cookie,auth2,security_tool,
                        jwt_hassing,jwt_token
                     )


sub_rount_secure=APIRouter(prefix="/secure")



sub_rount_secure.include_router(cookie.Router)
sub_rount_secure.include_router(auth2.Router)
sub_rount_secure.include_router(security_tool.Router)
sub_rount_secure.include_router(jwt_hassing.Router)
sub_rount_secure.include_router(jwt_token.Router)
