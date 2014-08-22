from __future__ import absolute_import
from .common import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'onelove',
        'USER': 'onelove',
        'HOST': 'localhost',
    }
}
