from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns(
    '',
    url(
        r'^create/',
        views.FleetCreate.as_view(),
        name='fleet_create',
    ),
)

