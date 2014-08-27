from django.db import models
from django.contrib.auth import get_user_model


class FleetType(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name


class Hosting(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name


class Fleet(models.Model):
    name = models.CharField(max_length=256)
    user = models.ForeignKey(get_user_model())
    type = models.ForeignKey(FleetType)
    hosting = models.ForeignKey(Hosting)
    repo = models.CharField(max_length=256)
    url = models.CharField(max_length=2048)

    def __unicode__(self):
        return self.name
