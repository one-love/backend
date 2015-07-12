import os

from flask.ext.script import Manager, Server

from app import create_app


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
manager.add_command("runserver", Server(host="0.0.0.0", use_reloader=True))
