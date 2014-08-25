from django.contrib import admin
from .models import Fleet, FleetType, Hosting


admin.site.register(Fleet)
admin.site.register(FleetType)
admin.site.register(Hosting)
