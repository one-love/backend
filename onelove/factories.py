import factory
from flask_security.utils import encrypt_password

import models
from providers import ssh
from bson.objectid import ObjectId


class UserFactory(factory.Factory):
    class Meta:
        model = models.User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = encrypt_password('Sekrit')
    active = True
    username = factory.Faker('name')
    id = factory.LazyAttribute(lambda obj: '%s' % ObjectId())

class RoleFactory(factory.Factory):
    class Meta:
        model = models.Role

    name = factory.Faker('first_name')
    admin = False


class ClusterFactory(factory.Factory):
    class Meta:
        model = models.Cluster
    name = factory.Faker('first_name')
    username = 'vagrant'
    providers = factory.LazyAttribute(lambda a: [ProviderSSHFactory()])


class ServiceFactory(factory.Factory):
    class Meta:
        model = models.Service
    name = factory.Faker('first_name')
    user = factory.SubFactory(UserFactory)
    applications = factory.LazyAttribute(lambda a: [ApplicationFactory()])


class ApplicationFactory(factory.Factory):
    class Meta:
        model = models.Application
    name = factory.Faker('first_name')
    galaxy_role = 'onelove-roles.common'


class ProviderSSHFactory(factory.Factory):
    class Meta:
        model = ssh.ProviderSSH
    name = factory.Faker('first_name')
    hosts = factory.LazyAttribute(lambda a: [HostSSHFactory()])


class HostSSHFactory(factory.Factory):
    class Meta:
        model = ssh.HostSSH
    ip = '192.168.33.34'
    hostname = 'target.vagrant'
