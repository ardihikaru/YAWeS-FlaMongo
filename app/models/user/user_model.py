from app import db
import datetime


class UserModel(db.Document):
    name = db.StringField(required=True, unique=False)
    username = db.StringField(required=True, unique=True)
    email = db.StringField(required=True, unique=True)
    hobby = db.StringField(required=True, unique=False)
    password = db.StringField(required=True, unique=False)
    create_time = db.DateTimeField(required=True, default=datetime.datetime.utcnow)
