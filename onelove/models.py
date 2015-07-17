from flask.ext.mongoengine import Document
from mongoengine.fields import StringField, BooleanField


class Server(Document):
    __tablename__ = 'servers'

    name = StringField(max_length=512)
    description = StringField(max_length=512)
    live = BooleanField()
