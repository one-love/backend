from flask.ext.restful import Resource, reqparse, fields, marshal_with

from ..models import Cluster
import application


fields = {
    'id': fields.String,
    'name': fields.String,
    'applications': fields.List(fields.Nested(application.fields)),
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
            return {'message': 'Cluster does not exist'}
        return cluster

    @marshal_with(fields)
    def put(self, id):
        args = reqparse.parse_args()
        cluster = Cluster.objects.get(id=id)
        cluster.name = args.get('name')
        cluster.save()
        return cluster

    def delete(self, id):
        try:
            cluster = Cluster.objects.get(id=id)
        except Cluster.DoesNotExist:
            return {'message': 'Cluster does not exist'}
        cluster.delete()
        return {'message': 'deleted'}
