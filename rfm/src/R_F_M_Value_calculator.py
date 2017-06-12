# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 10:21:50 2016

@author: revathy.sivan
"""

from pymongo import MongoClient
import datetime
import time
import re
db_client = MongoClient(host='169.45.215.122', port=27017)
agents= list(db_client.RFM.agent_list.distinct("AgentName"))
    
end_date = time.strftime("%Y-%m-%d")
end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
epoch = datetime.datetime.utcfromtimestamp(0)
unix_time_millis = (end_date - epoch).total_seconds() * 1000.0
date_time = "date_time string to datetime logic"
milliseconds_end_date = unix_time_millis
for row in agents :
    agnt = {}
    agentdata=db_client.RFM.agent_list.find_one({"AgentName":row})
    Frequency = agentdata["number of Transactions"]
    transaction = agentdata['Transactions']
    maxMilSec = 0
    minDate=0
    Postal_code_=0
    County_=0
    State_=0
    info={}
    count = 0
    sum1 = 0
    postlist=[]
    for trans in transaction:
        Postal_code=trans['PostalCode']
        County=trans['CountyOrParish']
        State=trans['StateOrProvince']
        closedate=trans['CloseDate']
        count = count + 1
#        if Postal_code is not  postlist:
        postlist.append(Postal_code)
        
#        set(postlist)
        if trans['ClosePrice'] is not None:
                closeprice = trans['ClosePrice']
        if trans['ListPrice'] is not None:
                listprice = trans['ListPrice']
        closedate1 = datetime.datetime.strptime(closedate, "%Y-%m-%d")
        epoch = datetime.datetime.utcfromtimestamp(0)
        def unix_time_millis(dt):
            return (dt - epoch).total_seconds() * 1000.0
        milliseconds = unix_time_millis(closedate1)
        if milliseconds>maxMilSec:
           minDate=closedate
           maxMilSec=milliseconds
           Postal_code_=Postal_code
           County_=County
           State_=State
        deviation = abs(listprice - closeprice)
        sum1 = sum1 + deviation
    post=list(set(postlist))
    for count in range(len(post)):
        print count
        agentdata['postal_code']=post[count]           
    Recency = (milliseconds_end_date-maxMilSec)
    postal_code1=Postal_code_
    County1=County_
    state1=State_
    last_transaction_date=minDate
#    agentdata['postal_code']=post
    agentdata['R_Value']=Recency
    agentdata['County']=County1
    agentdata['states']=state1
    agentdata['last_transaction_dates']=last_transaction_date
    
    if Frequency == 0:
            Monetary = 0
    else:
            Monetary = sum1/Frequency
    agentdata['M_Value']=Monetary
    agentdata['F_Value']=Frequency 
    #print agentdata
#    raw_input()
    db_client.RFM.agent_list.save(agentdata) 
    print 'pass'    