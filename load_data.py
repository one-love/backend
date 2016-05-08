#!/usr/bin/env python
from create_default_admin import user, admin_role
from onelove.factories import ClusterFactory, ServiceFactory
from onelove.utils import eprint


cluster = ClusterFactory()
cluster.roles.append(admin_role)
service = ServiceFactory(user=user)
service.save()

with open('keys/onelove') as mykey:
    cluster.sshKey = mykey.read()
    eprint(cluster.sshKey)

cluster.services.append(service)
cluster.save()
