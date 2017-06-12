from pymongo import MongoClient
import pandas as pd
import numpy as np
import json
db_client = MongoClient(host='52.91.122.15', port=27017)
class DBFilter():
            
            @staticmethod
            def filter(level):

                
                data =  list(db_client.RFM.PostalCodebased_rfm_value.distinct(level))
                print len(data)
                for i in data:
                    try:
                        print i
                        
                        agents = list(db_client.RFM.PostalCodebased_rfm_value.find({level:i},{"recenccy":1,"monetary":1,'AgentName':1,'Recent_transaction_date':1,"frequency":1}))
                        x = pd.DataFrame(agents)
                        def getR_Score(x,r=5,f=5,m=5):
                            if r<=0 or f<=0 or m<=0: return
                            x=x.sort(['recenccy', 'frequency','monetary'], ascending=[1, 0, 0])
                            x=x.reset_index(level=0)
                            x=x.loc[x.index.tolist()]
                            R_Score = scoring(x,'recenccy',r)
                            x['R_Score'] =R_Score
                            return (R_Score)
                        def getF_Score(x,r=5,f=5,m=5):
                            if r<=0 or f<=0 or m<=0: return
                            x=x.sort(['frequency', 'recenccy','monetary'], ascending=[0, 1, 0])
                            x=x.reset_index(level=0)
                            x=x.loc[x.index.tolist()]
                            F_Score = scoring(x,'frequency',f)
                            x['F_Score'] =F_Score
                            return (F_Score)
                            
                        def getM_Score(x,r=5,f=5,m=5): 
                            if r<=0 or f<=0 or m<=0: return
                            x=x.sort(['monetary', 'recenccy','frequency'], ascending=[0, 1, 0])
                            x=x.reset_index(level=0)
                            x=x.loc[x.index.tolist()]
                            M_Score = scoring(x,'monetary',m)
                            x['M_Score'] =M_Score
                            return (M_Score)
                         
                        def scoring(x,column,r=5):
                            
                            length = len(x)
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
                                score[rStart-1:rEnd]= r-i+1
                                s=int(rEnd)
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
                        print x
                        #db_client.RFM.rfm_value_zip_calc.insert({x})
                        for item in range(1,len(x)):
                            #print x['R_Score']
                            r=x['R_Score']
                            f=x['F_Score']
                            m=x['M_Score']
                            #5,3,2 are first 3 prime numbers
                            RFM_Score = (5*r + 3*f+2*m)
                            x['rfm']=RFM_Score 
                        record=x.to_dict('records')
                        agent={level:i,"Agent_data":record}
                        db_client["RFM"][level].insert(agent)
                        print 'pass'
                    except:
                        print "no sufficient Agentdata"
                    
#DBFilter.filter("state") 
#DBFilter.filter("County")
#post stands for postal code                     
DBFilter.filter("post") 
