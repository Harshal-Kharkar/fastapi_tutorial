from fastapi import FastAPI
from routers import (items,users,websocket,on_event,
                     contextlib,path_parameters,Query_paramters
                     ,Request_body,cookie,auth2,security_tool,
                        jwt_hassing,jwt_token,depends,database,pgadmin,
                        Background_task,sse
                     )
from celery_test.run_celery import Router 
import time
import requests
from sub_routing import sub_rount_secure
import uvicorn
from middleware import CustomMiddleware , RouterSpecificMiddleware
from sub_app import sub_app
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost.demo.com",
    # "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware to the FastAPI app
app.add_middleware(CustomMiddleware)
app.add_middleware(RouterSpecificMiddleware)

#sub app 
app.mount('/sub',sub_app)

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}



@app.middleware("http")
async def add_process_time_header(request: requests, call_next):
    print("runing middle ware")
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
# app.add_middler

app.include_router(items.Router)
app.include_router(users.Router)
app.include_router(websocket.Router)
# app.include_router(on_event.Router)
app.include_router(contextlib.Router)
app.include_router(path_parameters.Router)
app.include_router(Query_paramters.Router)
app.include_router(Request_body.Router)
# app.include_router(cookie.Router)
# app.include_router(auth2.Router)
# app.include_router(security_tool.Router)
# app.include_router(jwt_hassing.Router)
# app.include_router(jwt_token.Router)
app.include_router(sub_rount_secure)
app.include_router(depends.Router)
app.include_router(database.Router)
# app.include_router(pgadmin.Router)
app.include_router(Background_task.Router)
app.include_router(sse.Router)

app.include_router(Router)

if __name__== "__main__":
    uvicorn.run("main:app", reload=True,host="0.0.0.0",port=8000)
