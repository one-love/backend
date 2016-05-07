from mongoengine.fields import EmbeddedDocument
from mongoengine.fields import EmbeddedDocumentListField
from mongoengine.fields import StringField

from ..models import Provider
from ..plugin import Plugin


class HostSSH(EmbeddedDocument):
    ip = StringField(max_length=256)
    hostname = StringField(max_length=256)

    def __repr__(self):
        return '<Host %r>' % self.hostname


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


plugin = Plugin(provider=ProviderSSH)
