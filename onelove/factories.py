import factory
import models
from flask_security.utils import encrypt_password


class UserFactory(factory.Factory):
    class Meta:
        model = models.User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = encrypt_password('Sekrit')


class RoleFactory(factory.Factory):
    class Meta:
        model = models.Role

    name = factory.Faker('first_name')
    admin = False


class ProviderSSHFactory(factory.Factory):
    class Meta:
        model = models.ProviderSSH
    name = factory.Faker('first_name')


class ClusterFactory(factory.Factory):
    class Meta:
        model = models.Cluster
    name = factory.Faker('first_name')


class ClusterProviderSSHFactory(factory.Factory):
    class Meta:
        model = models.Cluster
    name = factory.Faker('first_name')
    providers = factory.LazyAttribute(lambda a: [ProviderSSHFactory()])
