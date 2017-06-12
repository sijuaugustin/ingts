'''
Created on Dec 29, 2016

@author: joseph
'''
from django.conf.urls import url, include
from rest_framework import routers
from .views import DemoViewSet
router = routers.DefaultRouter()
router.register(r'demo', DemoViewSet, 'DemoViewSet')
urlpatterns = [url(r'^', include(router.urls))]
