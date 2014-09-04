from django.conf.urls import patterns, include, url
from django.contrib import admin

from home.views import HomeView


admin.autodiscover()

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
        r'^api/v1/',
        include('api.urls')
    ),
    url(
        r'^api-auth/',
        include(
            'rest_framework.urls',
            namespace='rest_framework'
        )
    ),
)
