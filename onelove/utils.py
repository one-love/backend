from copy import deepcopy
from glob import glob
from os import getcwd, chdir, getenv, makedirs
from os.path import abspath, splitext, exists, dirname
from importlib import import_module
from shutil import copy

from flask import Flask
from flask_restplus import abort

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
    my_directory = os.path.dirname(__file__)
    projects_root = os.path.abspath(my_directory + '../../..')
    frontend_file_path = projects_root + '/frontend/src/backend_url.js'
    with open(frontend_file_path, 'w+') as frontend_file:
        content = "export const SOCKETIO_URL = '{url}/onelove';\n".format(
            url=url
        )
        frontend_file.write(content)
    with open(frontend_file_path, 'a') as frontend_file:
        content = "export const API_URL = '{url}/api/v0';\n".format(url=url)
        frontend_file.write(content)


def reload_celery(celery):
    celery.control.broadcast('pool_restart', arguments={'reload': True})


def import_neighbour_modules(imported_module, package):
    module_root = abspath(imported_module + '/..')
    pattern = '*.py'
    old_cwd = getcwd()

    chdir(module_root)
    file_abs_path = abspath(imported_module)
    for module in glob(pattern):
        module_abs_path = abspath(module)
        if file_abs_path != module_abs_path and module != '__init__.py':
            real_module = '.' + splitext(module)[0]
            import_module(real_module, package)
    chdir(old_cwd)


def check_fields(args):
    for key in args.keys():
        if args[key] is '':
            abort(409, "'%s' can not be empty string" % key)


def all_fields_optional(parser):
    new_parser = deepcopy(parser)
    for arg in new_parser.args:
        arg.required = False
    return new_parser


def copy_callbacks(destination):
    project_root = abspath(dirname(__file__))
    callbacks_root = '%s/callbacks' % project_root
    callbacks = [
        'onelove',
    ]
    for callback in callbacks:
        callback_path = '%s/%s.py' % (callbacks_root, callback)
        copy(callback_path, destination)


def setup_ansible_callbacks():
    home = abspath(getenv('HOME', ''))
    callback_dir = '%s/%s' % (home, '.ansible/plugins/callback')
    if not exists(callback_dir):
        makedirs(callback_dir)
    copy_callbacks(callback_dir)
