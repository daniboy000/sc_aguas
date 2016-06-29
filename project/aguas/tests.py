from django.test import TestCase

from .models import Place


class TestPlace(TestCase):
    def test_unicode(self):
        place = Place(
            place="FRENTE AO ACESSO PARA O RIO TAVARES",
            proper=True,
            lat=-27.6066033943,
            lon=48.4620203034,
        )
        expected = u"FRENTE AO ACESSO PARA O RIO TAVARES - "
        expected += "-27.6066033943/48.4620203034 - proper"
        self.assertEqual(unicode(place), expected)
