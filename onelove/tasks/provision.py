from os import makedirs
from shutil import rmtree
from tempfile import mkdtemp

from ansible.galaxy import Galaxy
from ansible.galaxy.role import GalaxyRole
from celery import current_app


class Options(object):
    roles_path = None
    api_server = 'https://galaxy.ansible.com'
    ignore_certs = True


@current_app.task(bind=True)
def provision(self, cluster_id, application_name):
    temp_directory = mkdtemp()
    options = Options()
    options.roles_path = '{temp_directory}/provision/roles'.format(
        temp_directory=temp_directory,
    )
    try:
        makedirs(options.roles_path)
        galaxy = Galaxy(options)
        version = 'master'
        role = GalaxyRole(galaxy, application_name, version=version)
        role.install()
    finally:
        rmtree(temp_directory)
    return True
