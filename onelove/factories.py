import factory
from django.contrib.auth.models import Group

from . import models


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.User

    email = 'some@onelove.com'
    first_name = 'John'
    last_name = 'Doe'
    is_active = True
    is_staff = False
    is_superuser = False


class GroupFactory(factory.DjangoModelFactory):
    class Meta:
        model = Group

    name = 'onelove'


class FleetFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Fleet

    name = 'onelove'
    url = 'http://www.google.com'
    group = factory.SubFactory(GroupFactory)


class ApplicationFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Application

    name = 'onelove'
    repo = 'https://github.com/one-love/ansible-one-love'
    fleet = factory.SubFactory(FleetFactory)


class AWSProviderFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.AWSProvider

    name = 'awsprovider'
    fleet = factory.SubFactory(FleetFactory)
    type = 'awsprovider'
    access_key = 'access_key'
    security_key = 'security_key'


class SSHProviderFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.SSHProvider

    name = 'sshprovider'
    fleet = factory.SubFactory(FleetFactory)
    type = 'sshprovider'
    ssh_key = 'ssh_key'


class SSHHostFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.SSHHost

    ssh_provider = factory.SubFactory(SSHProviderFactory)
    ip = '192.168.6.66'
