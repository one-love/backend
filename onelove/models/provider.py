from mongoengine.fields import (
    BaseField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    ListField,
    StringField
)

field_types = {
    'BooleanField': 'boolean',
    'DateTimeField': 'date_time',
    'EmailField': 'email',
    'ReferenceField': 'reference',
    'StringField': 'string',
    'UUIDField': 'uuid',
}


class Provider(Document):
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

    def hosts_by_tag(self, tags=[]):
        return []

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


class HostSSH(EmbeddedDocument):
    ip = StringField(max_length=256)
    hostname = StringField(max_length=256)
    tags = ListField(StringField(), default=[])

    def __repr__(self):
        return '<Host %r>' % self.hostname

    def has_tags(self, tags):
        for tag in tags:
            if tag in self.tags:
                return True
        return False


class ProviderSSH(Provider):
    type = 'SSH'
    hosts = EmbeddedDocumentListField(HostSSH)

    def list(self):
        return self.hosts

    def create(self, ip, hostname):
        host = HostSSH(ip=ip, hostname=hostname)
        self.hosts.append(host)
        self.save()
        return host

    def destroy(self, hostname):
        for host in self.hosts:
            if host.hostname == hostname:
                self.hosts.remove(host)
                return host
        return None

    def update(self, hostname, new_ip=None, new_hostname=None):
        for host in self.hosts:
            if host.hostname == hostname:
                host.ip = new_ip or host.ip
                host.hostname = new_hostname or host.hostname
                self.hosts.save()
                return host
        return None

    def hosts_by_tag(self, tags=[]):
        return list(filter(lambda host: host.have_tags(tags)), self.hosts)
