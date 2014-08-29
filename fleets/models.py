from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify


class Application(models.Model):
    name = models.CharField(max_length=256, unique=True)
    repo = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=256)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Application, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Hosting(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=256)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Hosting, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Fleet(models.Model):
    name = models.CharField(max_length=256, unique=True)
    user = models.ForeignKey(get_user_model())
    app = models.ForeignKey(Application, blank=True, null=True)
    hosting = models.ForeignKey(Hosting, blank=True, null=True)
    url = models.CharField(max_length=2048, unique=True)
    slug = models.SlugField(max_length=256)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Fleet, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name
