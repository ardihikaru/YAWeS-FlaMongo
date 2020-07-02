from .db import db


class User(db.Document):
    name = db.StringField(required=True, unique=False)
    username = db.StringField(required=True, unique=True)
    email = db.StringField(required=True, unique=True)
    hobby = db.StringField(required=True, unique=False)
    password = db.StringField(required=True, unique=False)
    # username = db.ListField(db.StringField(), required=True)
    # email = db.ListField(db.StringField(), required=True)
    # hobby = db.ListField(db.StringField(), required=True)
    # password = db.ListField(db.StringField(), required=True)