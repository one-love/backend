from flask import current_app
from flask_restplus import abort
from flask_restplus.reqparse import RequestParser

from .namespaces import ns_provider
from .pagination import paginate, parser
from .resources import ProtectedResource
from .schemas import HostSSHSchema
from .mixins import ProviderMixin


host_parser = parser.copy()

host_parser.add_argument(
    'by_tags',
    help='Tags',
    location='args',
    required=False,
    type=str,
    action='append',
)


@ns_provider.route('/<provider_id>/hosts', endpoint='hosts')
class HostListAPI(ProtectedResource, ProviderMixin):
    @ns_provider.expect(host_parser)
    def get(self, provider_id):
        """Get list of hosts"""
        args = host_parser.parse_args()

        provider = self.find_provider(provider_id)

        if args['by_tags']:
            tags = (args['by_tags'])
            hosts = provider.hosts_by_tag(tags)
        else:
            hosts = provider.hosts

        return paginate(hosts, HostSSHSchema())
        # return paginate(provider.hosts, HostSSHSchema())

    @ns_provider.expect(HostSSHSchema.fields())
    def post(self, provider_id):
        """Create provider"""
        provider = self.find_provider(provider_id)
        schema = HostSSHSchema()
        host, errors = schema.load(current_app.api.payload)
        if errors:
            return errors, 409
        provider.hosts.append(host)
        provider.save()
        response, errors = schema.dump(host)
        if errors:
            return errors, 409
        return response


@ns_provider.route('/<provider_id>/hosts/<hostname>', endpoint='host')
class HostAPI(ProtectedResource, ProviderMixin):
    def get(self, provider_id, hostname):
        """Get provider details"""
        provider = self.find_provider(provider_id)
        schema = HostSSHSchema()
        for host in provider.hosts:
            if host.hostname == hostname:
                response, errors = schema.dump(host)
                if errors:
                    return errors, 409
                return response
        abort(404, error='No such host')

    @ns_provider.expect(HostSSHSchema.fields(required=False))
    def patch(self, provider_id, hostname):
        """Change provider details"""
        provider = self.find_provider(provider_id)
        schema = HostSSHSchema()
        for host in provider.hosts:
            if host.hostname == hostname:
                data, errors = schema.load(current_app.api.payload)
                if errors:
                    return errors, 409
                host.hostname = data.hostname or host.hostname
                host.ip = data.ip or host.ip
                response, errors = schema.dump(host)
                if errors:
                    return errors, 409
                host.save()
                return response
        abort(404, error='No such host')

    def delete(self, provider_id, hostname):
        """Delete the provider"""
        provider = self.find_provider(provider_id)
        schema = HostSSHSchema()
        for host in provider.hosts:
            if host.hostname == hostname:
                response, errors = schema.dump(host)
                if errors:
                    return errors, 409
                host.delete()
                return response
        abort(404, error='No such host')
