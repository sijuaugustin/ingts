# from oauth2_provider.views.mixins import ScopedResourceMixin
# from oauth2_provider.views.generic import ProtectedTemplateView
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt


# class GraphView(ScopedResourceMixin, ProtectedTemplateView):
@method_decorator(xframe_options_exempt, name='dispatch')
class GraphView(TemplateView):
    required_scopes = ['graph']
    template_name = 'index.html'
