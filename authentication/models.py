# authentication/models.py
from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

class UserToken(Document):
    access_token = StringField(required=True)
    refresh_token = StringField(required=True)
    token_type = StringField(default='Bearer')
    expires_in = StringField()
    created_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'user_tokens',
        'indexes': ['access_token']
    }