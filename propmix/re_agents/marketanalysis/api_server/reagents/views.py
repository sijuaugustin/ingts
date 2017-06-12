'''
Created on Dec 29, 2016

@author: joseph
'''

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from pymongo import MongoClient
from .dbauth import DATABASE_ACCESS

prop_type = ['Single Family Residence', 'Condominium', 'Townhouse', 'All']
SpanType = ['1M', '3M', '6M', '12M', '18M']
ListOffices = ['TheMLSonline.com']


@permission_classes((permissions.AllowAny,))
class AgentMonetoryViewSet(viewsets.ViewSet):

    def list(self, request):
        """
        AgentMonetory

               API will return the Agent name, Percentage value of average sold to list price.

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
                     "enum": ['Single Family Residence', 'Condominium', 'Townhouse', 'All']
                     defaultValue: All
                   - name: Span
                     description: It is the time span in which the Total Transaction done in a particular time which calculates as '1M', '3M', '6M', '12M', '18M'.
                     required: true
                     paramType: query
                     "enum": ['1M', '3M', '6M', '12M', '18M']
                     defaultValue: 18M


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
        except:
                return Response({'status': 'ERROR',
                                 'error': 'NO_States_SPECIFIED'})
        req_state = request.query_params['State']
        req_listoffice = request.query_params['ListOfficeName']
        req_prop = request.query_params['PropertyType']
        req_span = request.query_params['Span']
        state = str(req_state)
        listoffice = str(req_listoffice)
        span = str(req_span)
        prop = str(req_prop)
        db_client = MongoClient(host='mongo-master.propmix.io', port=33017)
        db_client.agents.authenticate(**DATABASE_ACCESS)
        data = list(db_client.listingoffices.agentperformance.find({'_id': {"State": state,"ListOfficeName": listoffice}}))
        result = []
        performance_index = data[0]['performance_index'].items()
        performance_index.sort(key=lambda x: x[1][prop][span]['Number_of_Transactions_Active'] + x[1][prop][span]['Number_of_Transactions_Sold'], reverse=True)
        performance_index = performance_index[:10]
        for key, value in performance_index:
            if value[prop][span]['Number_of_Transactions_Sold'] > 0:
                dict_ = {}
                dict_['Agent_Name'] = key
                dict_['Number_of_Transactions_Sold'] = value[prop][span]['Number_of_Transactions_Sold']
                dict_['Total_ClosePrice_Sold'] = value[prop][span]['Total_ClosePrice_Sold']
                dict_['Total_ListPrice_Sold'] = value[prop][span]['Total_ListPrice_Sold']
                dict_['Number_of_Transactions_Active'] = value[prop][span]['Number_of_Transactions_Active']
                dict_['Total_ListPrice_Active'] = value[prop][span]['Total_ListPrice_Active']
                result.append(dict_)

        return Response(result)


@permission_classes((permissions.AllowAny,))
class AgentSharePercentViewSet(viewsets.ViewSet):
    def list(self, request):
        """
        AgentSharePercent

               API will return the Agent name, Percentage of Total Close Price and Total List Price of agent with repect to the Total Close Price and Total List Price of all the agent.

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
                     "enum": ['Single Family Residence', 'Condominium', 'Townhouse', 'All']
                     defaultValue: All
                   - name: Span
                     description: It is the time span in which the Total Transaction done in a particular time which calculates as '1M', '3M', '6M', '12M', '18M'.
                     required: true
                     paramType: query
                     "enum": ['1M', '3M', '6M', '12M', '18M']
                     defaultValue: 18M

               responseMessages:
                   - code: 401
                     message: Not authenticated
                   - code : 404
                     message: Not Found
                   - code : ERROR
                     message : NO_Property_SPECIFIED
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
        except:
                return Response({'status': 'ERROR',
                                 'error': 'NO_States_SPECIFIED'})
        req_state = request.query_params['State']
        req_listoffice = request.query_params['ListOfficeName']
        req_prop = request.query_params['PropertyType']
        req_span = request.query_params['Span']
        state = str(req_state)
        listoffice = str(req_listoffice)
        span = str(req_span)
        prop = str(req_prop)
        db_client = MongoClient(host='mongo-master.propmix.io', port=33017)
        db_client.agents.authenticate(**DATABASE_ACCESS)
        data = list(db_client.listingoffices.agentperformance.find({'_id': {"State": state,"ListOfficeName": listoffice}}))
        performance_index = data[0]['performance_index'].items()
        performance_index.sort(key=lambda x: x[1][prop][span]['Number_of_Transactions_Active'] + x[1][prop][span]['Number_of_Transactions_Sold'], reverse=True)
        performance_index = performance_index[:10]
        Close_Price = []
        List_Price = []
        List_Price_ = []
        for key_, value_ in performance_index:
                Close_Price.append(value_[prop][span]['Total_ClosePrice_Sold'])
                List_Price.append(value_[prop][span]['Total_ListPrice_Sold'])
                List_Price_.append(value_[prop][span]['Total_ListPrice_Sold'])
                List_Price_.append(value_[prop][span]['Total_ListPrice_Active'])
        Total_CP = sum(Close_Price)
        Total_LP = sum(List_Price)
        Total_LP_ = sum(List_Price_)
        result = []
        for key, value in performance_index:
            if value[prop][span]['Number_of_Transactions_Sold'] > 0:
                dict_ = {}
                dict_['Number_of_Transactions_Sold'] = value[prop][span]['Number_of_Transactions_Sold']
                dict_['Number_of_Transactions_Active'] = value[prop][span]['Number_of_Transactions_Active']
                dict_['ClosePrice_Percent_Sold'] = (float(value[prop][span]['Total_ClosePrice_Sold']) / float(Total_CP)) * 100
                dict_['ListPrice_Percent_Sold'] = (float(value[prop][span]['Total_ListPrice_Sold']) / float(Total_LP)) * 100
                dict_['ListPrice_Percent_Active'] = ((float(value[prop][span]['Total_ListPrice_Active']) + (float(value[prop][span]['Total_ListPrice_Sold']))) / float(Total_LP_)) * 100
                name = key
                name = name.split()
                if len(name) >= 3:
                    firstName = name[0]
                    secondName = name[1]
                    lastName = name[len(name) - 1]
                    firstInitial = firstName[0] + "."
                    secondInitial = secondName[0] + "."
                    new_name = firstInitial + secondInitial + lastName
                elif len(name) == 2:
                    firstName = name[0]
                    lastName = name[1]
                    firstInitial = firstName[0] + "."
                    new_name = firstInitial + lastName
                elif len(name) == 1:
                    new_name = name[0]
                dict_['Agent_Name'] = new_name
                result.append(dict_)
        return Response(result)


@permission_classes((permissions.AllowAny,))
class AgentSoldToListViewSet(viewsets.ViewSet):
    def list(self, request):
        """
        AgentSoldToList

               API will return the Agent name, Percentage value of average sold to list price.

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
                     "enum": ['Single Family Residence', 'Condominium', 'Townhouse', 'All']
                     defaultValue: All
                   - name: Span
                     description: It is the time span in which the Total Transaction done in a particular time which calculates as '1M', '3M', '6M', '12M', '18M'.
                     required: true
                     paramType: query
                     "enum": ['1M', '3M', '6M', '12M', '18M']
                     defaultValue: 18M

               responseMessages:
                   - code: 401
                     message: Not authenticated
                   - code : 404
                     message: Not Found
                   - code : ERROR
                     message : No span Specified or Invalid span

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
        except:
                return Response({'status': 'ERROR',
                                 'error': 'NO_States_SPECIFIED'})
        req_state = request.query_params['State']
        req_listoffice = request.query_params['ListOfficeName']
        req_prop = request.query_params['PropertyType']
        req_span = request.query_params['Span']
        state = str(req_state)
        listoffice = str(req_listoffice)
        span = str(req_span)
        prop = str(req_prop)
        db_client = MongoClient(host='mongo-master.propmix.io', port=33017)
        db_client.agents.authenticate(**DATABASE_ACCESS)
        data = list(db_client.listingoffices.agentperformance.find({'_id': {"State": state,"ListOfficeName": listoffice}}))
        result = []
        performance_index = data[0]['performance_index'].items()
        performance_index.sort(key=lambda x: x[1][prop][span]['Number_of_Transactions_Active'] + x[1][prop][span]['Number_of_Transactions_Sold'], reverse=True)
        performance_index = performance_index[:10]
        for key, value in performance_index:
            if value[prop][span]['Number_of_Transactions_Sold'] > 0:
                dict_ = {}
                dict_['Number_of_Transactions_Sold'] = value[prop][span]['Number_of_Transactions_Sold']
                dict_['Sold_to_List_deviation_percent'] = value[prop][span]['Avg_Sold_to_List_percent_Sold'] - 100
                dict_['Agent_Name'] = key
                result.append(dict_)
        return Response(result)
