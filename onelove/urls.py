from django.conf.urls import patterns, include, url

from home.views import HomeView

from django.contrib import admin
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
        r'^provision/',
        include('provision.urls')
    ),
)
