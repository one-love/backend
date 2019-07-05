from math import ceil

from flask_rest_api import abort
from marshmallow import fields

from .base import BaseSchema


def paginate(query, pagination):
    page = pagination.get('Page', 0)
    per_page = pagination.get('PerPage', 10)
    start = page * per_page
    total = query.count()
    if start > total:
        abort(409, 'Requested range out of boundaries')
    end = start + per_page
    totalPages = ceil(total / float(per_page))
    data = query[start:end]
    return {
        'data': data,
        'pages': totalPages,
        'total': total,
    }


class PageInSchema(BaseSchema):
    Page = fields.Int()
    PerPage = fields.Int()


def PageOutSchema(schema, *args, **kwargs):
    if schema.__name__[-6:] == 'Schema':
        schema_name = '{}Paginated'.format(schema.__name__[:-6])
    else:
        schema_name = '{}Paginated'.format(schema.__name__)
    schema_fields = {
        'pages': fields.Integer(),
        'total': fields.Integer(),
        'data': fields.List(fields.Nested(schema(*args,
                                                 **kwargs)),
                            many=True)
    }
    return type(schema_name, (BaseSchema, ), schema_fields)
