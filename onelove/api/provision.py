from flask import current_app
from flask_restplus import abort

from ..models.provision import Provision
from .namespaces import ns_provision
from .pagination import paginate, parser
from .resources import ProtectedResource
from .schemas import ProvisionSchema
from .utils import call_provision


@ns_provision.route('', endpoint='provisions')
class ProvisionListAPI(ProtectedResource):
    @ns_provision.expect(parser)
    def get(self):
        """List provisions"""
        return paginate(Provision.objects(), ProvisionSchema())

    @ns_provision.expect(ProvisionSchema.fields())
    def post(self):
        """Create provider"""
        schema = ProvisionSchema()
        provision, errors = schema.load(current_app.api.payload)
        if errors:
            return errors, 409
        provision.save()

        response, errors = schema.dump(provision)
        if errors:
            return errors, 409

        call_provision(provision_id=str(provision.id))

        return response


@ns_provision.route('/<provision_id>', endpoint='provision')
class ProvisionAPI(ProtectedResource):
    def get(self, provision_id):
        """Get specific provision"""
        try:
            provision = Provision.objects.get(id=provision_id)
        except Provision.DoesNotExist:
            abort(404, 'No such provision')
        schema = ProvisionSchema()
        data, errors = schema.dump(provision)
        if errors:
            abort(409, errors)
        return data

