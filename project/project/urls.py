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

    def get_queryset(self):
    	place = self.request.GET.get("place", None)
    	proper = self.request.GET.get("proper", None)

    	if place is not None:
    		return Place.objects.get_by_place(place)

    	if proper is not None:
    		return Place.objects.get_by_proper(proper)

    	return Place.objects.all()


router = routers.DefaultRouter()
router.register(r'places', PlaceViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^', include(router.urls)),
]
