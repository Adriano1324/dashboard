from fastapi import (
    APIRouter,
    Security,
    HTTPException)
import json
from mongoengine import NotUniqueError
from app.auth.main import get_current_active_user
from app.user.validators import User as User_validator
from app.user.models import User as User_model
from .validators import Database as Database_validator, Update_database
from.models import Database as Database_model
router = APIRouter()


@router.get("/my/databases")
async def my_databases(current_user: User_validator = Security(get_current_active_user, scopes=['user_auth'])):
    db = Database_model.objects(owner = current_user).Status()
    return json.loads(json.dumps(db))

@router.post("/add/database")
async def add_database(database:Database_validator ,current_user: User_validator = Security(get_current_active_user, scopes=['user_auth'])):
    new_db = Database_model(
        owner=current_user,
        typ = database.typ,
        user = database.user,
        password = database.password,
        server = database.server,
        database = database.database
        )
    try:
        new_db.save()
    except NotUniqueError:
        raise HTTPException(
            status_code=400,
            detail="Not unique username or email"
        )
    return 1


@router.delete('/delete/database/{id}')
async def delete_database(id:str, current_user: User_validator = Security(get_current_active_user, scopes=['user_auth'])):
    db = Database_model.objects(owner = current_user, id = id)
    db.delete()
    return HTTPException(
            status_code=200,
            detail="database connection dropped"
        )

@router.patch("/update/database/{id}")
async def update_user(id: str, db: Update_database, current_user: User_validator = Security(get_current_active_user, scopes=['user_auth'])):
    tmp = {k: v for k, v in db.dict().items() if v is not None}

    database = Database_model.objects(id = id, owner = current_user)
    database.update(**tmp)
    return json.loads(database.to_json())