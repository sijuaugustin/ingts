from django.conf.urls import url, include
from heatmap.views import HeatMapZipAPI
from heatmap.views import HeatMapCountyStateAPI
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'onzip', HeatMapZipAPI, 'HeatMapZipAPI')
router.register(r'onbroad', HeatMapCountyStateAPI, 'HeatMapCountyStateAPI')
urlpatterns = [url(r'^', include(router.urls)), ]
