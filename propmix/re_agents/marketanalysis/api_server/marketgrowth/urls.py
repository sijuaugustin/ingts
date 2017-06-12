'''
Created on Jan 23, 2017

@author: vishnu.sk
'''

from django.conf.urls import url, include
from .views import GrowthViewSet
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'growthstats', GrowthViewSet, 'GrowthViewSet')
urlpatterns = [url(r'^', include(router.urls))]
