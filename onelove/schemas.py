from marshmallow import Schema, fields, pre_load, post_load, post_dump
from flask_restplus import fields as rest_fields
from .models.auth import User
from .models.all import Service
from .models.parsing import TokenModel
from .api import api


def marshmallowToField(field):
    if type(field) in [fields.Email, fields.String, fields.UUID]:
        return rest_fields.String
    if type(field) in [fields.Bool, fields.Boolean]:
        return rest_fields.Boolean
    if type(field) in [fields.Int, fields.Integer]:
        return rest_fields.Integer
    if type(field) == fields.DateTime:
        return rest_fields.DateTime
    if type(field) == fields.Nested:
        return rest_fields.Nested
    else:
        raise ValueError('Unknown field of type {}'.format(type(field)))


class BaseSchema(Schema):

    __envelope__ = {
        'single': None,
        'many': None,
    }

    def get_envelope_key(self, many):
        """Helper to get the envelope key."""
        key = self.__envelope__['many'] if many else self.__envelope__['single']
        assert key is not None, "Envelope key undefined"
        return key

    @pre_load(pass_many=True)
    def unwrap_envelope(self, data, many):
        key = self.get_envelope_key(many)
        return data[key]

    @post_dump(pass_many=True)
    def wrap_with_envelope(self, data, many):
        key = self.get_envelope_key(many)
        return {key: data}
    @post_load
    def make_object(self, data):
        return self.Meta.model(**data)

    @classmethod
    def fields(cls, required=None):
        marshal_fields = {}
        for name in cls._declared_fields.keys():
            field = cls._declared_fields[name]
            if field.dump_only:
                continue
            fieldType = marshmallowToField(field)
            description = field.metadata.get('description', None)
            if required is None:
                field_required = field.required
            else:
                field_required = required
            marshal_fields[name] = fieldType(
                description=description,
                required=required,
            )
        return api.model(cls.Meta.name, marshal_fields)


class TokenSchema(BaseSchema):
    __envelope__ = {
        'single': 'token',
        'many': 'tokens',
    }
    email = fields.Email(required=True, description='Email')
    password = fields.Str(required=True, description='Password')

    class Meta:
        model = TokenModel
        name = 'Token'


class UserSchema(BaseSchema):
    __envelope__ = {
        'single': 'user',
        'many': 'users',
    }
    id = fields.String(description='ID', dump_only=True)
    email = fields.Email(required=True, description='Email', default='admin@example.com')
    password = fields.Str(required=True, description='Password', load_only=True)
    active = fields.Boolean(default=True)

    class Meta:
        model = User
        name = 'User'

class ServiceSchema(BaseSchema):
    __envelope__ = {
        'single': 'service',
        'many': 'services',
    }
    id = fields.String(description='ID', dump_only=True)
    name = fields.String(required=True, description='Service name')
    # applications = fields.Email(required=True, description='Email')
    # user = fields.Nested(UserSchema)

    class Meta:
        model = Service
        name = 'Service'
