from mongoengine import NotUniqueError, DoesNotExist

from fastapi import (
    APIRouter,
    HTTPException, 
    Depends, 
    Security,
    UploadFile,
    File
    )

router = APIRouter()

from typing import Optional, List

import json

from app.token.validators import Token, TokenData

from .validators import (
    User as User_validator,
    send_refresh_token,
    User_Update,
    Get_my_user)

from .models import User as User_model

from app.config import mail, jinja_env, backend_url

from app.auth.main import (
    get_current_active_user,
    authorize_user,
    get_password_hash)

from datetime import timedelta

from app.auth.main import (
    create_access_token,
    authorize_user,
    token_decode)

import json

import os
#get

#get logged user data
@router.get("/user/me", response_model=Get_my_user)
async def read_users_me(current_user: User_validator = Depends(get_current_active_user)):
    return current_user.me_json()

#get all users list for admin
@router.get("/user/all")
async def read_all_users(current_user: User_validator = Security(get_current_active_user,scopes=['admin']),page:int =1,items_per_page:int=20,username:str=''):
    offset = (int(page) - 1) * int(items_per_page)
    if username =='':
        users = User_model.objects().only('username','email','full_name','photo_url').skip( offset ).limit( items_per_page )
    else:
        users = User_model.objects(username__contains=username).only('username','email','full_name','photo_url').skip( offset ).limit( items_per_page )
    return json.loads(users.to_json())

#get list of public list
@router.get("/user/list")
async def read_public_users(page:int =1,items_per_page:int=20,username:str=''):
    offset = (int(page) - 1) * int(items_per_page)
    if username =='':
        users = User_model.objects(public=True).only('username','email','full_name','photo_url').skip( offset ).limit( items_per_page )
    else:
        users = User_model.objects(public=True, username__contains=username).only('username','email','full_name','photo_url').skip( offset ).limit( items_per_page )
    return json.loads(users.to_json())


#post

#post photo 

@router.post("/user/change/photo")
async def photo( photo:UploadFile = File(...),current_user: User_validator = Security(get_current_active_user, scopes=['user_auth'])):
    photo_url=backend_url+'/static/' + current_user.username+'/'+photo.filename
    os.makedirs(os.path.dirname('static/'+ current_user.username+'/'), exist_ok=True)
    current_user.update(photo_url=photo_url)
    with open('static/'+ current_user.username+'/'+photo.filename, 'wb') as f:
        f.write(await photo.read())
    return HTTPException(200)


#create new user account
@router.post("/user/create")
async def register(User:User_validator):
    new_user = User_model(
        username = User.username,
        password = User.password,
        email = User.email,
        full_name = User.full_name,
        disabled = False,
        photo_url = '/static/base.jpg',
        public = User.public
    )
    new_user.password = get_password_hash(new_user.password)
    try:
        new_user.create()
    except NotUniqueError:
        raise HTTPException(
            status_code=400,
            detail="Not unique username or email"
        )

    

    access_token_expires = timedelta(hours=62)
    access_token = create_access_token(
        data={"sub": new_user.username, "scopes": 'activate'},
        expires_delta=access_token_expires,
        refresh=False
    )
    data = {
        'username':new_user.username,
        'token':access_token['token'].decode("utf-8")
    }
    template = jinja_env.get_template('activate.html')
    output = template.render(data=data)
    #await mail.send_message(recipient=new_user.email,
    #        subject="account activation token",
    #        body=output,
    #        text_format="html")

    return new_user.to_json()


#send refresh token for existing user
@router.post("/user/remember-password")
async def get_change_password_code(username:str):
    try:
        user = User_model.objects.get(username=username)
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )
    access_token_expires = timedelta(hours=62)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": 'change_password'},
        expires_delta=access_token_expires,
        refresh=False
    )
    data = {
        'username':user.username,
        'token':access_token['token'].decode("utf-8")
    }
    template = jinja_env.get_template('remember_password.html')
    output = template.render(data=data)
    await mail.send_message(recipient=user.email,subject="Remember password", body=output , text_format="html")

    raise HTTPException(
            status_code=200,
            detail="send password renew email"
        )
#put

#update user account (update only sended fields)
@router.put("/user/update")
async def update_user(user_data:User_Update,
            current_user: User_validator = Security(get_current_active_user, scopes=['user_auth'])):
    user_data = {k: v for k, v in user_data.dict().items() if v is not None}
    current_user.update(**user_data)
    return current_user

#patch

#activate user account with activate token
@router.patch("/user/activate")
async def activate_user(token:send_refresh_token):
    token_data:TokenData=token_decode(token.Token)
    if 'activate' in token_data['scopes']:
        user = User_model.objects.get(username=token_data['sub'])
        user.update(disabled = False)
    raise HTTPException(
            status_code=200,
            detail="Account activated"
        )

#change password with token and new password
@router.patch("/user/change/password")
async def change_password(token:send_refresh_token,
            new_password:str):
    token_data:TokenData=token_decode(token.Token)
    if 'change_password' in token_data['scopes']:
        user = User_model.objects.get(username=token_data['sub'])
        password = get_password_hash(new_password)
        user.update(password = password)
    raise HTTPException(
            status_code=200,
            detail="password changed"
        )

#change user scopes
@router.patch("/user/modify-scope")
async def modify_scopes(username:str,
            scopes_list:List[str],
            current_user: User_validator = Security(authorize_user,scopes=['admin'])):
    try:
        user = User_model.objects.get(username=username)
    except DoesNotExist:
                raise HTTPException(
            status_code=404,
            detail="user not found"
        )
    user.update(scopes=scopes_list)