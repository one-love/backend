from flask_jwt import current_identity
from flask_restplus import abort
from mongoengine.queryset import NotUniqueError
from onelove.api import pagination
from flask import request, current_app


# from .fields.service import fields, get_fields

from ..schemas import ServiceSchema


from .mixins import ServiceMixin
from .namespaces import ns_service
from .resources import ProtectedResource

from ..models.all import Service
# from ..utils import check_fields, all_fields_optional


parser = ns_service.parser()
parser.add_argument('name', type=str, required=True, location='json')


@ns_service.route('', endpoint='services')
class ServiceListAPI(ProtectedResource):
    def get(self):
        """List services"""
        services = Service.objects.all()
        print(services)

        schema = ServiceSchema(many=True)
        response, errors = schema.dump(services)
        print(response)

        if errors:
           abort(409, errors)

        return response, 200

    @ns_service.response(409, 'Service with that name already exists')
    @ns_service.expect(ServiceSchema.fields())
    def post(self):
        """Create service"""
        print("pppppppppppppppppppppppppppppppppp")

        schema = ServiceSchema()
        data, errors = schema.load(current_app.api.payload)
        if errors:
            return errors, 409

        service = Service(name=data.name, user=current_identity.pk)
        print(service)


        try:
            service.save()
        except NotUniqueError:
            abort(409, error='Service with that name already exists')
        response = schema.dump(service)


        return response, 201


# @ns_service.route('/<id>', endpoint='services_service')
# @ns_service.response(404, 'Service not found')
# class ServiceAPI(ProtectedResource, ServiceMixin):
#     @ns_service.marshal_with(get_fields)
#     def get(self, id):
#         """Show service details"""
#         service = self._find_service(id)
#         return service
#
#     @ns_service.expect(fields)
#     @ns_service.marshal_with(get_fields)
#     def patch(self, id):
#         """Update service"""
#         service = self._find_service(id)
#         patch_parser = all_fields_optional(parser)
#         args = patch_parser.parse_args()
#         service.name = args.get('name') or service.name
#         service.save()
#         return service
#
#     @ns_service.marshal_with(get_fields)
#     def delete(self, id):
#         """Delete the service."""
#         service = self._find_service(id)
#         service.delete()
#         return service