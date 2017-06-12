'''
Created on Dec 29, 2016

@author: joseph
'''
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import permission_classes


@permission_classes((permissions.AllowAny,))
class DemoViewSet(viewsets.ViewSet):

    def list(self, request):
        return Response({"sample": "sample"})
