from fastapi import APIRouter
import jwt  # Correct import for the PyJWT package
from jwt.exceptions import InvalidKeyError  # Correct exception
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Annotated

Router = APIRouter(prefix="/jwt-token", tags=["JWT Token"])

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class TokenData(BaseModel):
    username: str | None = None
    password: str | None = None

class Token(TokenData):
    token : str 

user_data={}

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    print("Creating access token...with data:", data)
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print("Token created:", encoded_jwt)
    return encoded_jwt

@Router.post("/get-token")
async def get_token(tokendata: TokenData):
    print(f"Received request for token with username: {tokendata.username} and password: {tokendata.password}")
    access_token_expires = timedelta(seconds=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {"username": tokendata.username, "password": tokendata.password}
    access_token = create_access_token(
        data=token_data, expires_delta=access_token_expires
    )
    print("Returning access token...")
    token_data['token']=access_token
    user_data[tokendata.username]=token_data
    print(f'user data after getting token {user_data}')
    return {"access_token": access_token, "token_type": "bearer"}


@Router.post("/verify-toke")
async def verify(token:Token):
    print(token)
    if token.username in user_data:
        print("-----------------",user_data[token.username])
        if user_data[token.username]['token']==token.token:
            return {"message":"valid toke"}
    else:
        return {"message":"not a valid toke"}

