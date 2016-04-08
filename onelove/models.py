from flask_mongoengine import Document
from mongoengine.fields import (
    BooleanField,
    EmailField,
    ListField,
    ReferenceField,
    StringField,
    EmbeddedDocument,
    EmbeddedDocumentListField,
    EmbeddedDocumentField,
    UUIDField,
)
from flask_security import UserMixin, RoleMixin


class Application(EmbeddedDocument):
    name = StringField(max_length=512)
    galaxy_role = StringField(max_length=1024)

    def __repr__(self):
        return '<Application %r>' % self.name

    # Required for administrative interface
    def __unicode__(self):
        return self.__repr__()


class Provider(EmbeddedDocument):
    name = StringField(max_length=512)
    meta = {'allow_inheritance': True}

    def list(self):
        return []

    def update(self):
        pass

    def create(self):
        pass

    def destroy(self):
        pass

    def _field_list(self):
        return []

    def _setup(self):
        pass

    def __init__(self, **kwargs):
        super(Provider, self).__init__(kwargs)
        self._setup()

    def __repr__(self):
        return '<Provider %r>' % self.name

    # Required for administrative interface
    def __unicode__(self):
        return self.__repr__()


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
    roles = ListField(ReferenceField(Role), default=[])
    register_uuid = UUIDField(binary=False)
    username = StringField(max_length=255, unique=True)

    def __repr__(self):
        return '<User %r>' % self.email


class Service(Document):
    user = ReferenceField(User)
    name = StringField(max_length=512, unique_with='user')
    applications = ListField(EmbeddedDocumentField(Application))

    def __repr__(self):
        return '<Service %s/%s>' % (self.user.username, self.name)


class Cluster(Document):
    name = StringField(max_length=512)
    applications = ListField(EmbeddedDocumentField(Application))
    providers = ListField(EmbeddedDocumentField(Provider))
    roles = ListField(ReferenceField(Role), default=[])
    services = ListField(ReferenceField(Service), default=[])

    def __repr__(self):
        return '<Cluster %r>' % self.name


class Task(Document):
    status = StringField(max_length=63, default='PENDING')
    error_message = StringField(max_length=255)
    celery_id = StringField(max_length=255)
