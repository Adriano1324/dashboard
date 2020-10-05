from pydantic import BaseModel, HttpUrl, SecretStr
from typing import List, Optional

class User(BaseModel):
    username: str=None
    email: str = None
    full_name: str = None
    password: str = None
    disabled: bool = None
    scopes: List[str] = []
    photo_url:Optional[ HttpUrl]
    public:bool = None

class Get_my_user(BaseModel):
    username: str=None
    email: str = None
    full_name: str = None
    photo_url:Optional[ HttpUrl]
    public:bool = None

class User_Update(BaseModel):
    username: Optional[str]
    email: Optional[str] 
    full_name: Optional[str]
    public: Optional[bool] 
    photo_url:Optional[ HttpUrl]

class send_refresh_token(BaseModel):
    Token: str=None

class user_show(BaseModel):
    username: str
    email: str = None
    full_name: str = None
    photourl:HttpUrl
    public:bool

class All_Users(BaseModel):
    users:List[user_show]
    next_users:HttpUrl
    previous_users:HttpUrl