'''
Created on Dec 29, 2016

@author: joseph
'''

from django.conf.urls import url, include
from rest_framework import routers
from .views import AgentMonetoryViewSet
from .views import AgentSharePercentViewSet
from .views import AgentSoldToListViewSet

router = routers.DefaultRouter()
router.register(r'monetorystats', AgentMonetoryViewSet, 'AgentMonetoryViewSet')
router.register(r'sharestats', AgentSharePercentViewSet, 'AgentSharePercentViewSet')
router.register(r'slstats', AgentSoldToListViewSet, 'AgentSoldToListViewSet')
urlpatterns = [url(r'^', include(router.urls))]
