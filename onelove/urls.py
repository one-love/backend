from django.conf.urls import patterns, include
from tastypie.api import Api

from .api import FleetResource, UserResource


v1_api = Api(api_name='v1')
v1_api.register(FleetResource())
v1_api.register(UserResource())

urlpatterns = patterns(
    '',
    (
        r'^',
        include(v1_api.urls)
    ),
 )
