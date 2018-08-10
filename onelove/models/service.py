from flask_mongoengine import Document
from .auth import User
from mongoengine.fields import (
    BooleanField,
    EmailField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    ListField,
    ReferenceField,
    StringField,
    UUIDField,
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
    user = ReferenceField(User)
    name = StringField(max_length=512, unique_with='user')
    applications = ListField(EmbeddedDocumentField(Application))

    def __repr__(self):
        return '<Service %s/%s>' % (self.user.username, self.name)
