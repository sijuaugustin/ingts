
from django.conf.urls import url, include
from django.contrib.auth.models import User
from .views import heatap, HeatapS
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'heatvalue', heatap, 'heatap')
router.register(r'heatstate', HeatapS, 'state')
urlpatterns = [
    url(r'^', include(router.urls)),
]
