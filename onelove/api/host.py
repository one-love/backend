from flask import current_app
from flask_restplus import abort

from .namespaces import ns_provider
from .pagination import paginate, parser
from .resources import ProtectedResource
from .schemas import HostSSHSchema


@ns_provider.route('/<provider_id>/hosts', endpoint='hosts')
class HostListAPI(ProtectedResource):
    @ns_provider.expect(parser)
    def get(self, provider_id):
        """Get list of hosts"""
        provider = self.find_provider(provider_id)
        return paginate(provider.hosts, HostSSHSchema())

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
        response, errors = schema.dump(provider)
        if errors:
            return errors, 409
        return response


@ns_provider.route('/<provider_id>/hosts/<hostname>', endpoint='host')
class HostAPI(ProtectedResource):
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
