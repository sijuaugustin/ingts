'''
Created on Mar 16, 2016

@author: joseph
'''
from django.conf.urls import url, include
from .views import iPriceTrendViewSet, iZipStatusViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'trend', iPriceTrendViewSet, 'iPriceTrendViewSet')
router.register(r'zipstatus', iZipStatusViewSet, 'iZipStatusViewSet')
urlpatterns = [
    url(r'^', include(router.urls)),
]
