# -*- coding: utf-8 -*-
"""
Created on Thu Oct 06 11:52:27 2016

@author: mohin.km
"""
'''
Created on Aug 30, 2016

@author: Mohin.km
'''

from pymongo import MongoClient
import pandas as pd
import numpy as np
import json
db_client = MongoClient(host='52.91.122.15', port=27017)
class DBFilter():
            
            @staticmethod
            def filter(level):


                data =  list(db_client.RFM.agent_list_copy.distinct(level))
                print len(data)
                for i in data:
#                   try:
                        #print i
                        agents = list(db_client.RFM.agent_list_copy.find({level:i,'ratings':{"$exists":1},'sold_homes':{"$exists":1},'active_listings':{"$exists":1}},
                                                                     {"R_Value":1,"M_Value":1,'AgentName':1,'last_transaction_dates':1,"F_Value":1,'ratings':1,'sold_homes':1,'active_listings':1}))
                        print len(agents)
                        #print x
                        x = pd.DataFrame(agents)
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
                        
                        def agents_score(agents):
                            for agent in agents:
                                if agent.has_key('ratings'):
                                    #print 'yes'
                                    ratings =  agent['ratings']
                                    #print ratings
                                if agent.has_key('sold_homes'):
                                    sold_homes = agent['sold_homes']
                                    #print sold_homes
                                if agent.has_key('active_listings'):
                                   active_listings =  agent['active_listings']
                            #       #print active_listings
                                agent_score = ( sold_homes + active_listings)/2
                                
                                minimumscore=min(agent_score)
                                for score in agent_score:
                                    
                                    scores = ((score - minimumscore)/ deviation)*100   
                                return scores
                            
                            
                            
                        x['R_Score']=getR_Score(x)
                        x['F_Score']=getF_Score(x)
                        x['M_Score']=getM_Score(x)
                        x['agent_score']=agents_score(agents)
                        x = x.sort(['R_Score','F_Score','M_Score'],ascending=[0, 0, 0])
                        #db_client.RFM.rfm_value_zip_calc.insert({x})
                        for item in range(1,len(x)):
                            #print x['R_Score']
                            r=x['R_Score']
                            f=x['F_Score']
                            m=x['M_Score']
                            agntscore=x['agent_score']
                            RFM_Score = (5*r + 3*f+2*m)
                            x['rfm']=RFM_Score
                            x['finalscore']=(RFM_Score+agntscore)/2
                        #agent_score=x['agent_score'] 
                            #print x['rfm']
                        
                        
                        record=x.to_dict('records')
                        agent={level:i,"Agent_data":record}
                        #db_client.RFM.RFMSCORE_state.insert(agent)
                        db_client["RFM"][level].insert(agent)
                        print 'pass'
                        #getval(x)
#                    except:
#                         print 'internal error'

DBFilter.filter("states") 
DBFilter.filter("County")
#DBFilter.filter("postal_code")         
 
   


