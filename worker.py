#!/usr/bin/env python
import os
from flask_mongoengine import MongoEngine

from onelove.utils import create_app
from onelove.worker import run
from config import configs


project_root = os.path.dirname(os.path.abspath(__file__))
config_name = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(config_name)
db = MongoEngine(app)
run(project_root, configs[config_name])
