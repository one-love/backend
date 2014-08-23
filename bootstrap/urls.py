from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'logout/', 'bootstrap.views.logout', name='logout'),
)
