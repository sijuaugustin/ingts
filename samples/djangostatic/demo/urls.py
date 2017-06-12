'''
Created on Dec 29, 2016

@author: joseph
'''
from django.conf.urls import url, include
from django.views.generic import TemplateView

urlpatterns = [url(r'^demo', TemplateView.as_view(template_name='index.html'), name='demo'),
]
