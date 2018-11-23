from math import ceil

from flask_restplus import abort
from flask_restplus.reqparse import RequestParser

def_per_page = 10

parser = RequestParser()
parser.add_argument(
    'X-Page',
    default=0,
    help='Page number',
    location='headers',
    required=False,
    type=int,
)
parser.add_argument(
    'X-Per-Page',
    default=def_per_page,
    help='Items per page',
    location='headers',
    required=False,
    type=int,
)


def paginate(query, schema):
    args = parser.parse_args()
    page = args.get('X-Page')
    per_page = args.get('X-Per-Page')
    start = page * per_page
    total = len(query)
    if start > total:
        abort(409, 'Requested range out of boundaries')
    end = start + per_page
    totalPages = ceil(total / float(per_page))
    paginated_query = query[start:end]
    data, errors = schema.dump(paginated_query, many=True)
    if errors:
        abort(409, errors)
    return {
        'data': data,
        'pages': totalPages,
        'total': total,
    }
