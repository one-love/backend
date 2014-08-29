from django.db import models
from django.contrib.auth import get_user_model


class Application(models.Model):
    name = models.CharField(max_length=256)
    repo = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name


class Hosting(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name


class Fleet(models.Model):
    name = models.CharField(max_length=256)
    user = models.ForeignKey(get_user_model())
    app = models.ForeignKey(Application, blank=True, null=True)
    hosting = models.ForeignKey(Hosting, blank=True, null=True)
    url = models.CharField(max_length=2048)

    def __unicode__(self):
        return self.name
