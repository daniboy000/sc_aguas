from django.db import models


class PlaceManager(models.Manager):

    def get_by_place(self, place):
        return Place.objects.filter(place=place)

    def get_by_proper(self, proper):
        return Place.objects.filter(proper=proper)


class Place(models.Model):
    objects = PlaceManager()

    place = models.CharField(max_length=255, default="")
    spot = models.CharField(max_length=255, default="")
    lon = models.FloatField()
    lat = models.FloatField()
    proper = models.CharField(max_length=255, default="")
