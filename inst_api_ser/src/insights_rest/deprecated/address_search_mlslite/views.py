'''
Created on Sep 27, 2016

@author: vishnu.sk
'''
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from pymongo import MongoClient
from geopy.geocoders import Nominatim
@permission_classes((permissions.AllowAny,))
class address_search(viewsets.ViewSet):
    
    def list(self, request):
        radius=request.query_params['radius']  
      
        try:
            if not request.query_params['radius'].isdigit():
                return Response({'status':'ERROR','error':'INVALID_radius'})
        except:
                return Response({'status':'ERROR','error':'NO_radius_SPECIFIED'})
        SI_Address = ""

        if ("SI_Address" in request.query_params):
           SI_Address = request.query_params['SI_Address']
        else:
           return Response({'status': 'ERROR',
                            'error': 'Please Enter a valid SI_Address'})
        geolocator = Nominatim()
        location = geolocator.geocode(SI_Address, timeout=10)   
        latitude=location.latitude
        longitude=location.longitude
        db_client = MongoClient(host='mongo-master.propmix.io', port=33017)
        lat=float(latitude)
        long=float(longitude)
        rad=int(radius)
        data_1=list(db_client.MLSLite.miami1L.find({"$where":"getDistanceFromLatLonInKm(%s,%s,this.Latitude,this.Longitude) <= %s"%(lat,long,rad)},{'UnparsedAddress':1,'City':1,'StateOrProvince':1, 'PostalCode':1, 'PostalCodePlus4':1, 'ParcelNumber':1,
              'PropertyType':1,
              'PropertySubType':1,
              'LotSizeSquareFeet':1,
              'LivingArea':1,
              'ArchitecturalStyle':1,
              'Heating':1,
              'Cooling':1,
              'StoriesTotal':1,
              'Stories':1,
              'YearBuilt':1,
              'Roof':1,
              'ConstructionMaterials':1,
              'BedroomsTotal':1,
              'BathroomsTotalInteger':1,
              'ParkingFeatures':1,
              'PoolFeatures':1,
              'View':1,
              'PatioAndPorchFeatures':1,
              'Basement':1,
              'FireplacesTotal':1,
              'FireplaceYN':1,
              'FireplaceFeatures':1,
              'InteriorFeatures':1,
              'ExteriorFeatures':1,
              'OtherStructures':1,
              'PublicRemarks':1,
              'LotFeatures':1,
              'ZoningDescription':1,
              'CommunityFeatures':1,
              'ElementarySchoolDistrict':1,
              'MiddleOrJuniorSchoolDistrict':1,
              'HighSchoolDistrict':1,
              'ElementarySchool':1,
              'MiddleOrJuniorSchool':1,
              'HighSchool':1,
              'Appliances':1,
              'LotSizeDimensions':1,
              'Topography':1,
              'WaterSource':1,
              'ListingContractDate':1,
              'StandardStatus':1,
              'MlsStatus':1,
              'ListPrice':1,
              'CloseDate':1,
              'ListAgentStateLicense':1,
              'ListAgentFullName':1,
              'ListAgentPreferredPhone':1,
              'ListAgentEmail':1,
              'ListOfficeName':1,
              'ListOfficePhone':1,
              'ListOfficeEmail':1,
              'ListingId':1,
              'ListingKey':1,
              'ModificationTimestamp':1,
              'SI_FIPS':1,
              'SI_PropertyRefID':1,
              'SI_PriceperSquareFeet':1,
              'WaterfrontFeatures':1,
              'SI_WaterYN':1,
              'SI_DaysOnMarket':1,
              'SI_ListingNumber':1,
              'SI_SoldPriceRange':1,
              'SI_AdjustedSoldPrice':1,
              'MemberAddress1':1,
              'OfficeAddress1':1,
              'Latitude':1,
              'Longitude':1,
              'Distance':1,
              'SubjectProperty':1}))
        for i in data_1:
            if i["Latitude"]==latitude:
                i["subject_property"]="true"
            else:    
                i["subject_property"]="false"
        
        map(lambda data_1: data_1.pop('_id'), data_1)
        finalObj = {"Listings":data_1,"Total_Comparables":len(data_1)}
        return Response(finalObj)
