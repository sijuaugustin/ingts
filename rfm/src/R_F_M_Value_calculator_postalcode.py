# import
from pymongo import MongoClient
import datetime
import time
#data fetch from mongo
db_client = MongoClient(host='52.91.122.15', port=27017)
agents= list(db_client.RFM.agent_list.distinct("AgentName"))
#RFM_Value Calculation
def calculateRFM(postalCodeDict,agentName):
    print agentName
    minDate=0
    for postalCode in postalCodeDict.keys():
        
        maxMilSec = 0
        Frequency=len(postalCodeDict[postalCode])
        TotalDeviationsum=0
        for Trans in postalCodeDict[postalCode]:
            if Trans["ClosePrice"] is None:
                continue
            if Trans["ListPrice"] is None:
                continue
            closedateMilli = datetime.datetime.strptime(Trans["CloseDate"], "%Y-%m-%d")
            epoch = datetime.datetime.utcfromtimestamp(0)
            def unix_time_millis(dt):
                return (dt - epoch).total_seconds() * 1000.0
            milliseconds = unix_time_millis(closedateMilli)
            if milliseconds>maxMilSec:
               minDate=Trans["CloseDate"]
               maxMilSec=milliseconds
            deviation = abs(Trans['ListPrice'] - Trans["ClosePrice"])

            TotalDeviationsum = TotalDeviationsum + deviation
        Recency = (milliseconds_end_date-maxMilSec)
        if Frequency == 0:
            Monetary = 0
        else:
            Monetary = TotalDeviationsum/Frequency
        last_transaction_date=minDate
        print last_transaction_date
        print "postal Code: ",postalCode
        print Recency
        print Frequency
        print TotalDeviationsum,"/",Frequency,": ",Monetary
        print Monetary
#        zipdata={'recenccy':Recency,'frequency':Frequency,'monetary':Monetary,'Recent_transaction_date':last_transaction_date}
#        zip_transactions={"post":postalCode,'rfm data':zipdata,'recenccy':Recency}
#        agentdata={'AgentName':agentName,'postal_code':zip_transactions}
        agentdata={"post":postalCode,'AgentName':agentName,'recenccy':Recency,'frequency':Frequency,'monetary':Monetary,'Recent_transaction_date':last_transaction_date}
#        print agentdata
        db_client.RFM.PostalCodebased_rfm_value.insert(agentdata)
#Current date convert to milliSecond        
end_date = time.strftime("%Y-%m-%d")
end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
epoch = datetime.datetime.utcfromtimestamp(0)
unix_time_millis = (end_date - epoch).total_seconds() * 1000.0
date_time = "date_time string to datetime logic"
milliseconds_end_date = unix_time_millis

#Postal_Code wise data fetching
for row in agents :  
    postalCodeFilter={};
    agnt = {}
    agentdata=db_client.RFM.agent_list.find_one({"AgentName":row})
    Frequency = agentdata["number of Transactions"]
    agentName=agentdata["AgentName"]

    transaction = agentdata['Transactions']
    
    postlist=[]
    maxMilSec = 0
    sum1=0
    for trans in transaction:
        #postalCodeFilter={};
        Postal_code=trans['PostalCode']
        if Postal_code in postalCodeFilter.keys():
           postalCodeFilter[Postal_code].append(trans)
           postalCodeFilter.update(postalCodeFilter)
        else:
           postalCodeFilter[Postal_code]=[trans]
           postalCodeFilter.update(postalCodeFilter)         
    calculateRFM(postalCodeFilter,agentName)
    
        
        


