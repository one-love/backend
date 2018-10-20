from flask_mongoengine import Document
from mongoengine.fields import (
    EmbeddedDocumentField,
    ListField,
    ReferenceField,
    StringField
)

from .auth import Role
from .provider import Provider
from .service import Service

field_types = {
    'BooleanField': 'boolean',
    'DateTimeField': 'date_time',
    'EmailField': 'email',
    'ReferenceField': 'reference',
    'StringField': 'string',
    'UUIDField': 'uuid',
}


class Cluster(Document):
    name = StringField(max_length=512, blank=False)
    username = StringField(max_length=64)
    sshKey = StringField()
    providers = ListField(EmbeddedDocumentField(Provider), default=[])
    roles = ListField(ReferenceField(Role), default=[])
    services = ListField(ReferenceField(Service), default=[])

    def __repr__(self):
        return '<Cluster %r>' % self.n
