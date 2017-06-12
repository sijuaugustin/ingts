'''
Created on Jul 26, 2016

@author: cloudera
'''
'''
Created on Jul 22, 2016

@author: cloudera
'''
import urllib2
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from pymongo import MongoClient
import json

@permission_classes((permissions.AllowAny,))
class heatap(viewsets.ViewSet):
    
    def list(self, request):


            db_client = MongoClient(host='mongo-master.propmix.io', port=33017)
            data = list(db_client.iestimate.HeatMapMediansZipWise.find({}))
            heat_data=[]

            for i in range(len(data))  :
                heat={}
                pc=data[i]['_id']['PostalCode']
                #calc = { data[i]['_id']['PostalCode']:{ "closeprice": data[i]['5Y']['ClosePrice'], "listprice": data[i]['5Y']['ListPrice'],"price_sqft": data[i]['5Y']['price_sqft'],"NumberOfTransactions": data[i]['5Y']['NumberOfTransactions']}}
                Heat5y={ "closeprice": data[i]['5Y']['ClosePrice'], "listprice": data[i]['5Y']['ListPrice'],"price_sqft": data[i]['5Y']['price_sqft'],"NumberOfTransactions": data[i]['5Y']['NumberOfTransactions']};
                Heat1y={ "closeprice": data[i]['1Y']['ClosePrice'], "listprice": data[i]['1Y']['ListPrice'],"price_sqft": data[i]['1Y']['price_sqft'],"NumberOfTransactions": data[i]['1Y']['NumberOfTransactions']};
                Heat6M={ "closeprice": data[i]['6M']['ClosePrice'], "listprice": data[i]['6M']['ListPrice'],"price_sqft": data[i]['6M']['price_sqft'],"NumberOfTransactions": data[i]['6M']['NumberOfTransactions']};
                Heat3M={ "closeprice": data[i]['3M']['ClosePrice'], "listprice": data[i]['3M']['ListPrice'],"price_sqft": data[i]['3M']['price_sqft'],"NumberOfTransactions": data[i]['3M']['NumberOfTransactions']};
                Heat1M={ "closeprice": data[i]['1M']['ClosePrice'], "listprice": data[i]['1M']['ListPrice'],"price_sqft": data[i]['1M']['price_sqft'],"NumberOfTransactions": data[i]['1M']['NumberOfTransactions']};
                
                calc = {'postalcodes':pc,'data':{'5Y':Heat5y,'1Y':Heat1y,'6M':Heat6M,'3M':Heat3M,'1M':Heat1M }}
                heat.update(calc)  
                heat_data.append(heat)
           
            return Response(heat_data) 
@permission_classes((permissions.AllowAny,))
class HeatapS(viewsets.ViewSet):
    
    def list(self, request):


            db_client = MongoClient(host='169.45.215.122', port=33017)
            data = list(db_client.iestimate.HeatMapMediansStateWise.find({}))
            heat_data=[]
            feture_data_List=[]
            for i in range(len(data))  :
                heat={}
                state=data[i]['_id']['State'][0]
                #calc = { data[i]['_id']['PostalCode']:{ "closeprice": data[i]['5Y']['ClosePrice'], "listprice": data[i]['5Y']['ListPrice'],"price_sqft": data[i]['5Y']['price_sqft'],"NumberOfTransactions": data[i]['5Y']['NumberOfTransactions']}}
                #Heat5y={ "closeprice": data[i]['5Y']['ClosePrice'], "listprice": data[i]['5Y']['ListPrice'],"price_sqft": data[i]['5Y']['price_sqft'],"NumberOfTransactions": data[i]['5Y']['NumberOfTransactions']};
                Heat5y=data[i]['5Y']['ClosePrice'];
                poly={}
                #Heat6M={ "closeprice": data[i]['6M']['ClosePrice'], "listprice": data[i]['6M']['ListPrice'],"price_sqft": data[i]['6M']['price_sqft'],"NumberOfTransactions": data[i]['6M']['NumberOfTransactions']};
                #Heat3M={ "closeprice": data[i]['3M']['ClosePrice'], "listprice": data[i]['3M']['ListPrice'],"price_sqft": data[i]['3M']['price_sqft'],"NumberOfTransactions": data[i]['3M']['NumberOfTransactions']};
                #Heat1M={ "closeprice": data[i]['1M']['ClosePrice'], "listprice": data[i]['1M']['ListPrice'],"price_sqft": data[i]['1M']['price_sqft'],"NumberOfTransactions": data[i]['1M']['NumberOfTransactions']};
                prop={'State':state,'closeprice':Heat5y}
                feture_data_List.append({'type':'5_year_data','id':i,'properties':prop })
                
            calc = {'type':"FeatureCollection",'features':feture_data_List}
            #print heat_data
            return Response(calc)
            #print heat_data
            #heat_data={'heat_data':heat}
            #print heat_data
           



