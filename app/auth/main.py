from datetime import datetime, timedelta

from app.token.validators import Token, TokenData
from app.user.validators import User
from app.user.models import User as User_model

import jwt
from jwt import PyJWTError

from pydantic import ValidationError

from passlib.context import CryptContext

from starlette.status import HTTP_401_UNAUTHORIZED


from fastapi import (
    Depends,
    HTTPException,
    Security,
    Header
)

from fastapi.security import (
    OAuth2PasswordBearer,
    SecurityScopes
)

from mongoengine.errors import DoesNotExist
from .scopes import scopes as APIscopes


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/token",
    scopes=APIscopes
)

#decode user token
def token_decode(token: str):
    data = []
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception as e:

        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": str(e)},
        )
    return data

#verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

#hash plain password
def get_password_hash(password):
    return pwd_context.hash(password)

#return user by username
def get_user(username: str):
    try:
        result = User_model.objects.get(username=username)
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid username",
        )
    return result

#authenticate user by
def authenticate_user(username: str, password: str):
    try:
        user = get_user(username)
    except DoesNotExist:
        return False
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

# create access token with specific scopes
def create_access_token(*, data: dict, expires_delta: timedelta = None, refresh = True):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    if refresh:
        expire = datetime.utcnow() + timedelta(hours=24)
        to_encode.update({"exp": expire})
        to_encode['scopes'] = 'refresh'
        refresh_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        encoded_jwt = {
            'token': token,
            'refresh_token': refresh_token
        }
    else:
        encoded_jwt = {
            'token': token
        }
    
    return encoded_jwt


async def authorize_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = token_decode(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (PyJWTError, ValidationError):
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(current_user: User = Security(authorize_user, scopes=['user_auth'])):
    
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
