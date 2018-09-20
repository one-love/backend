import os

import pytest
from config import configs
from onelove import create_app
from pytest_factoryboy import register

from .factories import AdminFactory, RoleFactory, UserFactory

register(UserFactory)
register(AdminFactory)
register(RoleFactory)


@pytest.fixture
def app():
    config_name = os.getenv('FLASK_ENV') or 'testing'
    flask_app = create_app(configs[config_name])
    print(flask_app.config['MONGODB_HOST'])
    yield flask_app
