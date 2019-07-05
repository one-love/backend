from flask_mongoengine import Document
from flask_security import RoleMixin, UserMixin
from mongoengine.fields import (
    BooleanField,
    EmailField,
    ListField,
    ReferenceField,
    StringField
)


class Role(Document, RoleMixin):
    """
    Role
    """
    name = StringField(max_length=255)
    description = StringField(max_length=255)

    # Required for administrative interface
    def __unicode__(self):
        return self.name


class User(Document, UserMixin):
    """
    User
    """
    active = BooleanField(default=False)
    admin = BooleanField()
    email = EmailField(unique=True)
    first_name = StringField(max_length=255)
    last_name = StringField(max_length=255)
    password = StringField(max_length=255)
    roles = ListField(ReferenceField(Role), default=[])

    def __repr__(self):
        return '<User %r>' % self.email
