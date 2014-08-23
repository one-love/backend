from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(
        r'^$',
        'provision.views.home',
        name='provision_home'
    ),
    url(
        r'inventory/$',
        'provision.views.inventory',
        name='provision_inventory'
    ),
)
