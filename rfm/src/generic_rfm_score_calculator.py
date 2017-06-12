from pymongo import MongoClient
import pandas as pd
import numpy as np
import json
db_client = MongoClient(host='52.91.122.15', port=27017)
class DBFilter():
            
            @staticmethod
            def filter(level):


                data =  list(db_client.RFM.agent_list.distinct(level))
                print len(data)
                for i in data:
                    
                         print i
                         agents = list(db_client.RFM.agent_list.find({level:i},{"R_Value":1,"M_Value":1,'AgentName':1,'last_transaction_dates':1,"F_Value":1,'Transactions.ListAgentMlsId':1}))
                         #print agents
                         fuldata_=[]
                         
                        #print agents
                        #print range(len(agents))
                         for row in agents:
                                ful={}
                                print row['AgentName']
                                                           
                                ful['R_Value']=row['R_Value']
                                ful['M_Value']=row['M_Value']
                                ful['F_Value']=row['F_Value'] 
                                ful['AgentName']=row['AgentName']
                                ful['last_transaction_dates']=row['last_transaction_dates']
                                #fuldata_.append(ful)
                                 
                                 
                                 
                                id=row['Transactions'][0]
                                ful['ListAgentMlsId']=id['ListAgentMlsId']
#                                 for i in id:
#                                     ful['ListAgentMlsId']=id['ListAgentMlsId']
                                fuldata_.append(ful)   
                         
                                 
#                             fuldata['R_Value']=agents[row]['R_Value']
#                             fuldata['id']=agents[row][0]['ListAgentMlsId']
                             
                         print fuldata_
#                 
#                 
# #                             #print x
                         x = pd.DataFrame(fuldata_)
                         #x = x.rename(columns={'number of Transactions': 'Frequency'})
                         #print x   
                         def getR_Score(x,r=5,f=5,m=5):
                             if r<=0 or f<=0 or m<=0: return
                             x=x.sort(['R_Value', 'F_Value','M_Value'], ascending=[1, 0, 0])
                             x=x.reset_index(level=0)
                         #    print x.index.tolist()
                             x=x.loc[x.index.tolist()]
                             R_Score = scoring(x,'R_Value',r)
                             x['R_Score'] =R_Score
                             return (R_Score)
                         def getF_Score(x,r=5,f=5,m=5):
                             if r<=0 or f<=0 or m<=0: return
                             x=x.sort(['F_Value', 'R_Value','M_Value'], ascending=[0, 1, 0])
                             x=x.reset_index(level=0)
                             x=x.loc[x.index.tolist()]
                             F_Score = scoring(x,'F_Value',f)
                             x['F_Score'] =F_Score
                             return (F_Score)
                             
                         def getM_Score(x,r=5,f=5,m=5): 
                             if r<=0 or f<=0 or m<=0: return
                             x=x.sort(['M_Value', 'R_Value','F_Value'], ascending=[0, 1, 0])
                             x=x.reset_index(level=0)
                             x=x.loc[x.index.tolist()]
                             M_Score = scoring(x,'M_Value',m)
                             x['M_Score'] =M_Score
                             return (M_Score)
                          
                         def scoring(x,column,r=5):
                         #    print x
                             length = len(x)
                         #    score=np.zeros((length, length))
                             score=np.repeat(0, length, axis=0)
                             nr =round(length/r)
                             if nr > 0:
                                rStart =0
                                rEnd = 0 
                             for i in range(1,r+1):
                                 rStart = rEnd+1
                                 if rStart> i*nr: 
                                     continue
                                 if i == r:
                                     if rStart<=length : 
                                         rEnd = length 
                                     else: 
                                         continue
                                 else:
                                     rEnd = i*nr
                         #        print "changing: (%d,%d) to %d" %(rStart-1,rEnd,r-i+1)
                                 score[rStart-1:rEnd]= r-i+1
                                 s=int(rEnd)
                         #        print s
                                 if i<r and s <= length:
                                    for u in range(s,length):
                         #               print "%s: (%d , %d)=(%d(%d) , %d(%d)):%d" % (column,rEnd,u,x[column][rEnd],score[rEnd],x[column][u],score[u],(r-i+1))
                                        if x[column][rEnd]==x[column][u]:
                         #                  print "assigining %d to %d "% (r-i+1,u)
                                           score[u]= r-i+1
                                           
                                        else:
                                            rEnd = u
                                            break
                                             
                             return(score)
                     
                         x['R_Score']=getR_Score(x)
                         x['F_Score']=getF_Score(x)
                         x['M_Score']=getM_Score(x)
                         x = x.sort(['R_Score','F_Score','M_Score'],ascending=[0, 0, 0])
                         #db_client.RFM.rfm_value_zip_calc.insert({x})
                         for item in range(0,len(x)):
                             #print x['R_Score']
                             r=x['R_Score']
                             f=x['F_Score']
                             m=x['M_Score']
                             RFM_Score = (5*r + 3*f+2*m)
                             x['rfm']=RFM_Score
                             #print x['rfm']
                         
                         #records = json.loads(x.to_json()).values()
                         #db_client.RFM.rfm_value_zip_calc.insert(records)    
                         record=x.to_dict('records')
                         #record
                         #print i
                         agent={level:i,"Agent_data":record}
                         #db_client.RFM.RFMSCORE_state.insert(agent)
                         #print agent
                         db_client["RFM"][level].insert(agent)
                         print 'pass'
                         #getval(x)
                      
DBFilter.filter("states")
DBFilter.filter("County")
#DBFilter.filter("postal_code")             
