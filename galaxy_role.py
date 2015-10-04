#!/usr/bin/env python
from ansible.galaxy import Galaxy
from ansible.galaxy.role import GalaxyRole
from ansible.galaxy.api import GalaxyAPI


class Options(object):
    roles_path = '/tmp/roles'
    api_server = 'https://galaxy.ansible.com'
    validate_certs = False


options = Options()
role_name = 'meka.postgresql'
galaxy = Galaxy(options)
api = GalaxyAPI(galaxy, options.api_server)
api_role = api.lookup_role_by_name(role_name)
version = 'master'
try:
    version = api_role['summary_fields']['versions'][0]['name']
except:
    pass
role = GalaxyRole(galaxy, role_name, version=version)
galaxy.add_role(role)
role_data = role.fetch(api_role)
role.install(role_data)
