'''
Created on Nov 11, 2016

@author: revathy.sivan
'''
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from config import columnlist
from config import columnlist1
from config import c_data_value
from config import c_data_name
from pymongo import MongoClient
from .dbauth import DATABASE_ACCESS


def read_fulldata(data):
    columns_list1 = columnlist1
    array1 = []
    for list_item in data['Listings'][:-1]:
        features = []
        for column in columns_list1:
            features.append(list_item[column])
        array1.append(features)
    x1 = pd.DataFrame(data=array1)
    c = pd.DataFrame(x1, columns=c_data_value)
    c.columns = c_data_name
    a = 'Sold'
    c = c.loc[c['SI_Status'].isin([a])]
    return (c)


def read_integer(data):
    columns_list = columnlist
    array = []
    for list_item in data['Listings'][:-1]:
        features = []
        for column in columns_list:
            features.append(list_item[column])
        array.append(features)
    x = pd.DataFrame(data=array)
    x.columns = columnlist
    a = 'Sold'
    x = x.loc[x['MlsStatus'].isin([a])]
    return (x)


def kmean_algorithm(range_value, n_clusters, n_jobs, X_hat, valid):
    for _ in range(range_value):
        cls = KMeans(n_clusters=n_clusters, n_jobs=n_jobs)
        labels_hat = cls.fit_predict(X_hat)
        X_hat[~valid] = cls.cluster_centers_[labels_hat][~valid]
    return(X_hat)


def euclidean_claculation(x, c):

        d = len(x.index) - 1
        mean = x.loc[d]
        mean = np.array(mean, dtype='int32').tolist()
        l = len(x.columns)
        x.columns = [range(l)]
        x = x.convert_objects(convert_numeric=True)
        for index in range(len(x.columns)):
            x[index] = abs(mean[index] - x[index])
        mR = x.apply(lambda dh: np.sum(dh), axis=1)
        mR = mR[0:-1]
        c['similarity_score'] = mR
        c = c.sort(['similarity_score'], ascending=1)
        return (c)


def agent_info_getng(c, Zip):
    db_client = MongoClient(host='mongo-master.propmix.io', port=33017)
    db_client.RFM_mlslite.authenticate(**DATABASE_ACCESS)
    if len(c['ListAgentFullName']) != 0:
        Topten_similar_property = c[:10]
    agents = list(db_client.RFM_mlslite.post.find({"post": Zip}))
    ReturnAgents = []
    for _, row in Topten_similar_property.iterrows():
        Best_fit_agent = row['ListAgentFullName']
        if len(Best_fit_agent) == 0:
            continue
        UserNotExists = True
        for agentinfo_ in agents[0]['Agent_data']:
            if agentinfo_['AgentName'] == Best_fit_agent:
                agentinfo_.pop('_id', None)
                agentinfo_['ListAgentPreferredPhone'] = row['ListAgentPreferredPhone']
                agentinfo_['ListAgentEmail'] = row['ListAgentEmail']
                ReturnAgents.append(agentinfo_)
                UserNotExists = False
                break
        if UserNotExists:
            no_info_data = {}
            no_info_data['AgentName'] = row['ListAgentFullName']
            no_info_data['ListAgentPreferredPhone'] = row['ListAgentPreferredPhone']
            no_info_data['ListAgentEmail'] = row['ListAgentEmail']
            ReturnAgents.append(no_info_data)
    db_client.close()
    return(ReturnAgents)
