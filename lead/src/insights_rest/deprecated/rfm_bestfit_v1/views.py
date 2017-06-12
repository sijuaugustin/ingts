'''
Created on 18-Aug-2016

@author: revathy.sivan
'''
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from pymongo import MongoClient
db_client = MongoClient(host='mongo-master.propmix.io', port=33017)
import urllib2
import json
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
@permission_classes((permissions.AllowAny,))
class BestFit(viewsets.ViewSet):
    
    def list(self, request):
        """
        BestFitAPI: (RFM):
        API will return the best agent who can handle the subject property.
        
        
        
        url:https://insights.propmix.io:8004/RFMbestfit/agent/?address=%228204%20SW%20206%20TE,%20Miami,%20%22&radius=1&SI_PropertyType=SingleFamily&LotSizeArea=7500&Beds=3&YearBuilt=1990&ParkingTotal=1&GLA=1200&Baths=2&ViewYN=0&MlsBoard=Miami%20Board%20Of%20Realtors&Distance=0&Zip=33461
    
      
        ---
        # YAML (must be separated by `---`)
        
    
        type:
          schema : { Top Agents: [{AgentInfo: []}]}
          AgentInfo:
            required: false
            type: string
        parameters_strategy: merge
        omit_parameters:
            - path
        parameters:
            - name: address
              description: To fetch the near by property  given the subject property as input.
              required: true
              type: string
              paramType: query
              defaultValue: 8204 SW 206 TE, Miami 
            - name: SI_PropertyType
              description: the property belong to which property type like single family,Multifamily,etc.
              required: true
              paramType: query
              defaultValue: SingleFamily
            - name: Zipcode  
              description: To identify property belong to particular region
              required: true
              paramType: query
              defaultValue: 33461
            - name: MlsBoard
              description: It belongs to property belong to which MlsBoard
              required: true
              paramType: query
              defaultValue: Miami Board Of Realtors
            - name: radius  
              description: To get property in this radius
              required: true
              paramType: query
              defaultValue: 1
            - name: GLA  
              description: To get property similar to given GLA
              required: true
              paramType: query
              defaultValue: 1200
            - name: Beds
              description: To get property similar to given Beds
              required: true
              paramType: query
              defaultValue: 3
            - name: Baths
              description: To get property similar to given Baths
              required: true
              paramType: query
              defaultValue: 2
            - name: DaysOnMarket
              description: To get property similar to given DaysOnMarket
              required: true
              paramType: query
              defaultValue: 18
            - name: LotSizeArea
              description: To get property similar to given LotsizeArea
              required: true
              paramType: query
              defaultValue: 7500
            - name: YearBuilt
              description: To get property similar to given YearBuilt
              required: true
              paramType: query
              defaultValue: 1990
            - name: ParkingTotal
              description: To get property similar to given ParkingTotal
              required: true
              paramType: query
              defaultValue: 1
            - name: StoriesTotal
              description: To get property similar to given StoriesTotal
              required: true
              paramType: query
              defaultValue: 1
            - name: GarageYN
              description: To get property similar to given GarageYN
              required: true
              paramType: query
              defaultValue: 1
            - name: Distance
              description: To get property similar to given GarageYN
              required: true
              paramType: query
              defaultValue: 1
              

         
        responseMessages:
            - code: 401
              message: Not authenticated
            - code : 404
              message: Not Found
            - code : ERROR 
              message : No Zip Specified or Invalid Zip
    
        consumes:
            - application/json
            - application/xml
        produces:
            - application/json
            - application/xml
        """
        address=request.query_params['address'].replace('"','')
        if address:
            address=address
        else:
            return Response({'status':'ERROR','error':'Please Enter a valid address'})
            
        radius=request.query_params['radius']  
        
        try:
           if not request.query_params['radius'].isdigit():
              return Response({'status':'ERROR','error':'INVALID_radius'})
        except:
              return Response({'status':'ERROR','error':'NO_radius_SPECIFIED'})
        
        SI_PropertyType=""      
        if ("SI_PropertyType" in request.query_params):
            SI_PropertyType=request.query_params['SI_PropertyType']   
        else:
            return Response({'status':'ERROR','error':'Please Enter a valid SI_PropertyType'}) 
        
        if ("LotSizeArea" in request.query_params):
            Zip=request.query_params['LotSizeArea']   
        else:
            return Response({'status':'ERROR','error':'Please Enter a valid LotSizeArea'})   
           
        LotSizeArea=request.query_params['LotSizeArea']
        
        try:
           if not request.query_params['LotSizeArea'].isdigit():
              return Response({'status':'ERROR','error':'INVALID_LotSizeArea'})
        except:
              return Response({'status':'ERROR','error':'NO_LotSizeArea_SPECIFIED'})           
        if ("Beds" in request.query_params):
            Beds=request.query_params['Beds']   
        else:
            return Response({'status':'ERROR','error':'Please Enter a valid Beds'})    
        Beds=request.query_params['Beds']
        
        try:
           if not request.query_params['Beds'].isdigit():
              return Response({'status':'ERROR','error':'INVALID_Beds'})
        except:
              return Response({'status':'ERROR','error':'NO_Beds_SPECIFIED'})     
          
        if ("Baths" in request.query_params):
            Baths=request.query_params['Baths']   
        else:
            return Response({'status':'ERROR','error':'Please Enter a valid Baths'})     
              
        Baths=request.query_params['Baths']
        
        try:
           if not request.query_params['Baths'].isdigit():
              return Response({'status':'ERROR','error':'INVALID_Baths'})
        except:
              return Response({'status':'ERROR','error':'NO_Baths_SPECIFIED'})   
        
        if ("GLA" in request.query_params):
            
            GLA=request.query_params['GLA']   
        else:
            return Response({'status':'ERROR','error':'Please Enter a valid GLA'})    
        
        GLA=request.query_params['GLA']
        
        try:
           if not request.query_params['GLA'].isdigit():
              return Response({'status':'ERROR','error':'INVALID_GLA'})
        except:
              return Response({'status':'ERROR','error':'NO_GLA_SPECIFIED'})
          
          
        ''' if ("GarageYN" in request.query_params):
            GarageYN=request.query_params['GarageYN']   
        else:
            return Response({'status':'ERROR','error':'Please Enter a valid GarageYN'})     
            
        GarageYN=request.query_params['GarageYN'] 


        try:
           if not request.query_params['GarageYN'].isdigit():
              return Response({'status':'ERROR','error':'INVALID_GarageYN'})
        except:
              return Response({'status':'ERROR','error':'NO_GarageYN_SPECIFIED'}) '''
            
        if ("YearBuilt" in request.query_params):
            YearBuilt=request.query_params['YearBuilt']   
        else:
            return Response({'status':'ERROR','error':'Please Enter a valid YearBuilt'})            
            
            
        YearBuilt=request.query_params['YearBuilt'] 

        try:
           if not request.query_params['YearBuilt'].isdigit():
              return Response({'status':'ERROR','error':'INVALID_YearBuilt'})
        except:
              return Response({'status':'ERROR','error':'NO_YearBuilt_SPECIFIED'})    
            
        if ("ParkingTotal" in request.query_params):
            ParkingTotal=request.query_params['ParkingTotal']   
        else:
            return Response({'status':'ERROR','error':'Please Enter a valid ParkingTotal'})      
            
        ParkingTotal=request.query_params['ParkingTotal'] 

        try:
           if not request.query_params['ParkingTotal'].isdigit():
              return Response({'status':'ERROR','error':'INVALID_ParkingTotal'})
        except:
              return Response({'status':'ERROR','error':'NO_ParkingTotal_SPECIFIED'})   
              
        '''if ("GarageSpaces" in request.query_params):
            GarageSpaces=request.query_params['GarageSpaces']   
        else:
            return Response({'status':'ERROR','error':'Please Enter a valid GarageSpaces'})      
        
        GarageSpaces=request.query_params['GarageSpaces'] 

        try:
           if not request.query_params['GarageSpaces'].isdigit():
              return Response({'status':'ERROR','error':'INVALID_GarageSpaces'})
        except:
              return Response({'status':'ERROR','error':'NO_GarageSpaces_SPECIFIED'}) '''
        '''  
        if ("ViewYN" in request.query_params):
            ViewYN=request.query_params['ViewYN']   
        else:
            return Response({'status':'ERROR','error':'Please Enter a valid ViewYN'})      
        
            ViewYN=request.query_params['ViewYN'] 

        try:
           if not request.query_params['ViewYN'].isdigit():
              return Response({'status':'ERROR','error':'INVALID_ViewYN'})
        except:
              return Response({'status':'ERROR','error':'NO_ViewYN_SPECIFIED'})
        
        '''
    
         
        MlsBoard=""
        
        if ("MlsBoard" in request.query_params):
            MlsBoard=request.query_params['MlsBoard']   
        else:
            return Response({'status':'ERROR','error':'Please Enter a valid  MlsBoard'})
        
        if ("Distance" in request.query_params):
            Distance=request.query_params['Distance']   
        else:
            return Response({'status':'ERROR','error':'Please Enter a valid Distance'})   
           
        Distance=request.query_params['Distance']
        
        try:
           if not request.query_params['Distance'].isdigit():
              return Response({'status':'ERROR','error':'INVALID_Distance'})
        except:
              return Response({'status':'ERROR','error':'NO_Distance_SPECIFIED'}) 
        '''try:
           if not request.query_params['Response_Count'].isdigit():
            return Response({'status':'ERROR','error':'INVALID_Response_Count'})

        except:
            return Response({'status':'ERROR','error':'NO_Response_Count_SPECIFIED'})
        
            if ("Response_Count" in request.query_params):
                 Baths=request.query_params['Response_Count']   
            else:
                 return Response({'status':'ERROR','error':'Please Enter a valid Response_Count'}) 
        
        Response_Count=request.query_params['Response_Count'] 
        Response_Count= int(Response_Count)
        
        if   Response_Count <5:
               
             Response_Count=5
        else:
             Response_Count=Response_Count '''
        Zip=""
        
        if ("Zip" in request.query_params):
            Zip=request.query_params['Zip']   
        else:
            return Response({'status':'ERROR','error':'Please Enter a valid  Zip'})  
        
        #req = urllib2.Request("https://api.propmix.io/propmixapps/MlsListings/getListings?Address={address}&Radius={radius}&MonthsBack=12&MlsBoard={MlsBoard}&PropertyTypeList={SI_PropertyType}&LotSizeArea={LotSizeArea}&Baths={Baths}&Beds={Beds}&GLA={GLA}&GarageYN={GarageYN}&YearBuilt={YearBuilt}&ParkingTotal={ParkingTotal}&GarageSpaces={GarageSpaces}&ViewYN={ViewYN}&Distance={Distance}&Response_Count={Response_Count}".format(address=urllib2.quote(address), radius=radius,SI_PropertyType=SI_PropertyType,LotSizeArea=LotSizeArea,Baths=Baths,Beds=Beds,GLA=GLA,GarageYN=GarageYN,YearBuilt=YearBuilt,ParkingTotal=ParkingTotal,GarageSpaces=GarageSpaces,ViewYN=ViewYN,MlsBoard=MlsBoard,Distance=Distance,Response_Count=Response_Count)) 
        req = urllib2.Request("https://api.propmix.io/propmixapps/MlsListings/getListings?Address={address}&Radius={radius}&MonthsBack=12&MlsBoard={MlsBoard}&PropertyTypeList={SI_PropertyType}&LotSizeArea={LotSizeArea}&Baths={Baths}&Beds={Beds}&GLA={GLA}&YearBuilt={YearBuilt}&ParkingTotal={ParkingTotal}&Distance={Distance}".format(address=urllib2.quote(address), radius=radius,SI_PropertyType=SI_PropertyType,LotSizeArea=LotSizeArea,Baths=Baths,Beds=Beds,GLA=GLA,YearBuilt=YearBuilt,ParkingTotal=ParkingTotal,MlsBoard=MlsBoard,Distance=Distance)) 

        opener = urllib2.build_opener()
        try:
            f = opener.open(req)
        except:
            return Response({'status':'ERROR','error':'Unable to load Data Please try after some time'}) 
            
        data = json.loads(f.read())
        columns_list = ['Distance','LotSizeArea','GLA','Beds','Baths','GarageSpaces','ViewYN','ParkingTotal','YearBuilt','ListAgentFullName','Status']
        columns_list1 = ['Rets_id','SI_Status','Zip','Beds','Baths','GLA','BuildingAreaTotal','DaysOnMarket','GarageYN','StoriesTotal','FireplacesTotal','ParkingTotal','YearBuilt','ClosePrice','ListPrice',
                         'StreetNumber','StreetName','UnitNumber','City','State','Country','Address','Latitude','Longitude','Status','CloseDate','ListingDate','BathDecimal','Heating','Cooling','PublicRemarks','PoolFeatures',
                         'View','PropertyType','PropertySubType','SI_PropertyType','APN','AssociationFee','CommunityFeatures','TaxLegalDescription','TaxAnnualAmount','TaxYear','LotSizeArea',
                         'OwnerName','TaxAssessedValue','TaxExemptions','SubdivisionName','ListAgentFullName','ListAgentOfficePhone','ListAgentOfficePhoneExt','ModificationTimestamp','BasementAreaFinished',
                         'PhotoCount','Distance','OriginalListPrice','County','FrontageType','ViewYN','PoolPrivateYN','SpaFeatures','SpaYN','WaterfrontYN','WaterBodyName','WaterSource','Sewer','GarageSpaces','AttachedGarageYN',
                         'CarportSpaces','CarportYN','CoveredSpaces','FireplaceFeatures','FireplaceYN','Zoning','BasementArea','GarageSqft','Elevator','CarportDescription','GarageDescription','MasterBathDescription','WaterfrontDescription',
                         'WaterfrontFrontage','MLSListingNumber','BoardIdentifier','ConstructionType','EquipmentOrAppliances','ExteriorFeatures','FrontExposure','FloorDescription','InteriorFeatures','WaterAccess','SubjectProperty','ImageUrl','SpecialListingConditions']
        array1 = []
        for list_item in data['Listings'][:-1]:
            features = []
            for column in columns_list1:
                features.append(list_item[column])
            array1.append(features)
    
        x1 = pd.DataFrame(data=array1)
        if x1.empty: 
           print ({'status':'ERROR','error':'no  property in the current list1'}) 
        else:  
            x1=x1
        c = pd.DataFrame(x1, columns=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,
                              62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92])
        c.columns = ['Rets_id','SI_Status','Zip','Beds','Baths','GLA','BuildingAreaTotal','DaysOnMarket','GarageYN','StoriesTotal','FireplacesTotal','ParkingTotal','YearBuilt','ClosePrice','ListPrice',
                     'StreetNumber','StreetName','UnitNumber','City','State','Country','Address','Latitude','Longitude','Status','CloseDate','ListingDate','BathDecimal','Heating','Cooling','PublicRemarks','PoolFeatures',
                     'View','PropertyType','PropertySubType','SI_PropertyType','APN','AssociationFee','CommunityFeatures','TaxLegalDescription','TaxAnnualAmount','TaxYear','LotSizeArea',
                     'OwnerName','TaxAssessedValue','TaxExemptions','SubdivisionName','ListAgentFullName','ListAgentOfficePhone','ListAgentOfficePhoneExt','ModificationTimestamp','BasementAreaFinished',
                     'PhotoCount','Distance','OriginalListPrice','County','FrontageType','ViewYN','PoolPrivateYN','SpaFeatures','SpaYN','WaterfrontYN','WaterBodyName','WaterSource','Sewer','GarageSpaces','AttachedGarageYN',
                     'CarportSpaces','CarportYN','CoveredSpaces','FireplaceFeatures','FireplaceYN','Zoning','BasementArea','GarageSqft','Elevator','CarportDescription','GarageDescription','MasterBathDescription','WaterfrontDescription',
                     'WaterfrontFrontage','MLSListingNumber','BoardIdentifier','ConstructionType','EquipmentOrAppliances','ExteriorFeatures','FrontExposure','FloorDescription','InteriorFeatures','WaterAccess','SubjectProperty','ImageUrl','SpecialListingConditions']
        all=len(c)
        print all
        a ='Closed Sale'
        c=c.loc[c['Status'].isin([a])]
        closed=len(c)
        print closed
        array = []
        for list_item in data['Listings'][:-1]:
            features = []
            for column in columns_list:
                features.append(list_item[column])
            array.append(features)
    
        x= pd.DataFrame(data=array)

        x.columns=['Distance','LotSizeArea','GLA','Beds','Baths','GarageSpaces','ViewYN','ParkingTotal','YearBuilt','ListAgentFullName','Status']
        a ='Closed Sale'
        x=x.loc[x['Status'].isin([a])]
        xx=x.ix[:,0:9]
        x1=xx.replace(r'\s+',np.nan,regex=True).replace('',np.nan)
        x11=x1.as_matrix()
        x1=x11.astype(float)
        valid = np.isfinite(x1)
        mu = np.nanmean(x1, 0, keepdims=1)
        X_hat = np.where(valid, x1, mu)
        for ii in range(10):
            cls = KMeans(n_clusters=10, n_jobs=1)
            labels_hat = cls.fit_predict(X_hat)
            X_hat[~valid] = cls.cluster_centers_[labels_hat][~valid]
        x2= X_hat
        x2=pd.DataFrame(x2) 
        x2.columns = ['Distance','LotSizeArea','GLA','Beds','Baths','GarageSpaces','ViewYN','ParkingTotal','YearBuilt']
        #x1 = x1.replace("[+]", "",regex=True)
        #x1=x1.replace(['One Story'],[1])
        x=x2.append({'Distance':Distance,'LotSizeArea':LotSizeArea,'GLA':GLA,'Beds':Beds,'Baths':Baths,'ParkingTotal':ParkingTotal,'YearBuilt':YearBuilt},ignore_index='true')
        #print x
        subject=x.tail(1)
        d=len(x.index)
        mean=x.loc[d-1]
        mean = np.array(mean, dtype='int32').tolist()
        l=len(x.columns)
        x.columns=[range(l)]
        x=x.convert_objects(convert_numeric=True) 
        for index  in range(len(x.columns)):   
            x[index]=abs(mean[index]-x[index])
        mR=x.apply(lambda dh: np.sum(dh), axis=1)
        print mR
        mR=mR[0:-1]
        #print mR
        c['similarity_score']=mR
        c=c.sort(['similarity_score'], ascending=1)
        best_agent={}
        Topten_similar_property=c[:10]
        #for index,row in Topten_similar_property.iterrows():
        #    r=row[['ListAgentFullName','ListAgentOfficePhone','Zip']]
        #    best_agent.update(r)
         #   print best_agent
            
            
        #top_ten_agent_info=Topten_similar_property[['ListAgentFullName','ListAgentOfficePhone']]
        #Best_agent = top_ten_agent_info.to_dict()
        
        
        #Best_fit_agent=Topten_similar_property.iloc[0]['ListAgentFullName']
        #Best_fit_agent1=c.iloc[0][['ListAgentFullName', 'Zip']]
        #print Best_fit_agent1['Zip']
            
        #agent_details=c.iloc[0][['ListAgentFullName', 'ListAgentOfficePhone']]
        #Best_agent = agent_details.to_dict()
        
        agents= list(db_client.RFM.post.distinct("post"))
        ReturnAgents=[];
        for index,row in Topten_similar_property.iterrows():
            
            agentdata=list(db_client.RFM.post.find({"post":row['Zip']}))
            Best_fit_agent=row['ListAgentFullName']
            UserNotExists=True
            for agents in agentdata[0]['Agent_data']:
                if agents['AgentName']==Best_fit_agent:
                   agents.pop('_id', None)
                   agents['ListAgentOfficePhone']=row['ListAgentOfficePhone']
                   ReturnAgents.append(agents)
                   UserNotExists=False
                   break
            if UserNotExists:   
                no_info_data=row[['ListAgentFullName','ListAgentOfficePhone']].to_dict()
                ReturnAgents.append(no_info_data)
            #if UserExists:
             #   no_info_data=row[['ListAgentFullName','ListAgentOfficePhone']].to_dict()
             #   ReturnAgents.append(no_info_data)       
        return Response(ReturnAgents)
    
    
        
