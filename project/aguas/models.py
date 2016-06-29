from django.db import models


class Place(models.Model):
    place = models.CharField(max_length=255)
    lon = models.FloatField()
    lat = models.FloatField()
    proper = models.BooleanField()

    def __unicode__(self):
        return u"{} - {}/{} - {}".format(self.place, self.lat,
                                         self.lon, self.state)

    @property
    def state(self):
        if self.proper:
            return u"proper"
        return u"not proper"
