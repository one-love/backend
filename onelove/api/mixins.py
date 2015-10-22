from flask.ext.restplus import abort
from ..models import Cluster, ProviderSSH
from mongoengine.errors import ValidationError
from flask_jwt import current_identity
from ..models import User


class ClusterMixin(object):
    def _find_cluster(self, cluster_id):
        try:
            cluster = Cluster.objects.get(id=cluster_id)
            if current_identity.has_role(cluster.name):
                return cluster
            else:
                abort(403)
        except (Cluster.DoesNotExist, ValidationError):
            abort(404, error='Cluster does not exist')

    def _find_app(self, cluster_id, application_name):
        try:
            cluster = Cluster.objects.get(id=cluster_id)
        except (Cluster.DoesNotExist, ValidationError):
            abort(404, error='Cluster does not exist')
        for app in cluster.applications:
            if app.name == application_name:
                return app
        return None

    def _find_provider(self, cluster_id, provider_name):
        try:
            cluster = Cluster.objects.get(id=cluster_id)
        except (Cluster.DoesNotExist, ValidationError):
            abort(404, error='Cluster does not exist')
        for prov in cluster.providers:
            if prov.name == provider_name:
                return prov
        return None

    def _get_provider_class(self, type):
        if type == 'SSH':
            return ProviderSSH
        return None
