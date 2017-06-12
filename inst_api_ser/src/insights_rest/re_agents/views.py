from rest_framework import viewsets
from rest_framework.response import Response
from pymongo import MongoClient
from rest_framework_tracking.mixins import LoggingMixin
from oauth2_provider.ext.rest_framework import OAuth2Authentication, TokenHasScope
from .dbauth import DATABASE_ACCESS


class AgentDetails(LoggingMixin, viewsets.ViewSet):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['read']

    def list(self, request):
        """
        Agent Details

        API will return details about Agents like their transaction details and personal informations.

        ---
        type:
          schema : { Agent Transactions: [{Transactions: []}], Agent Information: [{AgentInfo: []}]}
          Agent Transactions:
            required: true
            type: set
            sample:
                nested:
                    required: true
                    type: object

          Agent Information:
            required: false
            type: string


        omit_serializer: false
        parameters_strategy: merge
        omit_parameters:
            - path
        parameters:
            - name: agent
              description: State which agents should be recommended.
              type: string
              paramType: query
              defaultValue: Read Northen
            - name: State
              description: State in which agents transactions happening.
              type: string
              paramType: query
              defaultValue: NC
            - name: zip
              description: postalcode in  which agents performing well.
              type: string
              paramType: query
              defaultValue: 28411
            - name: phone
              description: Preffered phone number.
              type: string
              paramType: query
              allowEmptyValue: true
            - name: email
              description: agent's email id.
              type: string
              paramType: query
              allowEmptyValue: true


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
        dbclient = MongoClient(host='mongo-master.propmix.io', port=33017)
        dbclient.RFM.authenticate(**DATABASE_ACCESS)
        req_agent = request.query_params['agent']
        agent = list(dbclient.RFM.MLSLITE_LIST_AGENT_unique.find({"AgentName": req_agent}, {'postal_code': 1, 'AgentName': 1, '_id': False, 'R_Value': 1, 'F_Value': 1, 'M_Value': 1, 'AgentInfo.ListAgentPreferredPhone': 1, 'AgentInfo.ListAgentEmail': 1}))
        agenttrans = list(dbclient.RFM.MLSLITE_LIST_AGENT_unique.find({"AgentName": req_agent}, {'Transactions.ListAgentMlsId': 1, 'Transactions.CloseDate': 1, 'Transactions.ListPrice': 1, 'Transactions.server_id': 1, 'Transactions.ListAgentEmail': 1, 'Transactions.CountyOrParish': 1, '_id': False, 'Transactions.rets_id': 1, 'Transactions.ListAgentStateLicense': 1, 'Transactions.PostalCode': 1, 'Transactions.StateOrProvince': 1}))
        agentdata = {'Agent Information': agent, 'Agent Transactions': agenttrans}
        dbclient.close()
        return Response(agentdata)
