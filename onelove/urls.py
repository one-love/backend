from django.conf.urls import patterns, include, url
from tastypie.api import Api
from .api import FleetResource

v1_api = Api(api_name='v1')
v1_api.register(FleetResource())

urlpatterns = patterns('',
    (r'^', include(v1_api.urls)),
                       )
