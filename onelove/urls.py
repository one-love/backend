from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter

from . import views


router_v1 = DefaultRouter()
router_v1.register(r'applications', views.ApplicationViewSet)
router_v1.register(r'fleets', views.FleetViewSet, base_name='fleet')
router_v1.register(r'groups', views.GroupViewSet)
router_v1.register(r'providers', views.ProviderViewSet)
router_v1.register(r'users', views.UserViewSet)

urlpatterns = patterns(
    '',
    url(
        r'^v1/',
        include(
            router_v1.urls,
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
        r'^v1/me/',
        views.MeView.as_view(),
        name='me',
    ),
    url(
        r'^v1/auth/',
        'rest_framework_jwt.views.obtain_jwt_token',
        name='login',
    ),
)
