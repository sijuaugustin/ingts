'''
Created on Jan 23, 2017

@author: vishnu.sk
'''

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from pymongo import MongoClient
from .dbauth import DATABASE_ACCESS

prop_type = ['Single Family Residence', 'Condominium', 'Townhouse', 'All']
SpanType = ['Year over Year', 'Quarter over Quarter', 'Same Quarter Previous and Current Year', 'Same Month Previous and Current Year']
PriceType = ['ClosePrice', 'ListPrice']
ListOffices = ['TheMLSonline.com']


@permission_classes((permissions.AllowAny,))
class GrowthViewSet(viewsets.ViewSet):

    def list(self, request):
        """
        Market Growth

               API will return the Total ClosePrice and Total ListPrice of various time spans.

               ---

               type:
                 schema : { CountyData: { Margin: [], type: FeatureCollection, features: [] }, StateData: { Margin: [], type: FeatureCollection, features: [] }}
               parameters_strategy: merge
               omit_parameters:
                   - path
               parameters:
                   - name: State
                     description: It is the location/State in which the Property is listed/sold.
                     required: true
                     type: string
                     paramType: query
                     "enum": ['All', 'MN', 'WI', 'WA']
                     defaultValue: All
                   - name: ListOfficeName
                     description:  It is the Brokerage office.
                     required: true
                     type: string
                     paramType: query
                     defaultValue: TheMLSonline.com
                   - name: PropertyType
                     description: The kind of Property types that are sold.
                     required: true
                     type: string
                     paramType: query
                     "enum": ["Single Family Residence", "Condominium", "Townhouse", "All" ]
                     defaultValue: All
                   - name: Price
                     description:  It is the Sold price or List price.
                     required: true
                     type: string
                     paramType: query
                     "enum": ["ClosePrice", "ListPrice"]
                     defaultValue: ClosePrice
                   - name: Span
                     description: It is the time span in which the transactions are done.
                     required: true
                     paramType: query
                     "enum": ['Year over Year', 'Quarter over Quarter', 'Same Quarter Previous and Current Year', 'Same Month Previous and Current Year']
                     defaultValue: Year over Year


               responseMessages:
                   - code: 401
                     message: Not authenticated
                   - code : 404
                     message: Not Found
                   - code : ERROR
                     message : Unknown Error

               consumes:
                   - application/json
                   - application/xml
               produces:
                   - application/json
                   - application/xml
        """
        try:
            if 'State' not in request.query_params:
                return Response({'status': 'ERROR', 'error':
                                 'INVALID_State'})
            elif 'ListOfficeName' not in request.query_params and request.query_params['ListOfficeName'] not in ListOffices:
                return Response({'status': 'ERROR', 'error':
                                 'INVALID_ListOfficeName'})
            elif 'PropertyType' not in request.query_params and request.query_params['PropertyType'] not in prop_type:
                return Response({'status': 'ERROR', 'error':
                                 'INVALID_Property_type'})
            elif 'Span' not in request.query_params and request.query_params['Span'] not in SpanType:
                return Response({'status': 'ERROR', 'error': 'INVALID_SPAN'})
            elif 'Price' not in request.query_params and request.query_params['Price'] not in PriceType:
                return Response({'status': 'ERROR', 'error': 'INVALID_Price'})
        except:
                return Response({'status': 'ERROR',
                                 'error': 'UnknownError'})
        req_state = request.query_params['State']
        req_listoffice = request.query_params['ListOfficeName']
        req_span = request.query_params['Span']
        req_prop = request.query_params['PropertyType']
        req_price = request.query_params['Price']
        state = str(req_state)
        prop = str(req_prop)
        span = str(req_span)
        listoffice = str(req_listoffice)
        price = str(req_price)
        db_client = MongoClient(host='mongo-master.propmix.io', port=33017)
        db_client.marketgrowth.authenticate(**DATABASE_ACCESS)
        data = list(db_client.marketgrowth.growthstats.find({'_id': {"State": state, "ListOfficeName": listoffice}}))
        performance_index = data[0]['performance_index'].items()
        result = []
        for key, value in performance_index:
            if span == 'Year over Year':
                if value[prop][price]['Total_Price_current_year'] != 0 and value[prop][price]['Total_Price_previous_year'] != 0:
                    dict_ = {}
                    dict_['Agent_Name'] = key
                    dict_['Current Year'] = value[prop][price]['Total_Price_current_year']
                    dict_['Previous Year'] = value[prop][price]['Total_Price_previous_year']
                    result.append(dict_)
            elif span == 'Quarter over Quarter':
                if value[prop][price]['Total_Price_current_year_4th_quarter'] != 0:
                    dict_ = {}
                    dict_['Agent_Name'] = key
                    dict_['Current Quarter'] = value[prop][price]['Total_Price_current_year_current_quarter']
                    dict_['2nd Quarter'] = value[prop][price]['Total_Price_current_year_2nd_quarter']
                    dict_['3rd Quarter'] = value[prop][price]['Total_Price_current_year_3rd_quarter']
                    dict_['4th Quarter'] = value[prop][price]['Total_Price_current_year_4th_quarter']
                    result.append(dict_)
            elif span == 'Same Quarter Previous and Current Year':
                if value[prop][price]['Total_Price_previous_year_current_quarter'] != 0:
                    dict_ = {}
                    dict_['Agent_Name'] = key
                    dict_['Current Year Same Quarter'] = value[prop][price]['Total_Price_current_year_current_quarter']
                    dict_['Previous Year Same Quarter'] = value[prop][price]['Total_Price_previous_year_current_quarter']
                    result.append(dict_)
            elif span == 'Same Month Previous and Current Year':
                if value[prop][price]['Total_Price_previous_year_last_month'] != 0:
                    dict_ = {}
                    dict_['Agent_Name'] = key
                    dict_['Current Year Same Month'] = value[prop][price]['Total_Price_current_year_last_month']
                    dict_['Previous Year Same Month'] = value[prop][price]['Total_Price_previous_year_last_month']
                    result.append(dict_)
        return Response(result[:10])
