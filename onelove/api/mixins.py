from flask.ext.restplus import abort
from ..models import Cluster, ProviderSSH
from mongoengine.errors import ValidationError
from flask_jwt import current_identity
from ..models import User
from ..models import Role


class ClusterMixin(object):
    def _find_cluster(self, cluster_id):
        permission = False
        try:
            cluster = Cluster.objects.get(id=cluster_id)
            user = User.objects.get(email=current_identity.email)
            permission = user.has_role('admin')

            if not permission:
                for role in cluster.roles:
                    if user.has_role(role):
                        permission = True

            if permission:
                return cluster
            else:
                abort(403)

        except (Cluster.DoesNotExist, ValidationError):
            abort(404, error='Cluster does not exist')
        except (Role.DoesNotExist):
            abort(401, error='You do not have valid permissions.')

    def _get_provider_class(self, type):
        if type == 'SSH':
            return ProviderSSH
        return None
