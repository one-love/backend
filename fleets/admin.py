from django.contrib import admin
from .models import Fleet, Application, AmazonProvider


admin.site.register(Fleet)
admin.site.register(Application)
admin.site.register(AmazonProvider)
