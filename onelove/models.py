from flask.ext.mongoengine import Document
from mongoengine.fields import (
    StringField,
    EmailField,
    EmbeddedDocument,
    EmbeddedDocumentListField
)


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


class Cluster(Document):
    name = StringField(max_length=512)
    applications = EmbeddedDocumentListField(Application)
    providers = EmbeddedDocumentListField(Provider)

    def __repr__(self):
        return '<Cluster %r>' % self.name


class User(Document):
    first_name = StringField(max_length=512)
    last_name = StringField(max_length=512)
    email = EmailField(unique=True)
    password = StringField(max_length=512)

    def __repr__(self):
        return '<user %r>' % self.email
