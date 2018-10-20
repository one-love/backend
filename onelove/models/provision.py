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
    cluster = ReferenceField(Cluster)
    logs = ListField(EmbeddedDocumentField(Log), default=[])
    service = ReferenceField(Service)
    status = StringField(max_length=63, default='PENDING')
    user = ReferenceField(User)


class Option(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return '<{self.key}: {self.value}>'.format(self=self)

    def option(self):
        return '{self.key}={self.value}'.format(self=self)


class ProvisionOptions(object):
    def __init__(self, options=[]):
        self.options = options
