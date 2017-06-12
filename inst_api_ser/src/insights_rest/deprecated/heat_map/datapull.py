'''
Created on Jul 20, 2016

@author: cloudera
'''
'''
Created on Jul 18, 2016

@author: cloudera
'''

from pymongo import MongoClient
import json
db_client = MongoClient(host='169.45.215.122', port=33017)
data = list(db_client.iestimate.HeatMapMediansZipWise.find({}))
# for row in data :
#     print data
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
#heat_data={'heat_data':heat}
print heat_data
     
    
#     heat[i]["postalcode"]= data[i]['_id']['PostalCode']
#     heat[i]["closeprice"]= data[i]['5Y']['ClosePrice']
# for row in heat:
#     print row
#     print item['_id']['PostalCode'],item['5Y']['ClosePrice']
    
       # print ("postalcode" :item['_id']['PostalCode'])
    
#data=data.to_json(path_or_buf = None, orient = 'records', date_format = 'epoch', double_precision = 10, force_ascii = True, date_unit = 'ms', default_handler = None)
#print data 
#myJSON = x.to_json(path_or_buf = None, orient = 'records', date_format = 'epoch', double_precision = 10, force_ascii = True, date_unit = 'ms', default_handler = None)
#postal_codes = [{'PostalCode':item['_id']['PostalCode']} for item in AllZips if item['_id']['PostalCode'] and item['_id']['PostalCode'].isdigit() and int(item['_id']['PostalCode']) != 0]
                



