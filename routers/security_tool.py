from fastapi import APIRouter, Request, Depends,HTTPException
from fastapi.security import (APIKeyHeader,APIKeyQuery,APIKeyCookie,
    HTTPBasic, HTTPBasicCredentials,HTTPBearer, HTTPAuthorizationCredentials,
    OAuth2PasswordRequestForm, OAuth2PasswordBearer,OAuth2PasswordRequestFormStrict)
from pydantic import BaseModel
from typing import Annotated
Router = APIRouter(prefix="/security-tool", tags=["Security Tool"])
header_schema = APIKeyHeader(name="X-API-KEY")
query_schema=  APIKeyQuery(name="api_key")

toekn="testtoken123"
query_token="query"
cookie='cookie'
http_creadentials=HTTPBasic()
bearer=HTTPBearer()
outh=OAuth2PasswordBearer(tokenUrl="security-tool/token")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="security-tool/logged-in-user")

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
    "harshal": {
        "username": "harshal",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedharshal",
        "disabled": False,
    },
}

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str

@Router.get("/validate-header/")
async def validate_header(api_key: str = Depends(header_schema)):
    if api_key == toekn:
        return {"message": "Valid API Key"}
    else:
        return {"message": "Invalid API Key"}
    
@Router.get("/validate-query/")
async def validate_query(api_key: str = Depends(query_schema)):
    if api_key == query_token:
        return {"message": "Valid Query API Key"}
    else:
        return {"message": "Invalid Query API Key"}
    
@Router.get("/validate-cookie/")
async def validate_cookie(ads_id: str = Depends(APIKeyCookie(name="cookie"))):
    if ads_id == cookie:
        return {"message": "Valid Cookie API Key"}
    else:
        return {"message": "Invalid Cookie API Key"}
    

@Router.get("/validate-basic-auth/")
async def validate_basic_auth(credentials: HTTPBasicCredentials = Depends(http_creadentials)):
    correct_username = credentials.username == "admin"
    correct_password = credentials.password == "password"
    if correct_username and correct_password:
        return {"message": "Valid Basic Auth"}
    else:
        return {"message": "Invalid Basic Auth"}
    
@Router.get("/validate-bearer-token/")
async def validate_bearer_token(credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    if credentials.credentials == 'demo':
        return {"message": "Valid Bearer Token"}
    else:   
        return {"message": "Invalid Bearer Token"}
    

@Router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # In a real application, you would verify the username and password
    # Here, we just return a dummy token for demonstration purposes
    if (form_data.username == "testuser" and
        form_data.password == "testpass"):
        return {"access_token": "dummy_token_for_" + form_data.username, "token_type": "bearer"}
    else:   
        return {"error": "Invalid credentials"}

@Router.post("/token-serict")
async def login(form_data: OAuth2PasswordRequestFormStrict = Depends()):
    # In a real application, you would verify the username and password
    # Here, we just return a dummy token for demonstration purposes
    if (form_data.username == "testuser" and
        form_data.password == "testpass"):
        return {"access_token": "dummy_token_for_" + form_data.username, "token_type": "bearer"}
    else:   
        return {"error": "Invalid credentials"}
  
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    
def fake_hash_password(password: str):
    print("Hashing password...", password)
    return 'fakehashed'+password

def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    print("token received:", token)
    user = fake_decode_token(token)
    print(f"inside get_current_user user: {user}")
    if not user:
        return {"error": "Invalid token"}
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    print(f"inside get_current_active_user user: {current_user}")
    if current_user.disabled:
        return {"error": "Inactive user"}
    return current_user

@Router.post("/logged-in-user")
async def login(form_data: OAuth2PasswordRequestForm= Depends()):
    print("form data", form_data)
    user_dict = fake_users_db.get(form_data.username)
    print(user_dict)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}

@Router.get("/get_all-users/")
async def get_all_users():
    return fake_users_db

@Router.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user