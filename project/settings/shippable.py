from __future__ import absolute_import
from .common import *

DATABASES['default']['NAME'] = 'onelove'
DATABASES['default']['HOST'] = 'localhost'

INSTALLED_APPS += (
    'django_nose',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-xunit',
    '--xunit-file=shippable/testresults/nosetests.xml',
]
