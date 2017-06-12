# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 20:25:29 2017

@author: vishnu.sk

"""

from cognub.jobmanager import ConfigDistributerSim, DistributedJobSim
import pandas as pd
from pymongo import MongoClient
import math
import datetime
from dbauth import DATABASE_ACCESS

date_format = "%Y-%m-%d"
now = datetime.datetime.now()
ListOfficeName = 'TheMLSonline.com'
db_client = MongoClient("mongo-master.propmix.io", port=33017)
db_client.MLSLite.authenticate(**DATABASE_ACCESS)
db_client.listingoffices.authenticate(**DATABASE_ACCESS)


class AgentPerforma():
    @staticmethod
    def agents(StateOrProvince_):
        def monthdelta(date, delta):
            m, y = (date.month + delta) % 12, date.year + ((date.month) + delta - 1) // 12
            if not m:
                m = 12
            d = min(date.day, [31, 29 if y % 4 == 0 and not y % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])
            return date.replace(day=d, month=m, year=y)

        pipeline = [{"$match": {'StateOrProvince': {"$ne": None},
                        'StateOrProvince': {"$ne": ""},
                        'ListOfficeName' : ListOfficeName,
                        'CloseDate': {'$gte': monthdelta(now, -24).strftime('%Y-%m-%d')},
                        'ClosePrice': {"$ne": 0},
                        'ClosePrice': {"$ne": ""},
                        'ListPrice': {"$ne": ""},
                        'lsratio': {"$ne": 0},
                        'lsratio': {"$ne": ""},
                        'ListPrice': {"$ne": 0},
                        'PropertySubType': {"$ne": 0},
                        'PropertySubType': {"$ne": ""},
                        'ListAgentFullName': {"$ne": None},
                        'ListAgentFullName': {"$ne": ""}}},
                    {"$project" :
                     {"ListPrice": 1,
                      "CloseDate": 1,
                      "StateOrProvince": 1,
                      "City": 1,
                      "lsratio": 1,
                      "PostalCode": 1,
                      "ClosePrice": 1,
                      "StandardStatus": 1,
                      "PropertySubType": 1,
                      "ListOfficeName": 1,
                      "ListAgentFullName": 1}}]
        Data_ = list(db_client.MLSLite.mlslite_unique.aggregate(pipeline))
        df = pd.DataFrame(Data_)

        def cleanup(df):
            df = df[df.PropertySubType.notnull()]
            df = df[df.PropertySubType != ""]
            df = df[df.StandardStatus != "Cancel/Withdrawn"]
            df = df[df.StandardStatus != "Contingent"]
            df = df[df.StandardStatus != "Pending"]
            df = df[df.StandardStatus != "Unknown"]
            df = df[df.lsratio <= 10]
            df = df.dropna()
            return df
        
        df = cleanup(df)
        unique_agents = df['ListAgentFullName'].unique()
        unique_properties = df['PropertySubType'].unique()
        unique_states = df['StateOrProvince'].unique()
        spans = [1, 3, 6, 12, 18]
        
        stats = {}
        
        def get_stats(sub_df_Sold,sub_df_Active):
            record = {}
            record["Total_ClosePrice_Sold"] = sub_df_Sold['ClosePrice'].sum()
            record['Total_ListPrice_Sold'] = sub_df_Sold['ListPrice'].sum()
            record['Total_ListPrice_Active'] = sub_df_Active['ListPrice'].sum()
            Total_lsratio_Sold = sub_df_Sold["lsratio"].sum()
            record_count_Sold = sub_df_Sold.shape[0]
            record_count_Active= sub_df_Active.shape[0]
            record['Avg_Sold_to_List_percent_Sold'] = 100 * ((float(record_count_Sold) / float(Total_lsratio_Sold))) if Total_lsratio_Sold != 0 else 0
            record['Number_of_Transactions_Sold'] = record_count_Sold 
            record['Number_of_Transactions_Active'] = record_count_Active 
            record['Span'] = '%dM' % (monthback)
            return record
        
        stats['All'] = {}
        for states in unique_states:
            stats[states] = {}
            
            for agent in unique_agents:
                stats[states][agent] = {}
                stats[states][agent]['All'] = {}
                for property_type in unique_properties:
                    stats[states][agent][property_type] = {}
                    for monthback in spans:
                        record = stats[states][agent][property_type]['%dM' % monthback] = {}
                        sub_df_Sold = df[(df['ListAgentFullName'] == agent) & (df['StandardStatus'] == 'Sold') & (df['StateOrProvince'] == states) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                        sub_df_Active = df[(df['ListAgentFullName'] == agent) & (df['StandardStatus'] == 'Active') & (df['StateOrProvince'] == states) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                        record.update(get_stats(sub_df_Sold, sub_df_Active))
        
                for monthback in spans:
                    property_type = "All"
                    record = stats[states][agent][property_type]['%dM' % monthback] = {}
                    sub_df_Sold = df[(df['ListAgentFullName'] == agent) & (df['StandardStatus'] == 'Sold') & (df['StateOrProvince'] == states) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                    sub_df_Active = df[(df['ListAgentFullName'] == agent) & (df['StandardStatus'] == 'Active') & (df['StateOrProvince'] == states) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]            
                    record.update(get_stats(sub_df_Sold, sub_df_Active))
        for agent in unique_agents:
            states = "All"
            stats['All'][agent] = {}
            stats['All'][agent]['All'] = {}
            for property_type in unique_properties:
                stats['All'][agent][property_type] = {}
                for monthback in spans:
                    record = stats['All'][agent][property_type]['%dM' % monthback] = {}
                    sub_df_Sold = df[(df['ListAgentFullName'] == agent) & (df['StandardStatus'] == 'Sold') & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format)) ]
                    sub_df_Active = df[(df['ListAgentFullName'] == agent) & (df['StandardStatus'] == 'Active') & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                    record.update(get_stats(sub_df_Sold, sub_df_Active))
        
            for monthback in spans:
                property_type = "All"
                record = stats['All'][agent][property_type]['%dM' % monthback] = {}
                sub_df_Sold = df[(df['ListAgentFullName'] == agent) & (df['StandardStatus'] == 'Sold') & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format)) ]
                sub_df_Active = df[(df['ListAgentFullName'] == agent) & (df['StandardStatus'] == 'Active') & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                record.update(get_stats(sub_df_Sold, sub_df_Active))
        for key, value in stats.items():
            new_stats = {'_id': {'ListOfficeName': ListOfficeName, 'State': key}, 'performance_index': value, "StateOrProvince": StateOrProvince_}
            db_client.listingoffices.agentperformance.update({'_id': {'ListOfficeName': ListOfficeName, 'State': key}, 'performance_index': value}, new_stats, upsert=True, multi=False)


class SampleDistributer(ConfigDistributerSim):
    def distribution_algorithm(self):
        StateOrProvince_ = list(db_client.MLSLite.mlslite_unique.distinct("StateOrProvince"))
        n = int(math.ceil(float(len(StateOrProvince_)) / float(self.get_jobscount())))
        return [StateOrProvince_[i:i + n] for i in xrange(0, len(StateOrProvince_), n)]


class SampleJob(DistributedJobSim):
    zkroot = '/cognubapps/propmix/agent_scheduler'
    zkhost = 'hdp-master.propmix.io:2181'
    distributer = SampleDistributer

    def __jobinit__(self, name):
        self.name = name

    def run(self, StateOrProvince_):
        AgentPerforma.agents(StateOrProvince_)

job = SampleJob("SampleJob")
job.start()
