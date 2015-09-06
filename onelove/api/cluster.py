from flask.ext.restful import abort, reqparse, fields, marshal_with
from flask_restful_swagger import swagger

import application
import provider
from ..models import Application, Cluster, ProviderSSH
from resources import ProtectedResource


fields = {
    'applications': fields.List(fields.Nested(application.fields)),
    'id': fields.String,
    'name': fields.String,
    'providers': fields.List(fields.Nested(application.fields)),
}


reqparse = reqparse.RequestParser()
reqparse.add_argument('name', type=str, required=True, location='json')


class ClusterMixin(object):
    def _find_cluster(self, cluster_id):
        try:
            cluster = Cluster.objects.get(id=cluster_id)
        except Cluster.DoesNotExist:
            abort(404, error='Cluster does not exist')
        return cluster

    def _find_app(self, cluster_id, application_name):
        try:
            cluster = Cluster.objects.get(id=cluster_id)
        except Cluster.DoesNotExist:
            abort(404, error='Cluster does not exist')
        for app in cluster.applications:
            if app.name == application_name:
                return app
        abort(404, error='Application does not exist')

    def _find_provider(self, cluster_id, provider_name):
        try:
            cluster = Cluster.objects.get(id=cluster_id)
        except Cluster.DoesNotExist:
            abort(404, error='Cluster does not exist')
        for prov in cluster.providers:
            if prov.name == provider_name:
                return prov
        return None

    def _get_provider_class(self, type):
        if type == 'SSH':
            return ProviderSSH
        return None

@swagger.model
class ClusterListAPICreate:
    def __init__(self, name):
        pass

class ClusterListAPI(ProtectedResource):
    @swagger.operation(
        summary='Get a Clusters list',
    )
    @marshal_with(fields)
    def get(self):
        return [cluster for cluster in Cluster.objects.all()]


    @swagger.operation(
        summary='Create the cluster',
        responseClass=ClusterListAPICreate.__name__,
        parameters=[
            {
                "method": "POST",
                "name": "Cluster",
                "description": "Cluster object to create a user",
                "required": True,
                "allowMultiple": False,
                "dataType": ClusterListAPICreate.__name__,
                "paramType": 'body'
            }
            ],
        responseMessages=[
                {
                    "code": 201,
                    "message": "New cluster is created."
                },
                {
                    "code": 400,
                    "message": "Bad request."
                }
            ]
        )
    @marshal_with(fields)
    def post(self):
        args = reqparse.parse_args()
        cluster = Cluster(
            name=args.get('name'),
        )
        cluster.save()
        return cluster, 201


class ClusterAPI(ProtectedResource, ClusterMixin):
    @marshal_with(fields)
    def get(self, id):
        cluster = self._find_cluster(id)
        return cluster

    @marshal_with(fields)
    def put(self, id):
        cluster = self._find_cluster(id)
        args = reqparse.parse_args()
        cluster.name = args.get('name')
        cluster.save()
        return cluster

    @swagger.operation(
        summary='Delete a cluster item by ID',
    )
    @marshal_with(fields)
    def delete(self, id):
        cluster = self._find_cluster(id)
        cluster.delete()
        return cluster


class ClusterApplicationListAPI(ProtectedResource, ClusterMixin):
    @swagger.operation(
        summary='Get list of aplications in the cluster',
    )
    @marshal_with(application.fields)
    def get(self, cluster_id):
        cluster = self._find_cluster(cluster_id)
        return cluster.applications

    @marshal_with(application.fields)
    def post(self, cluster_id):
        cluster = self._find_cluster(cluster_id)
        args = application.reqparse.parse_args()
        application_name = args.get('name')
        app = self._find_app(cluster_id, application_name)
        if app is not None:
            abort(409, error='Application with that name already exists')
        app = Application(name=application_name)
        cluster.applications.append(app)
        cluster.save()
        return cluster.applications


class ClusterApplicationAPI(ProtectedResource, ClusterMixin):
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


class ClusterApplicationProvisionAPI(ProtectedResource, ClusterMixin):
    def post(self, cluster_id, application_name):
        from ..tasks import provision
        result = provision.delay(cluster_id, application_name)
        return {'result': str(result)}


class ClusterProviderListAPI(ProtectedResource, ClusterMixin):
    @marshal_with(provider.fields)
    def get(self, cluster_id):
        cluster = self._find_cluster(cluster_id)
        return cluster.providers

    @marshal_with(provider.fields)
    def post(self, cluster_id):
        args = provider.reqparse.parse_args()
        provider_name = args.get('name')
        provider_type = args.get('type')
        prov = self._find_provider(cluster_id, provider_name)
        if prov is not None:
            abort(409, error='Provider with that name already exists')
        Provider = self._get_provider_class(provider_type)
        prov = Provider(name=provider_name)
        cluster = self._find_cluster(cluster_id)
        cluster.providers.append(prov)
        cluster.save()
        return cluster.providers


class ClusterProviderAPI(ProtectedResource, ClusterMixin):
    @marshal_with(provider.fields)
    def get(self, cluster_id, provider_name):
        return self._find_provider(cluster_id, provider_name)

    @marshal_with(provider.fields)
    def put(self, cluster_id, provider_name):
        args = provider.reqparse.parse_args()
        prov = self._find_provider(cluster_id, provider_name)
        prov.name = args.get('name')
        prov.save()
        return prov

    @marshal_with(provider.fields)
    def patch(self, cluster_id, provider_name):
        args = provider.reqparse.parse_args()
        prov = self._find_provider(cluster_id, provider_name)
        prov.name = args.get('name', prov.name)
        prov.save()
        return prov

    @marshal_with(provider.fields)
    def delete(self, cluster_id, provider_name):
        prov = self._find_provider(cluster_id, provider_name)
        cluster = Cluster.objects.get(id=cluster_id)
        cluster.providers.remove(prov)
        cluster.providers.save()
        return prov
