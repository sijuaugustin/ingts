from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from pymongo import MongoClient
SpanType = ['1M','3M','6M','1Y','5Y']
AtrType = ['ClosePrice','price_sqft','NumberOfTransactions','ListPrice']
@permission_classes((permissions.AllowAny,))
class zip_api(viewsets.ViewSet):
    
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
      radius=request.query_params['radius']  
      
      try:
         if not request.query_params['radius'].isdigit():
            return Response({'status':'ERROR','error':'INVALID_radius'})
      except:
            return Response({'status':'ERROR','error':'NO_radius_SPECIFIED'})
      
      longitude = ""

      if ("longitude" in request.query_params):
           longitude = request.query_params['longitude']
      else:
           return Response({'status': 'ERROR',
                            'error': 'Please Enter a valid longitude'})

      latitude = ""

      if ("latitude" in request.query_params):
           latitude = request.query_params['latitude']
      else:
           return Response({'status': 'ERROR',
                            'error': 'Please Enter a valid latitude'})
      db_client = MongoClient(host='mongo-master.propmix.io', port=33017) 
     
      lat=float(latitude)
      long=float(longitude)
      rad=int(radius)
      span=str(req_span)
      attribute=str(req_attr)
      data_1=list(db_client.iestimate.HeatMapNew.find( { "loc" :{ "$geoWithin" :{ "$centerSphere" :[ [ long,lat ] , rad / 3963.2 ]} } } ))
      
      data_2=[]
      for list_value in data_1:
        data_2.append(list_value["PostalCode"])
      uniq_zip=list(set(data_2))      
      zipDataDicts1={}
      zipDataDicts1["span"]=req_span
      j=0
      feture_data_List=[]
      for i in uniq_zip:
          j=j+1
          zipDataDict1={}
          data_3 =list(db_client.iestimate.HeatMapNew.find({"PostalCode":i}))
          cords=[]
          span_attr_value=[]
          for value1 in data_3:
              cords.append(value1['loc']['coordinates'])
              
          span_attr_value.append(value1[span][attribute])
          zipDataDict1=data_3[0]   
          zipDataDict1.pop('loc', None)  
          zipDataDict1.pop('_id', None)
          zipDataDict1.pop('1M', None)
          zipDataDict1.pop('3M', None)
          zipDataDict1.pop('6M', None)
          zipDataDict1.pop('1Y', None)
          zipDataDict1.pop('5Y', None)
          prop={'name':i,req_attr:span_attr_value[0]}
          polygon={'type':'Polygon','coordinates':cords}
          #zipDataDict1['coordinates']=cords
          #zipDataDict1[attribute]=span_attr_value
          feture_data_List.append({'type':'Feature','id':j,'properties':prop,'geometry':polygon})
          zipDataDicts1[i]=zipDataDict1
          
     
      if req_attr=="price_sqft":
                    margin_=[10,100,150,200,250,300,350,1000]
         #           margin.append(margin_)
      elif req_attr=="NumberOfTransactions":
                    margin_=[1,10,50,100,250,400,600,1000]
          #          margin.append(margin_)
      else:
                    margin_=[10000,80000,120000,200000,350000,450000,600000,10000000]
      calc = {'type':"FeatureCollection",'features':feture_data_List}
      county_={"PostalData": calc,"PostalDataMargin":margin_}
      return Response(county_)