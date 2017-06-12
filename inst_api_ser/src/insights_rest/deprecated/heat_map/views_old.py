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


            db_client = MongoClient(host='169.45.215.122', port=33017)
            data = list(db_client.iestimate.HeatMapMediansZipWise.find({}))
# for row in data :
#     print data
            heat={}
            for i in range(len(data))  :
    #calc = {{"Postalcode": data[i]['_id']['PostalCode']}:{ "closeprice": data[i]['5Y']['ClosePrice'], "listprice": data[i]['5Y']['ListPrice'],"price_sqft": data[i]['5Y']['price_sqft'],"NumberOfTransactions": data[i]['5Y']['NumberOfTransactions']}}
                calc = { data[i]['_id']['PostalCode']:{ "closeprice_5Y": data[i]['5Y']['ClosePrice'], "listprice_5Y": data[i]['5Y']['ListPrice'],"price_sqft_5Y": data[i]['5Y']['price_sqft'],"NumberOfTransactions_5Y": data[i]['5Y']['NumberOfTransactions'],"closeprice_1Y": data[i]['1Y']['ClosePrice'], "listprice_1Y": data[i]['1Y']['ListPrice'],"price_sqft_1Y": data[i]['1Y']['price_sqft'],"NumberOfTransactions_1Y": data[i]['1Y']['NumberOfTransactions'],"closeprice_6M": data[i]['6M']['ClosePrice'], "listprice_6M": data[i]['6M']['ListPrice'],"price_sqft_6M": data[i]['6M']['price_sqft'],"NumberOfTransactions_6M": data[i]['6M']['NumberOfTransactions'],"closeprice_3M": data[i]['3M']['ClosePrice'], "listprice_3M": data[i]['3M']['ListPrice'],"price_sqft_3M": data[i]['3M']['price_sqft'],"NumberOfTransactions_3M": data[i]['3M']['NumberOfTransactions'],"closeprice_1M": data[i]['1M']['ClosePrice'], "listprice_1M": data[i]['1M']['ListPrice'],"price_sqft_1M": data[i]['1M']['price_sqft'],"NumberOfTransactions_1M": data[i]['1M']['NumberOfTransactions']}}
 
                heat.update(calc)
#             print heat
#             data = db_client.iestimate.Final_Zip.find()
#             data=data.to_json(path_or_buf = None, orient = 'records', date_format = 'epoch', double_precision = 10, force_ascii = True, date_unit = 'ms', default_handler = None)
#             
#             print data
            return Response(heat)   


