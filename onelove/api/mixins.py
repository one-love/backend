from flask_restplus import abort
from mongoengine.errors import ValidationError

from ..models.cluster import Cluster
from ..models.provider import Provider
from ..models.service import Service


class ClusterMixin(object):
    def find_cluster(self, cluster_id):
        try:
            return Cluster.objects.get(id=cluster_id)
        except (Cluster.DoesNotExist, ValidationError):
            abort(404, error='Cluster does not exist')


class ProviderMixin(object):
    def find_provider(self, provider_id):
        try:
            return Provider.objects.get(id=provider_id)
        except (Provider.DoesNotExist, ValidationError):
            abort(404, error='Provider does not exist')


class ServiceMixin(object):
    def find_service(self, service_id):
        try:
            return Service.objects.get(id=service_id)
        except (Service.DoesNotExist, ValidationError):
            abort(404, error='Service does not exist')
