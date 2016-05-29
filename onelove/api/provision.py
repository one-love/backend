from flask_restplus import abort

from ..models import Provision
from .fields.provision import fields
from .namespaces import ns_provision
from .resources import ProtectedResource


@ns_provision.route('', endpoint='provisions')
class ProvisionListAPI(ProtectedResource):
    @ns_provision.marshal_with(fields)
    def get(self):
        """Get list of provisions"""
        return [provision for provision in Provision.objects.all()]


@ns_provision.route('/<id>', endpoint='provision')
class ProvisionAPI(ProtectedResource):
    @ns_provision.marshal_with(fields)
    def get(self, id):
        """Find provision by id"""
        try:
            provision = Provision.objects.get(id=id)
        except:
            abort(404, 'No such provision')
        return provision
