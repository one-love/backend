from mongoengine import EmbeddedDocument, StringField, Document, ListField, EmbeddedDocumentField
from mongoengine import fields
from mongoengine.django.auth import User


class Application(EmbeddedDocument):
    name = StringField(max_length=256)
    repo = StringField(max_length=256)

    def __unicode__(self):
        return self.name


class Provider(EmbeddedDocument):
    name = StringField(max_length=256)

    def __unicode__(self):
        return self.name


class Fleet(Document):
    name = StringField(max_length=256)
    url = StringField(max_length=2048)
    applications = ListField(EmbeddedDocumentField(Application))
    providers = ListField(EmbeddedDocumentField(Provider))
    user = fields.ReferenceField(User)

    def __unicode__(self):
        return self.name
