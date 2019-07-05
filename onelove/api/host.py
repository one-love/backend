from flask_rest_api import abort

from ..models.provider import HostSSH, Provider
from ..schemas.host import HostSSHSchema
from ..schemas.paging import PageInSchema, PageOutSchema, paginate
from .methodviews import ProtectedMethodView
from .provider import blueprint


@blueprint.route('/<provider_id>/hosts', endpoint='hosts')
class HostListAPI(ProtectedMethodView):
    @blueprint.arguments(PageInSchema(), location='headers')
    @blueprint.response(PageOutSchema(HostSSHSchema))
    def get(self, pagination, provider_id):
        """List hosts"""
        try:
            provider = Provider.objects.get(id=provider_id)
        except Provider.DoesNotExist:
            abort(404, message='No such provider')
        return paginate(provider.hosts, pagination)

    @blueprint.arguments(HostSSHSchema())
    @blueprint.response(HostSSHSchema())
    def post(self, args, provider_id):
        """Create host"""
        try:
            provider = Provider.objects.get(id=provider_id)
        except Provider.DoesNotExist:
            abort(404, message='No such provider')
        host = HostSSH(**args)
        provider.hosts.append(host)
        provider.save()
        return host


@blueprint.route('/<provider_id>/host/<host_name>', endpoint='host')
class HostAPI(ProtectedMethodView):
    @blueprint.response(HostSSHSchema())
    def get(self, provider_id, host_name):
        """Get host details"""
        try:
            provider = Provider.objects.get(id=provider_id)
        except Provider.DoesNotExist:
            abort(404, message='No such provider')
        for host in provider.hosts:
            if host.hostname == host_name:
                return host
        abort(404, 'No such host')

    @blueprint.arguments(HostSSHSchema(partial=True))
    @blueprint.response(HostSSHSchema())
    def patch(self, args, provider_id, host_name):
        """Edit host"""
        try:
            provider = Provider.objects.get(id=provider_id)
        except Provider.DoesNotExist:
            abort(404, message='No such provider')
        for host in provider.hosts:
            if host.hostname == host_name:
                for arg in args:
                    setattr(host, arg, args[arg])
                provider.save()
                return host
        abort(404, message='No such host')

    @blueprint.response(HostSSHSchema())
    def delete(self, provider_id, host_name):
        """Delete host"""
        try:
            provider = Provider.objects.get(id=provider_id)
        except Provider.DoesNotExist:
            abort(404, error='No such provider')
        for host in provider.hosts:
            if host.hostname == host_name:
                provider.hosts.remove(host)
                provider.save()
                return host
        abort(404, message='No such host')
