from flask_mongoengine import Document
from mongoengine.fields import (
    EmbeddedDocument,
    EmbeddedDocumentField,
    ListField,
    StringField
)


class Application(EmbeddedDocument):
    name = StringField(max_length=512)
    galaxy_role = StringField(max_length=1024)

    def __repr__(self):
        return '<Application %r>' % self.name

    # Required for administrative interface
    def __unicode__(self):
        return self.__repr__()


class Service(Document):
    name = StringField(max_length=512, unique=True)
    applications = ListField(EmbeddedDocumentField(Application))

    def __repr__(self):
        return '<Service %s>' % self.name
