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
    active = True


class RoleFactory(factory.Factory):
    class Meta:
        model = models.Role

    name = factory.Faker('first_name')
    admin = False


class ClusterFactory(factory.Factory):
    class Meta:
        model = models.Cluster
    name = factory.Faker('first_name')
