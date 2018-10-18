from flask_mongoengine import Document
from mongoengine.fields import (
    BaseField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    ListField,
    ReferenceField,
    StringField
)

from .auth import Role
from .service import Service

field_types = {
    'BooleanField': 'boolean',
    'DateTimeField': 'date_time',
    'EmailField': 'email',
    'ReferenceField': 'reference',
    'StringField': 'string',
    'UUIDField': 'uuid',
}


class Provider(EmbeddedDocument):
    name = StringField(max_length=512)
    type = 'BASE'
    meta = {'allow_inheritance': True}

    def list(self):
        return []

    def update(self, **kwargs):
        pass

    def create(self, **kwargs):
        pass

    def destroy(self, id):
        pass

    @classmethod
    def _check_field(cls, field):
        if isinstance(field, BaseField):
            if isinstance(field, EmbeddedDocument):
                return False
            if isinstance(field, EmbeddedDocumentField):
                return False
            if isinstance(field, EmbeddedDocumentListField):
                return False
            if isinstance(field, ListField):
                return False
            return True
        return False

    @classmethod
    def fields(cls):
        result = []
        for property in dir(cls):
            if property[0] != '_':
                property_type = getattr(cls, property)
                if cls._check_field(property_type):
                    type_name = type(property_type).__name__
                    result.append(
                        {
                            'name': property_type.name,
                            'type': field_types[type_name]
                        }
                    )
        return result

    def _setup(self):
        pass

    def __init__(self, *args, **kwargs):
        super(Provider, self).__init__(*args, **kwargs)
        self._setup()

    def __repr__(self):
        return '<Provider %r>' % self.name


class Cluster(Document):
    name = StringField(max_length=512, blank=False)
    username = StringField(max_length=64)
    sshKey = StringField()
    providers = ListField(EmbeddedDocumentField(Provider), default=[])
    roles = ListField(ReferenceField(Role), default=[])
    services = ListField(ReferenceField(Service), default=[])

    def __repr__(self):
        return '<Cluster %r>' % self.n
