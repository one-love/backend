from flask.ext.restful import fields, reqparse


fields = {
    'application_name': fields.String,
    'galaxy_role': fields.String,
    'name': fields.String,
}


reqparse = reqparse.RequestParser()
reqparse.add_argument('application_name', type=str, required=True, location='json')
reqparse.add_argument('galaxy_role', type=str, required=True, location='json')
reqparse.add_argument('name', type=str, required=True, location='json')
