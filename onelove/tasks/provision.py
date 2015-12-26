from os import makedirs, path
from shutil import rmtree
from tempfile import mkdtemp

import yaml
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


def fetch_role(playbook_path, role_name):
    options = Options()
    options.roles_path = '{playbook_path}/provision/roles'.format(
        playbook_path=playbook_path,
    )
    if not path.exists:
        makedirs(options.roles_path)
    galaxy = Galaxy(options)
    role = GalaxyRole(galaxy, role_name)
    role.install()


def get_application_dependencies(playbook_path, application_name):
    meta_path_template = '{playbook}/provision/roles/{app}/meta/main.yml'
    meta_path = meta_path_template.format(
        playbook=playbook_path,
        app=application_name,
    )
    with open(meta_path, 'r') as meta_file:
        yaml_meta = yaml.safe_load(meta_file)
    dependencies_meta = yaml_meta['dependencies']
    dependencies = []
    for dependency in dependencies_meta:
        dependencies.append(dependency['roles'])
    return dependencies


def generate_playbook(playbook_path, cluster_id, application_name):
    from ..models import Cluster
    pre_tasks = []
    pre_tasks_file = 'roles/{role}/pre_tasks/main.yml'.format(
        role=application_name,
    )
    pre_tasks_path = '{playbook_path}/provision/{pre_tasks_file}'.format(
        playbook_path=playbook_path,
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
    site_yml_path = '{playbook_path}/provision/site.yml'.format(
        playbook_path=playbook_path,
    )
    with open(site_yml_path, 'w+') as site_yml_file:
        site_yml_file.write(site_yml)
    print(site_yml)


@current_app.task(bind=True)
def provision(self, cluster_id, application_name):
    playbook_path = mkdtemp()
    try:
        fetch_role(playbook_path, application_name)
        dependencies = get_application_dependencies(
            playbook_path,
            application_name,
        )
        for role in dependencies:
            fetch_role(playbook_path, role)
        generate_playbook(playbook_path, cluster_id, application_name)
    finally:
        rmtree(playbook_path)
    return True
