from fastapi import APIRouter

from app.token.validators import Token

from datetime import timedelta
from fastapi import (
    Depends,
    HTTPException,
    Header
)
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm
)

from app.auth.main import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    token_decode,
    get_user,
    create_access_token
)

router = APIRouter()

#post

#Get access token
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": user.scopes},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token['token'], "token_type": "bearer", "refresh_token": access_token['refresh_token']}

#refresh inactive token
@router.post("/token/refresh", response_model=Token)
async def refresh_access_token(refresh_token: str = Header(None)):
    payload = token_decode(refresh_token)
    username = payload.get('sub')
    if 'refresh' in payload['scopes']:
        user = get_user(username=username)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "scopes": user.scopes},
            expires_delta=access_token_expires,
        )
        return {"access_token": access_token['token'], "token_type": "bearer", "refresh_token": access_token['refresh_token']}
    else:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token type",
            headers={"WWW-Authenticate": "Bearer"},
        )
