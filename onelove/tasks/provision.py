import zmq.green as zmq
from os import makedirs, path, environ
from shutil import rmtree
from tempfile import mkdtemp, mkstemp
from traceback import print_exc

import yaml
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.galaxy import Galaxy
from ansible.galaxy.role import GalaxyRole
from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from jinja2 import Environment, PackageLoader


class Options(object):
    def __init__(self, **kwargs):
        self.api_server = kwargs.get(
            'api_server',
            'https://galaxy.ansible.com',
        )
        self.ask_pass = kwargs.get('ask_pass', False)
        self.ask_su_pass = kwargs.get('ask_su_pass', False)
        self.ask_sudo_pass = kwargs.get('ask_sudo_pass', False)
        self.ask_vault_pass = kwargs.get('ask_vault_pass', False)
        self.become = kwargs.get('become', False)
        self.become_ask_pass = kwargs.get('become_ask_pass', False)
        self.become_method = kwargs.get('become_method', 'sudo')
        self.become_user = kwargs.get('become_user', 'root')
        self.check = kwargs.get('check', False)
        self.connection = kwargs.get('connection', 'smart')
        self.diff = kwargs.get('diff', False)
        self.extra_vars = kwargs.get('extra_vars', [])
        self.flush_cache = kwargs.get('flush_cache', None)
        self.force_handlers = kwargs.get('force_handlers', False)
        self.forks = kwargs.get('forks', 5)
        self.ignore_certs = kwargs.get('ignore_certs', True)
        self.inventory = kwargs.get('inventory', None)
        self.listhosts = kwargs.get('listhosts', None)
        self.listtags = kwargs.get('listtags', None)
        self.listtasks = kwargs.get('listtasks', None)
        self.module_path = kwargs.get('module_path', None)
        self.new_vault_password_file = kwargs.get(
            'new_vault_password_file',
            None,
        )
        self.output_file = kwargs.get('output_file', None)
        self.private_key_file = kwargs.get('private_key_file', None)
        self.remote_user = kwargs.get('remote_user', 'vagrant')
        self.scp_extra_args = kwargs.get('scp_extra_args', '')
        self.sftp_extra_args = kwargs.get('sftp_extra_args', '')
        self.skip_tags = kwargs.get('skip_tags', None)
        self.ssh_common_args = kwargs.get('ssh_common_args', '')
        self.ssh_extra_args = kwargs.get('ssh_extra_args', '')
        self.start_at_task = kwargs.get('start_at_task', None)
        self.step = kwargs.get('step', None)
        self.su = kwargs.get('su', False)
        self.su_user = kwargs.get('su_user', None)
        self.subset = kwargs.get('subset', None)
        self.sudo = kwargs.get('sudo', False)
        self.sudo_user = kwargs.get('sudo_user', None)
        self.syntax = kwargs.get('syntax', None)
        self.tags = kwargs.get('tags', 'all')
        self.timeout = kwargs.get('timeout', 10)
        self.vault_password_file = kwargs.get('vault_password_file', None)
        self.verbosity = kwargs.get('verbosity', 0)


def render_template(template, **kwargs):
    env = Environment(loader=PackageLoader('onelove.tasks', 'templates'))
    template = env.get_template(template)
    return template.render(**kwargs)


def fetch_role(playbook_path, role_name):
    options = Options()
    options.roles_path = '{playbook_path}/provision/roles'.format(
        playbook_path=playbook_path,
    )
    if not path.exists(options.roles_path):
        makedirs(options.roles_path)
    galaxy = Galaxy(options)
    role = GalaxyRole(galaxy, role_name, path=options.roles_path)
    role.install()
    dependencies = get_application_dependencies(
        playbook_path,
        role_name,
    )
    for role in dependencies:
        fetch_role(playbook_path, role)


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
        dependencies.append(dependency)
    return dependencies


def install_service(playbook_path, cluster, service):
    for application in service.applications:
        fetch_role(playbook_path, application.galaxy_role)

    return service.applications


def generate_playbook(playbook_path, cluster, service):
    pre_tasks = []
    roles = []
    for application in service.applications:
        pre_tasks_file = 'roles/{role}/pre_tasks/main.yml'.format(
            role=application.galaxy_role,
        )
        pre_tasks_path = '{playbook_path}/provision/{pre_tasks_file}'.format(
            playbook_path=playbook_path,
            pre_tasks_file=pre_tasks_file,
        )
        if path.isfile(pre_tasks_path):
            pre_tasks.append(pre_tasks_file)
        roles.append(application.galaxy_role)
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


def get_host_list(playbook_path, cluster):
    result = []
    for provider in cluster.providers:
        result += [host.ip for host in provider.list()]
    return result


def run_playbook(playbook_path, cluster):
    playbook_file = '{playbook_path}/provision/site.yml'.format(
        playbook_path=playbook_path,
    )
    loader = DataLoader()
    variable_manager = VariableManager()
    inventory = Inventory(
        loader=loader,
        variable_manager=variable_manager,
        host_list=get_host_list(playbook_path, cluster),
    )
    file_handle, private_key_file = mkstemp(dir=playbook_path)
    with open(private_key_file, 'w') as key_file:
        key_file.write(cluster.sshKey)
    options = Options(
        inventory=inventory,
        remote_user=cluster.username,
        private_key_file=private_key_file,
    )
    executor = PlaybookExecutor(
        playbooks=[playbook_file],
        inventory=inventory,
        variable_manager=variable_manager,
        loader=loader,
        options=options,
        passwords={
            'become_pass': 'vagrant',
        },
    )
    return executor.run()


def provision(provision_id, config):
    from mongoengine import connect
    from mongoengine.connection import disconnect
    connect(config.MONGODB_DB, host=config.MONGODB_HOST)
    from ..models import Provision

    playbook_path = mkdtemp()
    provision = Provision.objects.get(pk=provision_id)
    provision.status = 'RUNNING'
    provision.save()
    environ['PROVISION_ID'] = str(provision.pk)
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://backend:5500')
    socket.send_json(
        {
            'id': str(provision.id),
            'status': provision.status,
            'type': 'provision',
        }
    )
    socket.recv_json()
    try:
        install_service(playbook_path, provision.cluster, provision.service)
        generate_playbook(playbook_path, provision.cluster, provision.service)
        fail = run_playbook(playbook_path, provision.cluster)
        if (fail):
            provision.status = 'FAILED'
        else:
            provision.status = 'SUCCESS'
    except:
        provision.status = 'FAILED'
        print_exc()
    finally:
        provision.save()
        socket.send_json(
            {
                'id': str(provision.id),
                'status': provision.status,
                'type': 'provision',
            }
        )
        socket.recv_json()
        disconnect()
        rmtree(playbook_path)
