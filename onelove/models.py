from flask.ext.mongoengine import Document
from mongoengine.fields import (
    BooleanField,
    EmailField,
    ListField,
    ReferenceField,
    StringField,
    EmbeddedDocument,
    EmbeddedDocumentListField
)
from flask.ext.security import UserMixin, RoleMixin


class Application(EmbeddedDocument):
    name = StringField(max_length=512)
    galaxy_role = StringField(max_length=1024)
    application_name = StringField(max_length=1024)

    def __repr__(self):
        return '<Application %r>' % self.name


class Provider(EmbeddedDocument):
    name = StringField(max_length=512)
    meta = {'allow_inheritance': True}

    def __repr__(self):
        return '<Provider %r>' % self.name


class ProviderAWS(Provider):
    secret_key = StringField(max_length=512)
    access_key = StringField(max_length=512)


class HostSSH(EmbeddedDocument):
    ip = StringField(max_length=128)
    hostname = StringField(max_length=256)

    def __repr__(self):
        return '<Host %r>' % self.hostname


class ProviderSSH(Provider):
    private_key = StringField(max_length=4096)
    hosts = EmbeddedDocumentListField(HostSSH)


class Cluster(Document):
    name = StringField(max_length=512)
    applications = EmbeddedDocumentListField(Application)
    providers = EmbeddedDocumentListField(Provider)

    def __repr__(self):
        return '<Cluster %r>' % self.name


class Role(Document, RoleMixin):
    """
    Role
    """
    name = StringField(max_length=255, unique=True)
    description = StringField(max_length=255)


class User(Document, UserMixin):
    """
    User
    """
    active = BooleanField(default=True)
    email = EmailField(unique=True)
    first_name = StringField(max_length=255)
    last_name = StringField(max_length=255)
    password = StringField(max_length=255)
    roles = ListField(ReferenceField(Role), default=[])

    def __repr__(self):
        return '<user %r>' % self.email


class Task(Document):
    status = StringField(max_length=63)
    celery_id = StringField(max_length=255)
