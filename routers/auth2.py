from fastapi import APIRouter, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

Router = APIRouter(prefix="/auth2", tags=["Auth2"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth2/token")

user_database = {
    'username': 'testuser',
    'password': 'testpass'}

@Router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # In a real application, you would verify the username and password
    # Here, we just return a dummy token for demonstration purposes
    if (form_data.username == user_database['username'] and
        form_data.password == user_database['password']):
        return {"access_token": "dummy_token_for_" + form_data.username, "token_type": "bearer"}
    else:   
        return {"error": "Invalid credentials"}

    

@Router.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    # In a real application, you would decode the token and retrieve user info
    decode_token = token.replace("dummy_token_for_", "")
    if decode_token != user_database['username']:
        return {"error": "Invalid token"}
    return {"username": decode_token}
    # Here, we just return the token for demonstration purposes

