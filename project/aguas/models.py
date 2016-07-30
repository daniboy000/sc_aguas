from django.db import models


class Place(models.Model):
    place = models.CharField(max_length=255, default="")
    spot = models.CharField(max_length=255, default="")
    lon = models.FloatField()
    lat = models.FloatField()
    proper = models.CharField(max_length=255, default="")
