from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    QuerySet)
import json
from app.user.models import User

from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError, DatabaseError,InterfaceError

class Database_query(QuerySet):
    def Status(self):
        self = json.loads(self.to_json())
        choices={
            'postgres':'postgresql+pg8000',
            'mysql':'mysql+mysqlconnector'
        }
        for obj in self:
            engine = create_engine(
                '{type}://{user}:{password}@{server}/{database}'.format(
                    type= choices[obj['typ']],
                    user=obj['user'], 
                    password=obj['password'], 
                    server=obj['server'],
                    database=obj['database']),
                 pool_recycle=3600)
            try:
                engine.connect()
                obj['status']='success'
            except Exception as e:
                if e.__class__ == ProgrammingError :
                    obj['status']='wrong credentials'
                elif e.__class__ == InterfaceError or e.__class__ == DatabaseError:
                    obj['status']='wrong server address'
                else:
                    obj['status']='qq'
                    print(e.__class__)
        return self


class Database(Document):
    owner = ReferenceField(User)
    typ= StringField(
        choices={
            'postgres':'postgresql+pg8000',
            'mysql':'mysql+mysqlconnector'
        },
        default='postgres')
    user = StringField(default='root', required=True)
    password = StringField(default='', required=True)
    server = StringField(default='', required=True)
    database= StringField(default='', required= True)
    meta = {'queryset_class': Database_query}

