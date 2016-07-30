from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers, serializers, viewsets

from aguas.models import Place


class PlaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Place
        fields = ('place', 'spot', 'lat', 'lon', 'proper')


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


router = routers.DefaultRouter()
router.register(r'places', PlaceViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^', include(router.urls)),
]
