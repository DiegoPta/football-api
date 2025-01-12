"""
Auth script for the application.
"""

# Python imports.
import os, jwt
from dotenv import load_dotenv
from fastapi import Request
from fastapi import APIRouter, Body, status, HTTPException


load_dotenv('.env')
users: list[dict] = [{"username": os.getenv('USER'), "password": os.getenv('PASSWORD')}]


router = APIRouter(prefix='/auth', tags=['Auth'])


def verify_token(request: Request) -> bool:
    """
    Verifies if the user is authorized to access the endpoint.
    @param request: Request object.
    """
    if token := request.headers.get('Authorization'):
        try:
            token = token.split(' ')[-1]
            data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            if user := next(filter(lambda u: u['username'] == data['username'], users), None):
                if user == data:
                    return True
        except:
            pass
    return False


def verify_token_dependency(request: Request) -> None:
    """
    Verifies if the user is authorized to access the endpoint.
    @param request: Request object.
    """
    if not verify_token(request):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized!")
    

@router.post('/login', status_code=status.HTTP_200_OK)
def login_user(username: str = Body(), password: str = Body()) -> dict:
    """
    Logs in a user and returns a token.
    - **username**:    Username of the user.
    - **password**:    Password of the user.    
    """
    if user := next(filter(lambda u: u['username'] == username, users), None):
        if user['password'] == password:
            return {'token': f"Bearer {jwt.encode(user, os.getenv('SECRET_KEY'), algorithm='HS256')}"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid data!')
