from flask_mongoengine import Document
from mongoengine.fields import (
    EmbeddedDocument,
    EmbeddedDocumentField,
    ListField,
    ReferenceField,
    StringField
)

from .auth import User
from .cluster import Cluster
from .service import Service


class Log(EmbeddedDocument):
    status = StringField(default=None)
    host = StringField(default=None)
    task = StringField(default=None)
    timestamp = StringField(default=None)
    log = StringField(default=None)


class Provision(Document):
    status = StringField(max_length=63, default='PENDING')
    cluster = ReferenceField(Cluster)
    service = ReferenceField(Service)
    user = ReferenceField(User)
    logs = ListField(EmbeddedDocumentField(Log), default=[])
