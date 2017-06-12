'''
Created on Jul 26, 2016

@author: cloudera
'''
import urllib2
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from pymongo import MongoClient
import json

SpanType=['1M','3M','6M','1Y','5Y']
AtrType=['ClosePrice','price_sqft','NumberOfTransactions','ListPrice']


@permission_classes((permissions.AllowAny,))
class heatap(viewsets.ViewSet):
    def list(self, request):
        
        
        

            try:
                if request.query_params['span'] not in SpanType:
                    return Response({'status':'ERROR','error':'INVALID_SPAN'})
                elif request.query_params['attribute'] not in AtrType:
                    return Response({'status':'ERROR','error':'INVALID_ATTRIBUTE_NAME'})
 
                     
            except:
                return Response({'status':'ERROR','error':'NO_SPAN_SPECIFIED'}) 
            
            req_span=request.query_params['span']
            req_attr= request.query_params['attribute']  
            db_client = MongoClient(host='mongo-master.propmix.io', port=33017)
#             data = list(db_client.iestimate.HeatMapMediansZipWise.find({}))
#             heat_data=[]
            #level_map = {"State":{"collection":"HeatMapMediansStateWise"}}
            level_map = {"State":{"collection":"HeatMapMediansStateWise_new"}}
            feture_data_List=[]
            #cords=[]

            class DBFilter():
                @staticmethod
                def filter(level,span,attribute):
                    data_= list(db_client["iestimate"][level_map[level]["collection"]].find({}, {"%s.%s" % (span, attribute):True,"coordinates":True}))
                    #data_= list(db_client["iestimate"][level_map[level]["collection"]].find({}, {"%s.%s" % (span, attribute):True}))
                    for i in range(len(data_))  :
                                heat={}
                                state=data_[i]['_id']['State']
                                #calc = { data[i]['_id']['PostalCode']:{ "closeprice": data[i]['5Y']['ClosePrice'], "listprice": data[i]['5Y']['ListPrice'],"price_sqft": data[i]['5Y']['price_sqft'],"NumberOfTransactions": data[i]['5Y']['NumberOfTransactions']}}
                                #Heat5y={ "closeprice": data[i]['5Y']['ClosePrice'], "listprice": data[i]['5Y']['ListPrice'],"price_sqft": data[i]['5Y']['price_sqft'],"NumberOfTransactions": data[i]['5Y']['NumberOfTransactions']};
                                Heat5y=data_[i][span][attribute];
                                poly={}
                                #Heat6M={ "closeprice": data[i]['6M']['ClosePrice'], "listprice": data[i]['6M']['ListPrice'],"price_sqft": data[i]['6M']['price_sqft'],"NumberOfTransactions": data[i]['6M']['NumberOfTransactions']};
                                #Heat3M={ "closeprice": data[i]['3M']['ClosePrice'], "listprice": data[i]['3M']['ListPrice'],"price_sqft": data[i]['3M']['price_sqft'],"NumberOfTransactions": data[i]['3M']['NumberOfTransactions']};
                                #Heat1M={ "closeprice": data[i]['1M']['ClosePrice'], "listprice": data[i]['1M']['ListPrice'],"price_sqft": data[i]['1M']['price_sqft'],"NumberOfTransactions": data[i]['1M']['NumberOfTransactions']};
                                prop={'State':state,attribute:Heat5y}
                                #coordinates=list(data_[i]['coordinates'])
                                cords=data_[i]['coordinates']
                                
                               # print data[i]
                                polygon={'type':'Polygon','coordinates':cords}
                                feture_data_List.append({'type':span,'id':i,'properties':prop,'geometry':polygon})
                                #feture_data_List.append({'type':span,'id':i,'properties':prop})
                    
                    calc = {'type':"FeatureCollection",'features':feture_data_List}
            #print heat_data
            #return Response(calc)
                    return calc
                    
            data=DBFilter.filter("State",req_span,req_attr)
            return Response(data)

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
           



