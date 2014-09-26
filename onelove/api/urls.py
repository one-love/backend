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
        ),
    ),
    url(
        r'^$',
        include(
            'rest_framework.urls',
            namespace='rest_framework',
        ),
    ),
    url(
        r'^v1/auth/',
        'rest_framework.authtoken.views.obtain_auth_token',
        name='login',
    )
)
