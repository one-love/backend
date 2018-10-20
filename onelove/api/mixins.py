from flask_restplus import abort
from mongoengine.errors import ValidationError

from ..models.auth import Role, User
from ..models.cluster import Cluster
from ..models.provider import Provider
from ..models.service import Service


class ClusterMixin(object):
    def find_cluster(self, cluster_id, email):
        permission = False
        try:
            cluster = Cluster.objects.get(id=cluster_id)
            user = User.objects.get(email=email)
            permission = user.has_role('admin')

            if not permission:
                for role in cluster.roles:
                    if user.has_role(role):
                        permission = True

            if permission:
                return cluster
            abort(403)
        except (Cluster.DoesNotExist, ValidationError):
            abort(404, error='Cluster does not exist')
        except (Role.DoesNotExist):
            abort(401, error='You do not have valid permissions.')


class ProviderMixin(object):
    def find_provider(self, provider_id):
        try:
            return Provider.objects.get(id=provider_id)
        except (Provider.DoesNotExist, ValidationError):
            abort(404, error='Service does not exist')


class ServiceMixin(object):
    def find_service(self, service_id):
        try:
            return Service.objects.get(id=service_id)
        except (Service.DoesNotExist, ValidationError):
            abort(404, error='Service does not exist')
