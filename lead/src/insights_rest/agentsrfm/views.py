'''
Created on 18-Aug-2016

@author: revathy.sivan
'''
from rest_framework import viewsets
from rest_framework.response import Response
from pymongo import MongoClient
import urllib2
import json
import pandas as pd
import numpy as np
from rest_framework_tracking.mixins import LoggingMixin
from oauth2_provider.ext.rest_framework import OAuth2Authentication, TokenHasScope


from .config import host
from config import Street_name
from .config import Radius_name
from .config import MonthsBack_name
from .config import data1_columns_name
from .read import read_fulldata
from .read import read_integer
from .read import euclidean_claculation
from .read import kmean_algorithm
from .read import agent_info_getng
import requests
from .config import City_name
from .config import State_name
from .config import PropertyType_name
from .config import PageSize_name
from .config import Longitude_name
from .config import Latitude_name
from .config import PageSize_Value
from .config import Zip_name
from .config import isZip_name
from .config import ZipON
from .dbauth import DATABASE_ACCESS


class BestFitAgent(LoggingMixin, viewsets.ViewSet):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['read']

    def list(self, request):
        """
        Best Fit API

        API will return the best agent who can handle the subject property.

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
              defaultValue: 1514 Cherry Flats Rd, Miami, AZ 85539, USA
            - name: SI_PropertyType
              description: the property belong to which property type like single family,Multifamily,etc.
              required: true
              paramType: query
              defaultValue: Residential
            - name: Zip
              description: To identify property belong to particular region
              required: true
              paramType: query
              defaultValue: 85539
            - name: radius
              description: To get property in this radius
              required: true
              paramType: query
              defaultValue: 2
            - name: GLA
              description: To get property similar to given GLA
              required: true
              paramType: query
              defaultValue: 1200
            - name: Beds
              description: To get property similar to given Beds
              required: true
              paramType: query
              defaultValue: 4
            - name: Baths
              description: To get property similar to given Baths
              required: true
              paramType: query
              defaultValue: 2
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
            - name: StoriesTotal
              description: To get property similar to given StoriesTotal
              required: true
              paramType: query
              defaultValue: 1
            - name: Distance
              description: To get property similar to given GarageYN
              required: true
              paramType: query
              defaultValue: 0
            - name: MonthsBack
              description: To get property similar to given MonthsBack
              required: true
              paramType: query
              defaultValue: 36
            - name: City
              description: To get property similar to given City
              required: true
              paramType: query
              defaultValue: Miami
            - name: State
              description: To get property similar to given State
              required: true
              paramType: query
              defaultValue: AZ


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
        address = request.query_params['address'].replace('"', '')
        if address:
            address = address
        else:
            return Response({'status': 'ERROR',
                             'error': 'Please Enter a valid address'})
        radius = ""
        if ("radius" in request.query_params):
            radius = request.query_params['radius']
        else:
            return Response({'status': 'ERROR',
                             'error': 'Please Enter a valid radius'})
        if ("SI_PropertyType" in request.query_params):
            PropertyType = request.query_params['SI_PropertyType']
        else:
            PropertyType = ""
        LotSizeArea = ""
        if ("LotSizeArea" in request.query_params):
            LotSizeArea = request.query_params['LotSizeArea']
        else:
            return Response({'status': 'ERROR',
                             'error': 'Please Enter a valid LotSizeArea'})
        Beds = ""
        if ("Beds" in request.query_params):
            Beds = request.query_params['Beds']
        else:
            return Response({'status': 'ERROR',
                             'error': 'Please Enter a valid Beds'})
        Baths = ""
        if ("Baths" in request.query_params):
            Baths = request.query_params['Baths']
        else:
            return Response({'status': 'ERROR',
                             'error': 'Please Enter a valid Baths'})
        GLA = ""
        if ("GLA" in request.query_params):
            GLA = request.query_params['GLA']
        else:
            return Response({'status': 'ERROR',
                             'error': 'Please Enter a valid GLA'})
        if ("YearBuilt" in request.query_params):
            request.query_params['YearBuilt']
        else:
            return Response({'status': 'ERROR',
                             'error': 'Please Enter a valid YearBuilt'})

        YearBuilt = request.query_params['YearBuilt']

        try:
            if not request.query_params['YearBuilt'].isdigit():
                return Response({'status': 'ERROR',
                                'error': 'INVALID_YearBuilt'})
        except:
            return Response({'status': 'ERROR',
                             'error': 'NO_YearBuilt_SPECIFIED'})
        StoriesTotal = ""
        if ("StoriesTotal" in request.query_params):
            StoriesTotal = request.query_params['StoriesTotal']
        else:
            StoriesTotal = ""
        Distance = 0
        if ("Longitude" in request.query_params):
            Longitude = request.query_params['Longitude']
        else:
            Longitude = ""
        if ("Latitude" in request.query_params):
            Latitude = request.query_params['Latitude']
        else:
            Latitude = ""
        if ("Zip" in request.query_params):
            Zip = request.query_params['Zip']
        else:
            return Response({'status': 'ERROR',
                             'error': 'NO_Zip_SPECIFIED'})
        try:
            radius = float(radius)
            LotSizeArea = float(LotSizeArea)
            Beds = float(Beds)
            Baths = float(Baths)
            GLA = float(GLA)
            StoriesTotal = float(StoriesTotal)
            Zip = str(Zip)
        except:
            return Response({'status': 'ERROR',
                             'error': 'Integer_float_SPECIFIED'})
        MonthsBack = ""
        if ("MonthsBack" in request.query_params):
            MonthsBack = request.query_params['MonthsBack']
        else:
            return Response({'status': 'ERROR',
                             'error': 'Please Enter a valid MonthsBack'})
        City = ""

        if ("City" in request.query_params):
            City = request.query_params['City']
        else:
            return Response({'status': 'ERROR',
                             'error': 'Please Enter a valid City'})
        State = ""

        if ("State" in request.query_params):
            State = request.query_params['State']
        else:
            return Response({'status': 'ERROR',
                             'error': 'Please Enter a valid State'})

        try:
            PageSize = PageSize_Value
            url_map = "%s%s={address}&%s={radius}\
            &%s={MonthsBack}&%s={City}&%s={State}\
            &%s={PropertyType}&%s={PageSize}\
            &%s={Longitude}&%s={Latitude}\
            &%s={Zip}&%s={ZipON}" % (host,
                                     Street_name,
                                     Radius_name,
                                     MonthsBack_name,
                                     City_name,
                                     State_name,
                                     PropertyType_name,
                                     PageSize_name,
                                     Longitude_name,
                                     Latitude_name,
                                     Zip_name,
                                     isZip_name
                                     )

            url = (url_map).format(address=urllib2.quote(address),
                                   radius=radius, State=State,
                                   MonthsBack=MonthsBack,
                                   City=City, PageSize=PageSize,
                                   PropertyType=PropertyType,
                                   Latitude=Latitude,
                                   Longitude=Longitude,
                                   Zip=Zip,
                                   ZipON=ZipON)
        except:
            return Response({'status': 'ERROR',
                             'error': 'Unable to load Data in\
                              url map Please try after some time'})
        try:
            response = requests.get(url)
        except:
            return Response({'status': 'ERROR',
                             'error': 'Unable to load Data\
                              Please try after some time'})
        try:
            data = json.loads(response.text)
        except:
            return Response({'status': 'ERROR',
                             'error': 'Unable to load Data\
                              Please try after some time'})

        try:
            c = read_fulldata(data)

        except:
            print "error in data reading block1"
            return Response({'status': 'ERROR',
                             'error': 'Unable to load Data\
                              from input api please try after some time'})
        if c.empty:
                return Response({'status': 'ERROR',
                                 'error': 'no  property in the current list1'})
        else:
            c = c
        try:
            x = read_integer(data)
        except:
            print "error in data reading block2"
            return Response({'status': 'ERROR',
                            'error': 'Unable to load Data \
                            from input api please try after some time'})
        if x.empty:
            return Response({'status': 'ERROR',
                             'error': 'no  property in the current list'})
        else:
            x = x
        try:
            xx = x.ix[:, 0:8]
            x1 = xx.replace(r'\s+', np.nan, regex=True).replace('', np.nan)
            x1 = x1.replace("[+]", "", regex=True)
            x1_count = len(x1.index)
            x11 = x1.as_matrix()
            x1 = x11.astype(float)
            valid = np.isfinite(x1)
            mu = np.nanmean(x1, 0, keepdims=1)
            X_hat = np.where(valid, x1, mu)
            if x1_count > 50:
                        range_value = 20
                        n_clusters = 8
                        n_jobs = -1
                        X_hat = kmean_algorithm(range_value, n_clusters,
                                                n_jobs, X_hat,
                                                valid)
            elif x1_count > 10:
                        range_value = 10
                        n_clusters = 3
                        n_jobs = -1
                        X_hat = kmean_algorithm(range_value, n_clusters,
                                                n_jobs, X_hat,
                                                valid)
            else:
                        range_value = 2
                        n_clusters = 2
                        n_jobs = -1
                        X_hat = kmean_algorithm(range_value, n_clusters,
                                                n_jobs, X_hat,
                                                valid)
            x2 = X_hat
            x2 = pd.DataFrame(x2)
            x2.columns = data1_columns_name
        except:
            return Response({'status': 'ERROR',
                            'error': 'Error occur in Missing value handling '})
        try:
            x = x2.append({'Distance': Distance,
                           'LotSizeArea': LotSizeArea,
                           'GLA': GLA,
                           'Beds': Beds,
                           'Baths': Baths,
                           'YearBuilt': YearBuilt},
                          ignore_index='true')
        except:
            print "error in mean append block"
            return Response({'status': 'ERROR',
                             'error': 'please try after some time'})
        try:
            c = euclidean_claculation(x, c)
        except:
            print "error in euclidean block"
            return Response({'status': 'ERROR',
                             'error': 'please try after some time'})
        try:
            ReturnAgents = agent_info_getng(c, Zip)
            return Response(ReturnAgents)
        except:
            print "error in agent information collecting"
            return Response({'status': 'ERROR',
                             'error': 'please try after some time'})


class Top10Agents(LoggingMixin, viewsets.ViewSet):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['read']

    def list(self, request):
        """
        Agent Recommendation API

        API will return the best 10 agents in your State/County/Postalcode

        ---
        # YAML (must be separated by `---`)
        type:
          schema : { Top Agents: [{AgentInfo: []}]}
          Top Agents:
            required: true
            type: set
            sample:
                nested:
                    required: true
                    type: object

          AgentInfo:
            required: false
            type: string



        omit_serializer: false
        parameters_strategy: merge
        omit_parameters:
            - path
        parameters:
            - name: level
              description: State which agents should be recommended.
              type: string
              paramType: query
              defaultValue: State
            - name: value
              description: different states in US.
              paramType: query
              defaultValue: IL

        responseMessages:
            - code: 401
              message: Not authenticated
            - code : 404
              message: Not Found
            - code : ERROR
              message : No STATE Specified or Invalid STATE

        consumes:
            - application/json
            - application/xml
        produces:
            - application/json
            - application/xml
        """
        try:
                if request.query_params['level'].isdigit():
                    return Response({'status': 'ERROR',
                                     'error': 'INVALID_LEVEL'})
        except:
                    return Response({'status': 'ERROR',
                                     'error': 'NO_LEVEL_SPECIFIED'})

        class RfmFilter:
                @staticmethod
                def rfm(level, value):
                    db_client = MongoClient(host='mongo-master.propmix.io', port=33017)
                    db_client.RFM_mlslite.authenticate(**DATABASE_ACCESS)
                    data = []
                    if level == 'County':
                        si_fips = int(value)
                        data = list(db_client['RFM_mlslite'][level].find(
                            {'SI_FIPS': si_fips}, {'Agent_data.AgentName': 1,
                                                   'Agent_data.rfm': 1,
                                                   'Agent_data.R_Score': 1,
                                                   'Agent_data.F_Score': 1,
                                                   'Agent_data.M_Score': 1,
                                                   'Agent_data.last_\
                                                   transaction_dates': 1,
                                                   'Agent_data.AgentInfo': 1}
                                                                         )
                                    .limit(10))
                    else:
                        data = list(db_client['RFM_mlslite'][level].find(
                            {level: value}, {'Agent_data.AgentName': 1,
                                             'Agent_data.rfm': 1,
                                             'Agent_data.R_Score': 1,
                                             'Agent_data.F_Score': 1,
                                             'Agent_data.M_Score': 1,
                                             'Agent_data.last_\
                                             transaction_dates': 1,
                                             'Agent_data.AgentInfo': 1})
                                    .limit(10))
                    tenagents = []
                    for x in xrange(10):
                        tenagents.append(data[0]['Agent_data'][x])

                    calc = {'Top Agents': tenagents}
                    db_client.close()
                    return calc

        req_level = request.query_params['level']
        req_value = request.query_params['value']
        if req_level == 'State':
            if req_value.isdigit():
                return Response({'status': 'ERROR', 'error': 'INVALID VALUE'})

            dat = RfmFilter.rfm('State', req_value)
            return Response(dat)

        elif req_level == 'County':
            dat = RfmFilter.rfm('County', req_value)
            return Response(dat)
        elif req_level == 'PostalCode':
            dat = RfmFilter.rfm('post', req_value)
            return Response(dat)
        else:
            return Response({'status':'ERROR', 'error':'INVALID LEVEL'})
