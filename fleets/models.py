from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify


class Fleet(models.Model):
    name = models.CharField(max_length=256, unique=True)
    url = models.CharField(max_length=2048, unique=True)
    slug = models.SlugField(max_length=256)
    user = models.ForeignKey(get_user_model())

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Fleet, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Application(models.Model):
    name = models.CharField(max_length=256, unique=True)
    repo = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=256)
    fleet = models.ForeignKey(Fleet, related_name='applications')

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Application, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class AmazonProvider(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=256)
    access_key = models.CharField(max_length=256)
    security_key = models.CharField(max_length=256)
    fleet = models.ForeignKey(Fleet, related_name='amazon_providers')

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(AmazonProvider, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name
