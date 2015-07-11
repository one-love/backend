from flask.ext.mongoengine import MongoEngine


db = MongoEngine()


class Server(db.Document):
    __tablename__ = 'servers'

    name = db.StringField(max_length=512)
    description = db.StringField(max_length=512)
    live = db.BooleanField()
