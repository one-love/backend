from . import api


def_per_page = 10


parser = api.parser()
parser.add_argument(
    'X-Page',
    type=int,
    required=False,
    default=1,
    help='Page number',
    location='headers'
)
parser.add_argument(
    'X-Per-Page',
    type=int,
    required=False,
    default=def_per_page,
    help='Items per page',
    location='headers'
)


def pages():
    args = parser.parse_args()
    page = args.get('X-Page')
    per_page = args.get('X-Per-Page')
    return(page, per_page)


class Pagination(object):
    def __init__(self, list):
        self.list = list
        self.page = list.page if list.page else 1
        self.per_page = list.per_page if list.per_page else def_per_page
        self.total = list.total

    @property
    def last_page(self):
        last_page = ((self.total - 1) / self.per_page) + 1
        return last_page

    @property
    def headers(self):
        headers = {'X-Total-Count': self.total,
                   'X-First-Page': '1',
                   'X-Last-Page': self.last_page
                   }
        return headers