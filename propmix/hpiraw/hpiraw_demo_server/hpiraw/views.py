'''
Created on Feb 20, 2017

@author: joseph
'''
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt


@method_decorator(xframe_options_exempt, name='dispatch')
class GraphView(TemplateView):
    required_scopes = ['graph']
    template_name = 'hpiraw/index.html'
