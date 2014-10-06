from __future__ import absolute_import
from .common import *

INSTALLED_APPS += (
    'django_extensions',
    'django_nose',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=onelove',
]
