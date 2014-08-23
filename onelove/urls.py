from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(
        r'^$',
        'bootstrap.views.home',
        name='home'
    ),
    url(
        r'^logout/$',
        'bootstrap.views.logout',
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
