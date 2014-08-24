from django.db import models


class Fleet(models.Model):
    type = models.CharField(max_length=256)
    hosting = models.CharField(max_length=256)
    repo = models.CharField(max_length=256)
