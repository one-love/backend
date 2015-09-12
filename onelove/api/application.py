from flask.ext.restplus import abort
from resources import ProtectedResource
from ..models import Application, Cluster
from . import api
from .mixins import ClusterMixin
from .namespaces import ns_cluster
from .fields import application_fields as fields


parser = api.parser()
parser.add_argument('application_name', type=str, required=True, location='json')
parser.add_argument('galaxy_role', type=str, required=True, location='json')
parser.add_argument('name', type=str, required=True, location='json')


@ns_cluster.route('/<cluster_id>/applications', endpoint='api/cluster/applications')
class ClusterApplicationListAPI(ProtectedResource, ClusterMixin):
    @api.marshal_with(fields)
    def get(self, cluster_id):
        """Get list of a aplications for the cluster"""
        cluster = self._find_cluster(cluster_id)
        return cluster.applications

    @api.expect(fields)
    @api.marshal_with(fields)
    def post(self, cluster_id):
        """Create aplication for the cluster"""
        cluster = self._find_cluster(cluster_id)
        args = parser.parse_args()
        application_name = args.get('name')
        app = self._find_app(cluster_id, application_name)
        if app is not None:
            abort(409, error='Application with that name already exists')
        app = Application(name=application_name)
        cluster.applications.append(app)
        cluster.save()
        return cluster.applications


@ns_cluster.route('/<cluster_id>/applications/<application_name>', endpoint='api/cluster/application')
class ClusterApplicationAPI(ProtectedResource, ClusterMixin):
    @api.marshal_with(fields)
    def get(self, cluster_id, application_name):
        return self._find_app(cluster_id, application_name)

    @api.expect(fields)
    @api.marshal_with(fields)
    def put(self, cluster_id, application_name):
        args = parser.parse_args()
        app = self._find_app(cluster_id, application_name)
        app.name = args.get('name')
        app.save()
        return app

    @api.marshal_with(fields)
    def delete(self, cluster_id, application_name):
        app = self._find_app(cluster_id, application_name)
        cluster = Cluster.objects.get(id=cluster_id)
        cluster.applications.remove(app)
        cluster.applications.save()
        return app


@ns_cluster.route('/<cluster_id>/applications/<application_name>/provision', endpoint='api/cluster/application/provision')
class ClusterApplicationProvisionAPI(ProtectedResource, ClusterMixin):
    @api.expect(fields)
    @api.marshal_with(fields)
    def post(self, cluster_id, application_name):
        from ..tasks import provision
        result = provision.delay(cluster_id, application_name)
        return {'result': str(result)}
