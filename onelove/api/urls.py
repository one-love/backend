from django.conf.urls import patterns, url, include
from . import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'fleets', views.FleetViewSet)
router.register(r'applications', views.ApplicationViewSet)
router.register(r'providers', views.ProviderViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browseable API.
urlpatterns = patterns('',
    url(r'^v1/', include(router.urls)),
    url(r'', include('rest_framework.urls', namespace='rest_framework'))
)
