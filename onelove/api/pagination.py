from . import api
from flask import request

parser = api.parser()
parser.add_argument('page', type=int, required=False, default=1, help='Page number')
parser.add_argument('per_page', type=int, required=False, default=10, help='Items per page')


class Pagination(object):
    def __init__(self, list):
        self.list = list
        self.page = list.page if list.page is not None else 1
        self.per_page = list.per_page if list.per_page is not None else 10
        self.total = list.total

    @property
    def prev_page(self):
        if self.page == 1:
            prev_page = 1
        else:
            prev_page = self.page - 1
        return prev_page

    @property
    def next_page(self):
        if self.total < self.page * self.per_page:
            next_page = self.page
        else:
            next_page = self.page + 1
        return next_page

    @property
    def last_page(self):
        last_page = (self.total / float(self.per_page))
        return last_page

    @property
    def headers(self):
        first_link = '<%s?page=%d&per_page=%d>; rel="first"' % (request.base_url, 1, self.per_page)
        prev_link = '<%s?page=%d&per_page=%d>; rel="prev"' % (request.base_url, self.prev_page, self.per_page)
        next_link = '<%s?page=%d&per_page=%d>; rel="next"' % (request.base_url, self.next_page, self.per_page)
        last_link = '<%s?page=%d&per_page=%d>; rel="last"' % (request.base_url, self.last_page, self.per_page)

        links = "{0}, {1}, {2}, {3}".format(first_link, prev_link, next_link, last_link)

        headers = {'X-Total-Count': self.total,
                   'Link': links
                   }
        return headers
