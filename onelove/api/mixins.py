from flask_restplus import abort
from mongoengine.errors import ValidationError

# from ..models import Cluster
from ..models.service import Service

# class ClusterMixin(object):
#     def _find_cluster(self, cluster_id):
#         permission = False
#         try:
#             cluster = Cluster.objects.get(id=cluster_id)
#             user = User.objects.get(email=current_identity.email)
#             permission = user.has_role('admin')
#
#             if not permission:
#                 for role in cluster.roles:
#                     if user.has_role(role):
#                         permission = True
#
#             if permission:
#                 return cluster
#             else:
#                 abort(403)
#
#         except (Cluster.DoesNotExist, ValidationError):
#             abort(404, error='Cluster does not exist')
#         except (Role.DoesNotExist):
#             abort(401, error='You do not have valid permissions.')
#
#     def _get_provider_class(self, provider_type):
#         return current_app.config['PROVIDERS'].get(provider_type, None)


class ServiceMixin(object):
    def _find_service(self, service_id):
        try:
            service = Service.objects.get(id=service_id)
            return service
        except (Service.DoesNotExist, ValidationError):
            abort(404, error='Service does not exist')
