from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'fleets', views.FleetViewSet)
router.register(r'applications', views.ApplicationViewSet)
router.register(r'providers', views.ProviderViewSet)

urlpatterns = patterns(
    '',
    url(
        r'^v1/',
        include(
            router.urls,
            namespace='v1',
        ),
    ),
    url(
        r'^$',
        include(
            'rest_framework.urls',
            namespace='rest_framework',
        ),
    ),
)
