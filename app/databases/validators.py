from pydantic import BaseModel
from enum import Enum
from typing import Optional

class Database_enum(str, Enum):
    postgres = 'postgres'
    mysql = 'mysql'


class Database(BaseModel):
    typ:Database_enum
    user:str
    password:str
    server:str
    database:str

class Update_database(BaseModel):
    typ:Optional[Database_enum]
    user:Optional[str]
    password:Optional[str]
    server:Optional[str]
    database:Optional[str]
