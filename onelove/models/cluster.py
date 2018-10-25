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


class Cluster(Document):
    name = StringField(max_length=512, blank=False)
    username = StringField(max_length=64)
    sshKey = StringField()
    providers = ListField(EmbeddedDocumentField(Provider), default=[])
    roles = ListField(ReferenceField(Role), default=[])
    services = ListField(ReferenceField(Service), default=[])
    tags = ListField(StringField(), default=[])

    def __repr__(self):
        return '<Cluster %r>' % self.name

    def hosts(self):
        result = []
        for provider in self.providers:
            result.extend(provider.host_by_tag(self.tags))
        return result
