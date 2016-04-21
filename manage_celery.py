import os

from onelove import OneLove
from onelove.utils import create_app


config_name = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(config_name)
onelove = OneLove(app)

from onelove.tasks import *

celery = onelove.celery
