from mongoengine import (
    Document,
    StringField,
    BooleanField,
    ListField
)

import json

from app.config import connection,backend_url


class User(Document):
    username = StringField(unique=True, required=True)
    password = StringField(required=True, min_length=8)
    email = StringField(unique=True, required=True)
    full_name = StringField(max_length=50)
    disabled = BooleanField(default=False)
    scopes = ListField(default=['user_auth'])
    photo_url = StringField(default='/static/base.jpg')
    public = BooleanField(default=True)

    meta = {
        'indexes': ['username', 'email']
    }
    
    def create(self):
        self.photo_url = backend_url+self.photo_url
        self.save()

    def me_json(self):
        return {
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'public': self.public,
            'photo_url': self.photo_url
        }