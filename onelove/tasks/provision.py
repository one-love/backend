from os import makedirs, path
from shutil import rmtree
from tempfile import mkdtemp

from ansible.galaxy import Galaxy
from ansible.galaxy.role import GalaxyRole
from celery import current_app
from jinja2 import Environment, PackageLoader


class Options(object):
    roles_path = None
    api_server = 'https://galaxy.ansible.com'
    ignore_certs = True


def render_template(template, **kwargs):
    env = Environment(loader=PackageLoader('onelove.tasks', 'templates'))
    template = env.get_template(template)
    return template.render(**kwargs)


@current_app.task(bind=True)
def provision(self, cluster_id, application_name):
    from ..models import Cluster
    temp_directory = mkdtemp()
    options = Options()
    options.roles_path = '{temp_directory}/provision/roles'.format(
        temp_directory=temp_directory,
    )
    pre_tasks = []
    try:
        makedirs(options.roles_path)
        galaxy = Galaxy(options)
        version = 'master'
        role = GalaxyRole(galaxy, application_name, version=version)
        role.install()
        pre_tasks_file = 'roles/{role}/pre_tasks/main.yml'.format(
            role=application_name,
        )
        pre_tasks_path = '{temp_directory}/provision/{pre_tasks_file}'.format(
            temp_directory=temp_directory,
            pre_tasks_file=pre_tasks_file,
        )
        if path.isfile(pre_tasks_path):
            pre_tasks.append(pre_tasks_file)
        roles = [application_name]
        cluster = Cluster.objects.get(id=cluster_id)
        site_yml = render_template(
            'site.yml',
            pre_tasks=pre_tasks,
            roles=roles,
            cluster=cluster.name,
        )
        site_yml_path = '{temp_directory}/provision/site.yml'.format(
            temp_directory=temp_directory,
        )
        with open(site_yml_path, 'w+') as site_yml_file:
            site_yml_file.write(site_yml)
        print(site_yml)
    finally:
        rmtree(temp_directory)
    return True
