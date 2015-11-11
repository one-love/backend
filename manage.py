#!/usr/bin/env python
import os

from celery import current_app as celery
from flask import redirect, Flask, url_for
from flask.ext.script import Manager, Server

from onelove import OneLove
from config import configs


config_name = os.getenv('FLASK_CONFIG') or 'default'
app = Flask(__name__, static_folder='onelove/static')
app.config.from_object(configs[config_name])
onelove = OneLove(app)
manager = Manager(app)
manager.add_command(
    "runserver",
    Server(
        host="0.0.0.0",
        use_reloader=True,
        use_debugger=True
    )
)


@app.route('/')
def index():
    return redirect(url_for(onelove.api.endpoint('doc')))


if __name__ == '__main__':
    from datetime import datetime
    current_time = datetime.now()
    current_dir, current_file = os.path.split(__file__)
    livereload_path = os.path.abspath(
        '{}{}'.format(
            current_dir,
            '/../frontend/app/livereload.txt')
    )
    with open(livereload_path, 'w+') as livereload:
        livereload.write(str(current_time))
    manager.run()
