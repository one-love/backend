from django.conf.urls import patterns, include, url
from django.contrib import admin

from onelove.views import HomeView


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
        'onelove.views.logout',
        name='logout'
    ),
    url(
        r'^api/',
        include('onelove.urls')
    )
)
