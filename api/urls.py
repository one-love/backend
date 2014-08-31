from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    url(
        r'^fleet/$',
        views.FleetList.as_view(),
        name='fleet_list'
    ),
    url(
        r'^fleet/(?P<id>[0-9]+)/$',
        views.FleetDetail.as_view(),
        name='fleet_detail'
    ),
)
