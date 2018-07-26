from flask_mongoengine import Document
from flask_security import UserMixin, RoleMixin
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


class Role(Document, RoleMixin):
    """
    Role
    """
    name = StringField(max_length=255)
    admin = BooleanField()
    description = StringField(max_length=255)

    # Required for administrative interface
    def __unicode__(self):
        return self.name


class User(Document, UserMixin):
    """
    User
    """
    active = BooleanField(default=False)
    email = EmailField(unique=True)
    first_name = StringField(max_length=255)
    last_name = StringField(max_length=255)
    password = StringField(max_length=255)
    register_uuid = UUIDField(binary=False)
    roles = ListField(ReferenceField(Role), default=[])
    username = StringField(max_length=255, unique=True)

    def __repr__(self):
        return '<User %r>' % self.email
