'''
Created on Nov 14, 2016

@author: cloudera
'''
from rest_framework import viewsets
from rest_framework.response import Response
from pymongo import MongoClient
from rest_framework_tracking.mixins import LoggingMixin
from oauth2_provider.ext.rest_framework import OAuth2Authentication, TokenHasScope


class AgentsRFM(LoggingMixin, viewsets.ViewSet):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['read']

    def list(self, request):
        """
        Agent Recommendation API(RFM):
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
#             try:
#                 if request.query_params['zip'] not in ZIPType:
#                     return Response({'status':'ERROR','error':'INVALID_POSTALCODE'})
        try:
                if request.query_params['level'].isdigit():
                    return Response({'status': 'ERROR', 'error': 'INVALID_LEVEL'})
        except:
                    return Response({'status': 'ERROR', 'error': 'NO_LEVEL_SPECIFIED'})
#             try:
#                 if  request.query_params['value'].isalpha():
#                     return Response({'status':'ERROR','error':'INVALID_VALUE'})
#             except:
#                 return Response({'status':'ERROR','error':'NO_VALUE_SPECIFIED'})
#             try:
#                 zipcode = pz.get(str(request.query_params['zip']),"US")
#             except:
#                 return Response({'status':'ERROR','error':'Invalid ZipCode'})
#
#             except:
#                 return Response({'status':'ERROR','error':'NO_SPAN_SPECIFIED'})
        db_client = MongoClient(host='mongo-master.propmix.io', port=33017)

        class RfmFilter:
                @staticmethod
                def rfm(level, value):

                    data = []
                    if level == 'County':
                        print level, type(value)
                        si_fips = int(value)
                        print type(si_fips)
                        data_ = list(db_client['RFM_mlslite'][level].find({'SI_FIPS': si_fips}, {'Agent_data.AgentName': 1, 'Agent_data.rfm': 1, 'Agent_data.R_Score': 1, 'Agent_data.F_Score': 1, 'Agent_data.M_Score': 1, 'Agent_data.last_transaction_dates': 1, 'Agent_data.AgentInfo': 1}).limit(10))
                    else:
                        data_ = list(db_client['RFM_mlslite'][level].find({level: value}, {'Agent_data.AgentName': 1, 'Agent_data.rfm': 1, 'Agent_data.R_Score': 1, 'Agent_data.F_Score': 1, 'Agent_data.M_Score': 1, 'Agent_data.last_transaction_dates': 1, 'Agent_data.AgentInfo': 1}).limit(10))
                    #print data_
                    print len(data_)
                    name = []
                    tenagents = []
                    for x in xrange(10):
                        tenagents.append(data_[0]['Agent_data'][x])
#
#                     for i in range(len(data_))[:10]:
#                         name.append(data_[i]['Agent_data'])

                    calc = {'Top Agents': tenagents}

                    return calc

        req_level = request.query_params['level']
        print req_level
        req_value = request.query_params['value']
        if req_level == 'State':
            if req_value.isdigit():
                return Response({'status': 'ERROR', 'error': 'INVALID_'})

            dat = RfmFilter.rfm('State', req_value)
            print type(dat)
            return Response(dat)

        elif req_level == 'County':
            dat = RfmFilter.rfm('County', req_value)
            return Response(dat)
        elif req_level == 'post':
            dat = RfmFilter.rfm('post', req_value)
            return Response(dat)

            #return Response(da)
#             elif req_level=='postal_code':
#                 RfmFilter.rfm('postal_code',req_value)
