from flask.ext.restful import Resource, abort, reqparse, fields, marshal_with

from ..models import Cluster
import application


fields = {
    'applications': fields.List(fields.Nested(application.fields)),
    'id': fields.String,
    'name': fields.String,
}


reqparse = reqparse.RequestParser()
reqparse.add_argument('name', type=str, required=True, location='json')


class ClusterListAPI(Resource):
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


class ClusterAPI(Resource):
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


class ClusterApplicationListAPI(Resource):
    """
    List all applications beloging to a single cluster
    """
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
        app = application.Application()
        app.name = args.get('name')
        cluster.applications.append(app)
        cluster.save()
        return cluster.applications
