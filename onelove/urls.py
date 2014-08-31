from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers

from api import views
from home.views import HomeView


admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'fleets', views.FleetViewSet)
router.register(r'applications', views.ApplicationViewSet)
router.register(r'amazonproviders', views.AmazonProviderViewSet)

urlpatterns = patterns(
    '',
    url(
        r'^$',
        HomeView.as_view(),
        name='home'
    ),
    url(
        r'^logout/',
        'home.views.logout',
        name='logout'
    ),
    url(
        r'^admin/',
        include(admin.site.urls)
    ),
    url(
        r'^fleet/',
        include('fleets.urls'),
    ),
    url(
        r'^api/v1/',
        include(router.urls)
    ),
    url(
        r'^api-auth/',
        include(
            'rest_framework.urls',
            namespace='rest_framework'
        )
    ),
)
