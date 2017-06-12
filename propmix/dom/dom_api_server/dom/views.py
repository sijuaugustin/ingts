'''
Created on Feb 17, 2017

@author: vivek.mv
'''
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from pymongo import MongoClient
from .dbauth import DATABASE_ACCESS




SpanType = ['last 3 Month', 'last 6 Month','last 12 Month','last 18 Month','last 15 Month','last 24 Month']
days = ['100','200','300','400','500']



@permission_classes((permissions.AllowAny,))
class DOM(viewsets.ViewSet):
        def list(self, request):
            """
            Price Deviation over DOM

            API will return Price Deviation over DOM

            ---

            type:
              schema : {period: int, yr: int, index_nsa: float }
            parameters_strategy: merge
            omit_parameters:
                - path
            parameters:
                - name: zip
                  description: postal code
                  required: true
                  type: string
                  paramType: query
                  defaultValue: 33134
                - name: span
                  description: It is the time span which the property that sold
                  required: true
                  paramType: query
                  defaultValue: last 3 Month


            consumes:
                - application/json
            produces:
                - application/json
        """            

            
            if ('span' in request.query_params):
                req_span = str(request.query_params['span'])
            else:
                return Response({'status': 'ERROR','error': 'un_specified span_type'})
            if ('zip' in request.query_params):
                zipcode = str(request.query_params['zip'])
            else:
                return Response({'status': 'ERROR','error': 'un_specified zip_code'})
            if request.query_params['span'] not in SpanType:
                return Response({'status': 'ERROR', 'error': 'INVALID_SPAN'})
            
            

            db_client =  MongoClient(host='mongo-master.propmix.io', port=33017)
            db_client.pricing.authenticate(**DATABASE_ACCESS)
            data = list(db_client.pricing.pricedifferencefinal.find({"PostalCode": zipcode},{"PriceDeviationIndex.%s"%(req_span):1 }))
            if ('days' in request.query_params):
                limit = int(request.query_params['days'])
                mnth = data[0]['PriceDeviationIndex'][req_span]
                condition_data=[]
                for i in mnth:
                    if i['DOM'] <= limit:
                        condition_data.append(i)
                result=condition_data
                return Response(result)
            else:
                return Response(data)
                        
                    
                         
                    
        
           
              
                
            
                     
                     
                     
                     
                     
                    
                
                
    
                
        
        
                    
                    
                    
    
    
    

       
       

        
        
            
                
          
        
            
        
        
        
        
        
        
        
        
        

             

        
        

       
        
        
        
         
        
     
        
        
        
        
        
        
        
        
        
