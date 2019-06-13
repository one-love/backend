from marshmallow import fields

from .base import BaseSchema


class TokenSchema(BaseSchema):
    email = fields.Email(required=True, description='Email')
    password = fields.Str(required=True, description='Password')


class RoleSchema(BaseSchema):
    id = fields.Integer(description='ID', dump_only=True)
    description = fields.String(required=True, description='Description')
    name = fields.String(required=True, description='Name')


class UserSchema(BaseSchema):
    id = fields.String(description='ID', dump_only=True)
    email = fields.Email(required=True, description='Email')
    password = fields.Str(
        required=True,
        description='Password',
        load_only=True
    )
    active = fields.Boolean()
    admin = fields.Boolean()


class RefreshSchema(BaseSchema):
    access = fields.Str()
    accessExpire = fields.Integer()
    refreshExpire = fields.Integer()


class LoginSchema(RefreshSchema):
    refresh = fields.Str()
