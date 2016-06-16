rom mongoengine.fields import EmbeddedDocument
from mongoengine.fields import EmbeddedDocumentListField
from mongoengine.fields import StringField
import digitalocean
import time

from ..models import Provider
from ..plugin import Plugin


class HostDO(EmbeddedDocument):
    ip = StringField(max_length=256)
    hostname = StringField(max_length=256)

    def __repr__(self):
        return '<Host %r>' % self.hostname


class ProviderDO(Provider):
    type = 'DO'
    hosts = EmbeddedDocumentListField(HostDO)

    # Hard coded for now
    token = "Put_Your_Digital_Ocean_Api_Key_Here"
    anager = digitalocean.Manager(token=token)
    name = 'pythonApi'
    region = 'ams2'
    image = 'debian-8-x64'
    size_slug = '512mb'
    backups = False

    def list(self):
        return self.hosts

    def create(self, hostname, ip):

        droplet = digitalocean.Droplet(token=self.token,
                                       name=self.name,
                                       region=self.region,
                                       image=self.image,
                                       size_slug=self.size_slug,
                                       backups=self.backups)
        droplet.create()

        # Wait droplet to start
        status = 'in-progress'
        while status != 'completed':
            time.sleep(2)
            actions = droplet.get_actions()
            for action in actions:
                action.load()
                status = action.status

        # Wait for droplet IP address
        while droplet.ip_address is None:
            time.sleep(2)
            droplet = self.manager.get_droplet(droplet.id)

        host = HostDO(ip=droplet.ip_address, hostname=droplet.name)
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


plugin = Plugin(provider=ProviderDO)
