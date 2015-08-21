from flask.ext.restful import fields, reqparse


fields = {
    'name': fields.String,
    'type': fields.String,
}


reqparse = reqparse.RequestParser()
reqparse.add_argument('name', type=str, required=True, location='json')
reqparse.add_argument('type', type=str, required=True, location='json')
