from app import db
import datetime
# from mongoengine import signals


class UserModel(db.Document):
    meta = {'collection': 'Users'}
    name = db.StringField(required=True, unique=False)
    username = db.StringField(required=True, unique=True)
    email = db.StringField(required=True, unique=True)
    hobby = db.StringField(required=True, unique=False)
    password = db.StringField(required=True, unique=False)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        # print(" ---- self.updated_at:", self.updated_at)
        return super(UserModel, self).save(*args, **kwargs)

    # @classmethod
    # def pre_save(cls, sender, document, **kwargs):
    #     document.updated_at = datetime.datetime.now()

# signals.pre_save.connect(MyDoc.pre_save, sender=MyDoc)

