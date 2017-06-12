'''
Created on Dec 29, 2016

@author: joseph
'''
from django.conf.urls import url
from .views import GraphView

urlpatterns = [url(r'^data', GraphView.as_view(),
                   name='dom'),
               ]
