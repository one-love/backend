from . import db


class Server(db.Document):
    __tablename__ = 'servers'

    name = db.StringField(max_length=512)
    description = db.StringField(max_length=512)
    live = db.BoolField()
