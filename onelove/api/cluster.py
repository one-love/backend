import pagination
from base64 import b64decode
from flask import current_app
from flask_jwt import current_identity

from ..models import Cluster, User
from ..utils import check_fields, all_fields_optional
from .fields.cluster import fields, get_fields
from .mixins import ClusterMixin
from .namespaces import ns_cluster
from .resources import ProtectedResource


parser = ns_cluster.parser()
parser.add_argument('name', type=str, required=True, location='json')
parser.add_argument('username', type=str, required=True, location='json')
parser.add_argument('sshKey', type=str, required=True, location='json')


@ns_cluster.route('', endpoint='clusters')
class ClusterListAPI(ProtectedResource):
    @ns_cluster.marshal_with(get_fields)
    @ns_cluster.doc(parser=pagination.parser)
    @ns_cluster.response(200, 'Status OK ')
    def get(self):
        """List clusters"""
        args = pagination.parser.parse_args()
        page = args.get('page')
        per_page = args.get('per_page')

        clusters = Cluster.objects(
            roles__in=current_identity.roles
        ).paginate(page, per_page)
        paging = pagination.Pagination(clusters)
        return clusters.items, 200, paging.headers

    @ns_cluster.doc(body=fields)
    @ns_cluster.marshal_with(get_fields)
    @ns_cluster.response(201, 'Cluster is created')
    def post(self):
        """Create cluster"""
        args = parser.parse_args()
        check_fields(args)
        cluster_name = args.get('name')
        cluster_username = args.get('username')
        cluster_ssh_key = b64decode(args.get('sshKey'))
        cluster = Cluster(
            name=cluster_name,
            username=cluster_username,
            sshKey=cluster_ssh_key,
        )

        admin_role = current_app.onelove.user_datastore.find_or_create_role(
            name='admin_' + cluster_name,
            description="Cluster %s admin" % cluster_name,
            admin=True,
        )
        cluster.roles.append(admin_role)

        user_role = current_app.onelove.user_datastore.find_or_create_role(
            name='user_' + cluster_name,
            description="Cluster %s users" % cluster_name,
            admin=False,
        )
        cluster.roles.append(user_role)
        cluster.save()

        user = User.objects.get(id=current_identity.get_id())

        current_app.onelove.user_datastore.add_role_to_user(user, admin_role)
        return cluster


@ns_cluster.route('/<id>', endpoint='clusters.cluster')
@ns_cluster.doc(params={'id': 'An ID'})
@ns_cluster.response(404, 'Cluster not found')
class ClusterAPI(ProtectedResource, ClusterMixin):
    @ns_cluster.marshal_with(get_fields)
    def get(self, id):
        """Show cluster details"""
        cluster = self._find_cluster(id)
        return cluster

    @ns_cluster.expect(fields)
    @ns_cluster.marshal_with(fields)
    @ns_cluster.expect(fields)
    @ns_cluster.marshal_with(get_fields)
    def patch(self, id):
        """Update cluster"""
        cluster = self._find_cluster(id)
        patch_parser = all_fields_optional(parser)
        args = patch_parser.parse_args()
        cluster.name = args.get('name') or cluster.name
        cluster.username = args.get('username') or cluster.username
        sshKey = args.get('sshKey', None)
        if sshKey is not None:
            cluster.sshKey = b64decode(sshKey)
        cluster.save()
        return cluster

    @ns_cluster.marshal_with(fields)
    def delete(self, id):
        """Delete the cluster."""
        cluster = self._find_cluster(id)
        cluster.delete()
        return cluster
