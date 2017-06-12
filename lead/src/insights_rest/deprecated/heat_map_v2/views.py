from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from pymongo import MongoClient
import math
#declare range
SpanType = ['1M','3M','6M','1Y','5Y']
AtrType = ['ClosePrice','price_sqft','NumberOfTransactions','ListPrice']


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
        level_map = {"County":{"collection":"HeatMapMediansCountyWise_copy"}, "State":{"collection":"HeatMapMediansStateWise_new"}}
        #feture_data_List=[]
        #margin=[]
       
 
        
        class DBFilter():
            
            @staticmethod
            def filter(level,span,attribute):
                
                feture_data_List=[]
               
                
                data_= list(db_client["iestimate"][level_map[level]["collection"]].find({}, {"%s.%s" % (span, attribute):True,"coordinates":True}))
                
                for i in range(len(data_))  :
                        try:
                            
                            
                            
                            CountyOrStateOrZip=data_[i]['_id'][level][0] if type(data_[i]['_id'][level]) is list else data_[i]['_id'][level]
                           # print data_[i]['_id']
                            if math.isnan(float(data_[i][span][attribute])):
                                heat_attr = -1
                            else:
                                heat_attr = data_[i][span][attribute]

                                
                            prop={'name':CountyOrStateOrZip,attribute:heat_attr}
                            cords=data_[i]['coordinates']
                            polygon={'type':'Polygon','coordinates':cords}
                            
                            
                            feture_data_List.append({'type':'Feature','id':i,'properties':prop,'geometry':polygon})
                            #print i, CountyOrStateOrZip, feture_data_List
                        except:
                            print 'nodata for'
                calc = {'type':"FeatureCollection",'features':feture_data_List}

                
#                 def chunkIt(seq, num):
#                     avg = len(seq) / float(num)
#                     out = []
#                     last = 0.0
# 
#                     while last < seq:
#                         out.append(seq[int(last):int(last + avg)])
#                         last += avg
# 
#                     return out
              
#                 countymargin=chunkIt(range(int(maxi)),8)
#                 statemargin=chunkIt(range(int(maxi)) ,8)
                return calc
            
            

        State_data = DBFilter.filter("State",req_span,req_attr) 
        County_data = DBFilter.filter("County",req_span,req_attr)
        if req_attr=="price_sqft":
                    margin_=[10,100,150,200,250,300,350,1000]
         #           margin.append(margin_)
        elif req_attr=="NumberOfTransactions":
                    margin_=[1,10,50,100,250,400,600,1000]
          #          margin.append(margin_)
        else:
                    margin_=[10000,80000,120000,200000,350000,450000,600000,10000000]
           #         margin.append(margin_)
        #Zip_data = DBFilter.filter("PostalCode",req_span,req_attr)
        
        
        all_data = {"CountyData": County_data,"CountyDataMargin":margin_,"StateData": State_data,"StateDataMargin":margin_ }
        return Response(all_data)

    
    
         
