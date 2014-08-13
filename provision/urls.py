from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'provision.views.home', name='provision-home'),
)
