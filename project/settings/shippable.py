from __future__ import absolute_import
from .common import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'onelove',
        'USER': 'postgres',
        'HOST': 'localhost',
    }
}

INSTALLED_APPS += (
    'django_nose',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-xunit',
    '--xunit-file=shippable/testresults/nosetests.xml',
]
