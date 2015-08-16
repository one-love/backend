from flask.ext.restful import abort, reqparse, fields, marshal_with

import application
from ..models import Cluster
from resources import ProtectedResource


fields = {
    'applications': fields.List(fields.Nested(application.fields)),
    'id': fields.String,
    'name': fields.String,
}


reqparse = reqparse.RequestParser()
reqparse.add_argument('name', type=str, required=True, location='json')


class ClusterListAPI(ProtectedResource):
    @marshal_with(fields)
    def get(self):
        return [cluster for cluster in Cluster.objects.all()]

    @marshal_with(fields)
    def post(self):
        args = reqparse.parse_args()
        cluster = Cluster(
            name=args.get('name'),
        )
        cluster.save()
        return cluster


class ClusterAPI(ProtectedResource):
    @marshal_with(fields)
    def get(self, id):
        try:
            cluster = Cluster.objects.get(id=id)
        except Cluster.DoesNotExist:
            abort(404, error='Cluster does not exist')
        return cluster

    @marshal_with(fields)
    def put(self, id):
        try:
            cluster = Cluster.objects.get(id=id)
        except Cluster.DoesNotExist:
            abort(404, error='Cluster does not exist')
        args = reqparse.parse_args()
        cluster.name = args.get('name')
        cluster.save()
        return cluster

    @marshal_with(fields)
    def delete(self, id):
        try:
            cluster = Cluster.objects.get(id=id)
        except Cluster.DoesNotExist:
            abort(404, error='Cluster does not exist')
        cluster.delete()
        return cluster


class ClusterApplicationListAPI(ProtectedResource):
    """
    List all applications beloging to a single cluster
    """
    def _find_app(self, cluster_id, application_name):
        try:
            cluster = Cluster.objects.get(id=cluster_id)
        except Cluster.DoesNotExist:
            abort(404, error='Cluster does not exist')
        for app in cluster.applications:
            if app.name == application_name:
                return app
        return None

    @marshal_with(application.fields)
    def get(self, cluster_id):
        try:
            cluster = Cluster.objects.get(id=cluster_id)
        except Cluster.DoesNotExist:
            abort(404, error='Cluster does not exist')
        return cluster.applications

    @marshal_with(application.fields)
    def post(self, cluster_id):
        try:
            cluster = Cluster.objects.get(id=cluster_id)
        except Cluster.DoesNotExist:
            abort(404, error='Cluster does not exist')
        args = application.reqparse.parse_args()
        application_name = args.get('name')
        app = self._find_app(cluster_id, application_name)
        if app is not None:
            abort(409, error='Application with that name already exists')
        app = application.Application(name=application_name)
        cluster.applications.append(app)
        cluster.save()
        return cluster.applications


class ClusterApplicationAbstractAPI(ProtectedResource):
    def _find_app(self, cluster_id, application_name):
        try:
            cluster = Cluster.objects.get(id=cluster_id)
        except Cluster.DoesNotExist:
            abort(404, error='Cluster does not exist')
        for app in cluster.applications:
            if app.name == application_name:
                return app
        abort(404, error='Application does not exist')


class ClusterApplicationAPI(ClusterApplicationAbstractAPI):
    @marshal_with(application.fields)
    def get(self, cluster_id, application_name):
        return self._find_app(cluster_id, application_name)

    @marshal_with(application.fields)
    def put(self, cluster_id, application_name):
        args = application.reqparse.parse_args()
        app = self._find_app(cluster_id, application_name)
        app.name = args.get('name')
        app.save()
        return app

    @marshal_with(application.fields)
    def delete(self, cluster_id, application_name):
        app = self._find_app(cluster_id, application_name)
        cluster = Cluster.objects.get(id=cluster_id)
        cluster.applications.remove(app)
        cluster.applications.save()
        return app


class ClusterApplicationProvisionAPI(ClusterApplicationAbstractAPI):
    def post(self, cluster_id, application_name):
        from ..tasks import provision
        result = provision.delay(cluster_id, application_name)
        return {'result': str(result)}
