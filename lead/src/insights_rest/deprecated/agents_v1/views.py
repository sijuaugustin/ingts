'''
Created on Sep 27, 2016

@author: cloudera
'''
from rest_framework import viewsets
from rest_framework.response import  Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions  
from pymongo import MongoClient
@permission_classes((permissions.AllowAny,))

class Agent(viewsets.ViewSet):
    def list(self,request):
        """
        Agent  API(RFM) :API will return all the details about Agents like their transaction  details and personal informations.
       


        url:https://insights.propmix.io:8004/RFMAgents/Agent/?agent=A%20G%20Krone
        

        ---
        # YAML (must be separated by `---`)
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
              defaultValue: A Douglas Anderson

          
    
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
            if  request.query_params['agentid'].isalpha():
                return Response({'status':'ERROR','error':'INVALID_AGENT_ID'})
            if not request.query_params['agentid']:
                return Response({'status':'ERROR','error':'INVALID_AGENT_ID'})
            else:
                req_agentid=request.query_params['agentid']
             
             
#             if request.query_params['agent'] not in SpanType:
#                 return Response({'status':'ERROR','error':'INVALID_SPAN'})
#             elif request.query_params['attribute'] not in AtrType:
#                 return Response({'status':'ERROR','error':'INVALID_ATTRIBUTE_NAME'})                  
        except:
                return Response({'status':'ERROR','error':'NO_ID_SPECIFIED'}) 
        
        
        
        req_agentid=request.query_params['agentid']
        dbclient= MongoClient(host='mongo-master.propmix.io',port=33017)
        #req_agent=request.query_params['agent']
        agent=list(dbclient.RFM.agent_list.find({"Transactions.ListAgentMlsId" :req_agentid},{'postal_code':1,'AgentName':1,'_id': False,'R_Value':1,'F_Value':1,'M_Value':1}))
        #'Transactions.ListOfficeKey':1,'Transactions.ListOfficeName':1,'Transactions.ListAgentMlsId':1,'Transactions.ListAgentPreferredPhone':1,'Transactions.ListAgentEmail':1,'Transactions.ListAgentKey':1,'Transactions.CountyOrParish':1,'Transactions.ListOfficeMlsId':1,'Transactions.ListAgentStateLicense':1,'Transactions.ListAgentFax':1,'Transactions.ListAgentOfficePhone':1,'Transactions.StateOrProvince':1
#         
#         for i in agent:
#             AGNT={}
#             AGNT['POSTAL CODE']=i['postal_code']
#             AGNT['AGENT NAME']=i['AgentName']
#             AGNT['ListOfficeKey']=i['Transactions']['ListOfficeKey']
        agenttrans=list(dbclient.RFM.agent_list.find({"Transactions.ListAgentMlsId" :req_agentid},{'Transactions.ListAgentMlsId':1,'Transactions.CloseDate':1,'Transactions.ListPrice':1,'Transactions.server_id':1,'Transactions.ListAgentEmail':1,'Transactions.CountyOrParish':1,'_id': False,'Transactions.rets_id':1,'Transactions.ListAgentStateLicense':1,'Transactions.PostalCode':1,'Transactions.StateOrProvince':1}))
#         agentinfo=[]
#         for row in range(len(agenttrans)):
#             agentinfo=agenttrans[row]['Transactions']
#             print row
#             print agentinfo
        #print agentinfo
#         for i in  agent:
#             agentinfo.append(i)
        agentdata={'Agent Information':agent,'Agent Transactions':agenttrans}
        #print agentdata
        return Response(agentdata)
