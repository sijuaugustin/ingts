from django.conf.urls import url, include
from .views import heatap
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'heatvalue', heatap, 'heatap')

urlpatterns = [
    url(r'^', include(router.urls)),
]
