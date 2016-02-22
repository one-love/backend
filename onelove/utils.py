from flask import Flask
from config import configs


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(configs[config_name])
    return app


def reload_frontend():
    """
    reload frontend
    """
    import getpass
    import os

    username = getpass.getuser()
    port = '5000'
    host = 'localhost'
    if username == 'vagrant':
        host = 'onelove.vagrant'
    url = 'http://{host}:{port}'.format(host=host, port=port)
    content = "export const API_URL = '{url}/api/v0';\n".format(url=url)
    my_directory = os.path.dirname(__file__)
    projects_root = os.path.abspath(my_directory + '../../..')
    frontend_file_path = projects_root + '/frontend/src/backend_url.js'
    with open(frontend_file_path, 'w+') as frontend_file:
        frontend_file.write(content)
