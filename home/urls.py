from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^$', 'home.views.home', name='home'),
)
