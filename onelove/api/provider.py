from ..models.provider import Provider
from .namespaces import ns_provider
from .pagination import paginate, parser
from .resources import ProtectedResource
from .schemas import ProviderSchema


@ns_provider.route('', endpoint='providers')
class ProviderListAPI(ProtectedResource):
    @ns_provider.expect(parser)
    def get(self):
        """Get list of a providers"""
        return paginate(Provider.objects(), ProviderSchema())
