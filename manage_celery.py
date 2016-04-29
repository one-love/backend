import os

from onelove import OneLove
from onelove.utils import create_app, setup_ansible_callbacks


config_name = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(config_name)
onelove = OneLove(app)

setup_ansible_callbacks()

from onelove.tasks import *

celery = onelove.celery
