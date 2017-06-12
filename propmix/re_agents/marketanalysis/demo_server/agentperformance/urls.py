'''
Created on Dec 29, 2016

@author: joseph
'''
from django.conf.urls import url
from .views import GraphView

urlpatterns = [url(r'^agentperformance', GraphView.as_view(), name='demo'),
               ]
