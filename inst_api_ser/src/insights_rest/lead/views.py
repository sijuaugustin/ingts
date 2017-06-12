'''
Created on Mar 1, 2017

@author: revathy.sivan
'''
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from pymongo import MongoClient
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
db_client = MongoClient("mongo-slave.propmix.io", port=33017)

@permission_classes((permissions.AllowAny,))
class LeadData(viewsets.ViewSet):

    def list(self, request):
        """
        Lead API

        API will return the lead property information.

        ---
        # YAML (must be separated by `---`)

        type:
          schema : { offmarket properties: [{criteria: []}]}
          offmarket properties:
            required: false
            type: string
        parameters_strategy: merge
        omit_parameters:
            - path
        parameters:
            - name: criteria
              description: To get property belongs to particular  criteria.
              required: true
              type: string
              paramType: query
              defaultValue: leadcriteria1
            - name: span
              description: To get property belongs to particular  span.
              required: true
              paramType: query
              defaultValue: last 12 Month
            - name: post
              description: To identify property belong to particular region
              required: true
              paramType: query
              defaultValue: 85050


        responseMessages:
            - code: 401
              message: Not authenticated
            - code : 404
              message: Not Found
            - code : ERROR
              message : No post Specified or Invalid post

        consumes:
            - application/json
            - application/xml
        produces:
            - application/json
            - application/xml
        """

        span_type = ['last 6 Month', 'last 12 Month', 'last 24 Month', 'last 27 Month', 'last 30 Month']
        criteria_type = ['leadcriteria1', 'leadcriteria2', 'leadcriteria3', 'others']

        if ('span' in request.query_params):
            span = str(request.query_params['span'])
        else:
            return Response({'status': 'ERROR',
                             'error': 'un_specified span_type'})

        if ('post' in request.query_params):
            zip_code = str(request.query_params['post'])
        else:
            return Response({'status': 'ERROR',
                             'error': 'un_specified post'})

        if ('criteria' in request.query_params):
            criteria = str(request.query_params['criteria'])
        else:
            return Response({'status': 'ERROR',
                             'error': 'un_specified criteria'})

        if request.query_params['span'] not in span_type:
            return Response({'status': 'ERROR', 'error': 'INVALID_SPAN'})
        if request.query_params['criteria'] not in criteria_type:
            return Response({'status': 'ERROR', 'error': 'INVALID_CRITERIA'})

        data = list(db_client.LeadsData.lead.find({"PostalCode": zip_code}, {"data.%s.%s" % (criteria, span): 1, '_id': 0}))
        if len(data) == 0:
            return Response({'status': 'ERROR', 'error': 'Not Enough Properties Matching with your search'})
        if data[0]['data'] == {}:
            return Response({'status': 'ERROR', 'error': 'Not Enough Properties Matching your search Criteria'})
        if data[0]['data'][criteria] == {}:
            return Response({'status': 'ERROR', 'error': 'Not Enough Properties Matching with your search span '})
        DATA = data[0]['data'][criteria][span]
        Property_info = {'offmarket properties': DATA}
        return Response(Property_info)
    @method_decorator(cache_page(60*60))
    def dispatch(self,*args,**kwargs):
        return super(LeadData,self).dispatch(*args,**kwargs)