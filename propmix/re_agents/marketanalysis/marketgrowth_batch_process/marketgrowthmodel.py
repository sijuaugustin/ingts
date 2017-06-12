# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 15:12:49 2017

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


class GrowthData():
    @staticmethod
    def growth(StateOrProvince_):
        def monthdelta(date, delta):
            m, y = (date.month + delta) % 12, date.year + ((date.month) + delta - 1) // 12
            if not m:
                m = 12
            d = min(date.day, [31, 29 if y % 4 == 0 and not y % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])
            return date.replace(day=d, month=m, year=y)
        pipeline = [{"$match": {'StateOrProvince': {"$ne": None},
                                'StateOrProvince': {"$ne": ""},
                                'ListOfficeName' : ListOfficeName,
                                'StandardStatus' : "Sold",
                                'CloseDate': {'$gte': monthdelta(now, -24).strftime('%Y-%m-%d')},
                                'ClosePrice': {"$ne": 0},
                                'ClosePrice': {"$ne": ""},
                                'ListPrice': {"$ne": ""},
                                'ListPrice': {"$ne": 0},
                                'PropertySubType': {"$ne": 0},
                                'PropertySubType': {"$ne": ""},
                                'ListAgentFullName': {"$ne": None},
                                'ListAgentFullName': {"$ne": ""}}},
                    {"$project":
                     {"ListPrice": 1,
                      "CloseDate": 1 ,
                      "StateOrProvince": 1,
                      "City": 1,
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
            df = df.dropna()
            return df
        
        df = cleanup(df)
        unique_agents = df['ListAgentFullName'].unique()
        unique_properties = df['PropertySubType'].unique()
        unique_states = df['StateOrProvince'].unique()
        
        stats = {}
        def get_stats(sub_df1, sub_df2,sub_df3,sub_df4,sub_df5,sub_df6,sub_df7,sub_df8,sub_df9):
            record = {}
            rec_sold = {}
            rec_list = {}
            rec_sold["Total_Price_current_year_current_quarter"] = sub_df1['ClosePrice'].sum()
            rec_sold["Total_Price_current_year_2nd_quarter"] = sub_df2['ClosePrice'].sum()
            rec_sold["Total_Price_current_year_3rd_quarter"] = sub_df3['ClosePrice'].sum()    
            rec_sold["Total_Price_current_year_4th_quarter"] = sub_df4['ClosePrice'].sum()
            rec_sold["Total_Price_current_year_last_month"] = sub_df5['ClosePrice'].sum()
            rec_sold["Total_Price_previous_year_last_month"] = sub_df6['ClosePrice'].sum()
            rec_sold["Total_Price_previous_year_current_quarter"] = sub_df7['ClosePrice'].sum()
            rec_sold["Total_Price_current_year"] = sub_df8['ClosePrice'].sum()
            rec_sold["Total_Price_previous_year"] = sub_df9['ClosePrice'].sum()
            rec_list["Total_Price_current_year_current_quarter"] = sub_df1['ListPrice'].sum()
            rec_list["Total_Price_current_year_2nd_quarter"] = sub_df2['ListPrice'].sum()
            rec_list["Total_Price_current_year_3rd_quarter"] = sub_df3['ListPrice'].sum()
            rec_list["Total_Price_current_year_4th_quarter"] = sub_df4['ListPrice'].sum()
            rec_list["Total_Price_current_year_last_month"] = sub_df5['ListPrice'].sum()
            rec_list["Total_Price_previous_year_last_month"] = sub_df6['ListPrice'].sum()
            rec_list["Total_Price_previous_year_current_quarter"] = sub_df7['ListPrice'].sum()
            rec_list["Total_Price_current_year"] = sub_df8['ListPrice'].sum()
            rec_list["Total_Price_previous_year"] = sub_df9['ListPrice'].sum()
            record['ClosePrice'] = rec_sold
            record['ListPrice'] = rec_list
            return record
        
        stats['All'] = {}
        for states in unique_states:
            stats[states] = {}
            
            for agent in unique_agents:
                stats[states][agent] = {}
                stats[states][agent]['All'] = {}
                for property_type in unique_properties:
                    stats[states][agent][property_type] = {}
                    record = stats[states][agent][property_type] = {}
                    sub_df1 = df[(df['ListAgentFullName'] == agent) & (df['StateOrProvince'] == states) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -3).strftime(date_format))]
                    sub_df2 = df[(df['ListAgentFullName'] == agent) & (df['StateOrProvince'] == states) & (df['PropertySubType'] == property_type) & (df['CloseDate'] < monthdelta(now, -3).strftime(date_format)) & (df['CloseDate'] >= monthdelta(now, -6).strftime(date_format))]
                    sub_df3 = df[(df['ListAgentFullName'] == agent) & (df['StateOrProvince'] == states) & (df['PropertySubType'] == property_type) & (df['CloseDate'] < monthdelta(now, -6).strftime(date_format)) & (df['CloseDate'] >= monthdelta(now, -9).strftime(date_format))]
                    sub_df4 = df[(df['ListAgentFullName'] == agent) & (df['StateOrProvince'] == states) & (df['PropertySubType'] == property_type) & (df['CloseDate'] < monthdelta(now, -9).strftime(date_format)) & (df['CloseDate'] >= monthdelta(now, -12).strftime(date_format))]
                    sub_df5 = df[(df['ListAgentFullName'] == agent) & (df['StateOrProvince'] == states) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -1).strftime(date_format))]
                    sub_df6 = df[(df['ListAgentFullName'] == agent) & (df['StateOrProvince'] == states) & (df['PropertySubType'] == property_type) & (df['CloseDate'] < monthdelta(now, -12).strftime(date_format)) & (df['CloseDate'] >= monthdelta(now, -13).strftime(date_format))]
                    sub_df7 = df[(df['ListAgentFullName'] == agent) & (df['StateOrProvince'] == states) & (df['PropertySubType'] == property_type) & (df['CloseDate'] < monthdelta(now, -12).strftime(date_format)) & (df['CloseDate'] >= monthdelta(now, -15).strftime(date_format))]
                    sub_df8 = df[(df['ListAgentFullName'] == agent) & (df['StateOrProvince'] == states) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -12).strftime(date_format))]
                    sub_df9 = df[(df['ListAgentFullName'] == agent) & (df['StateOrProvince'] == states) & (df['PropertySubType'] == property_type) & (df['CloseDate'] < monthdelta(now, -12).strftime(date_format)) & (df['CloseDate'] >= monthdelta(now, -24).strftime(date_format))]
                    record.update(get_stats(sub_df1, sub_df2,sub_df3,sub_df4,sub_df5,sub_df6,sub_df7,sub_df8,sub_df9))
        
                property_type = "All"
                record = stats[states][agent][property_type]= {}
                sub_df1 = df[(df['ListAgentFullName'] == agent) & (df['StateOrProvince'] == states) & (df['CloseDate'] >= monthdelta(now, -3).strftime(date_format))]
                sub_df2 = df[(df['ListAgentFullName'] == agent) & (df['StateOrProvince'] == states) & (df['CloseDate'] < monthdelta(now, -3).strftime(date_format)) & (df['CloseDate'] >= monthdelta(now, -6).strftime(date_format))]
                sub_df3 = df[(df['ListAgentFullName'] == agent) & (df['StateOrProvince'] == states) & (df['CloseDate'] < monthdelta(now, -6).strftime(date_format)) & (df['CloseDate'] >= monthdelta(now, -9).strftime(date_format))]
                sub_df4 = df[(df['ListAgentFullName'] == agent) & (df['StateOrProvince'] == states) & (df['CloseDate'] < monthdelta(now, -9).strftime(date_format)) & (df['CloseDate'] >= monthdelta(now, -12).strftime(date_format))]
                sub_df5 = df[(df['ListAgentFullName'] == agent) & (df['StateOrProvince'] == states) & (df['CloseDate'] >= monthdelta(now, -1).strftime(date_format))]
                sub_df6 = df[(df['ListAgentFullName'] == agent) & (df['StateOrProvince'] == states) & (df['CloseDate'] < monthdelta(now, -12).strftime(date_format)) & (df['CloseDate'] >= monthdelta(now, -13).strftime(date_format))]
                sub_df7 = df[(df['ListAgentFullName'] == agent) & (df['StateOrProvince'] == states) & (df['CloseDate'] < monthdelta(now, -12).strftime(date_format)) & (df['CloseDate'] >= monthdelta(now, -15).strftime(date_format))]
                sub_df8 = df[(df['ListAgentFullName'] == agent) & (df['StateOrProvince'] == states) & (df['CloseDate'] >= monthdelta(now, -12).strftime(date_format))]
                sub_df9 = df[(df['ListAgentFullName'] == agent) & (df['StateOrProvince'] == states) & (df['CloseDate'] < monthdelta(now, -12).strftime(date_format)) & (df['CloseDate'] >= monthdelta(now, -24).strftime(date_format))]
                record.update(get_stats(sub_df1, sub_df2,sub_df3,sub_df4,sub_df5,sub_df6,sub_df7,sub_df8,sub_df9))
        for agent in unique_agents:
            states = "All"
            stats['All'][agent] = {}
            stats['All'][agent]['All'] = {}
            for property_type in unique_properties:
                stats['All'][agent][property_type] = {}
                record = stats['All'][agent][property_type] = {}
                sub_df1 = df[(df['ListAgentFullName'] == agent) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -3).strftime(date_format))]
                sub_df2 = df[(df['ListAgentFullName'] == agent) & (df['PropertySubType'] == property_type) & (df['CloseDate'] < monthdelta(now, -3).strftime(date_format)) & (df['CloseDate'] >= monthdelta(now, -6).strftime(date_format))]
                sub_df3 = df[(df['ListAgentFullName'] == agent) & (df['PropertySubType'] == property_type) & (df['CloseDate'] < monthdelta(now, -6).strftime(date_format)) & (df['CloseDate'] >= monthdelta(now, -9).strftime(date_format))]
                sub_df4 = df[(df['ListAgentFullName'] == agent) & (df['PropertySubType'] == property_type) & (df['CloseDate'] < monthdelta(now, -9).strftime(date_format)) & (df['CloseDate'] >= monthdelta(now, -12).strftime(date_format))]
                sub_df5 = df[(df['ListAgentFullName'] == agent) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -1).strftime(date_format))]
                sub_df6 = df[(df['ListAgentFullName'] == agent) & (df['PropertySubType'] == property_type) & (df['CloseDate'] < monthdelta(now, -12).strftime(date_format)) & (df['CloseDate'] >= monthdelta(now, -13).strftime(date_format))]
                sub_df7 = df[(df['ListAgentFullName'] == agent) & (df['PropertySubType'] == property_type) & (df['CloseDate'] < monthdelta(now, -12).strftime(date_format)) & (df['CloseDate'] >= monthdelta(now, -15).strftime(date_format))]
                sub_df8 = df[(df['ListAgentFullName'] == agent) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -12).strftime(date_format))]
                sub_df9 = df[(df['ListAgentFullName'] == agent) & (df['PropertySubType'] == property_type) & (df['CloseDate'] < monthdelta(now, -12).strftime(date_format)) & (df['CloseDate'] >= monthdelta(now, -24).strftime(date_format))]
                record.update(get_stats(sub_df1, sub_df2,sub_df3,sub_df4,sub_df5,sub_df6,sub_df7,sub_df8,sub_df9))
                    
            property_type = "All"
            record = stats['All'][agent][property_type] = {}
            sub_df1 = df[(df['ListAgentFullName'] == agent) & (df['CloseDate'] >= monthdelta(now, -3).strftime(date_format))]
            sub_df2 = df[(df['ListAgentFullName'] == agent) & (df['CloseDate'] < monthdelta(now, -3).strftime(date_format)) & (df['CloseDate'] >= monthdelta(now, -6).strftime(date_format))]
            sub_df3 = df[(df['ListAgentFullName'] == agent) & (df['CloseDate'] < monthdelta(now, -6).strftime(date_format)) & (df['CloseDate'] >= monthdelta(now, -9).strftime(date_format))]
            sub_df4 = df[(df['ListAgentFullName'] == agent) & (df['CloseDate'] < monthdelta(now, -9).strftime(date_format)) & (df['CloseDate'] >= monthdelta(now, -12).strftime(date_format))]
            sub_df5 = df[(df['ListAgentFullName'] == agent) & (df['CloseDate'] >= monthdelta(now, -1).strftime(date_format))]
            sub_df6 = df[(df['ListAgentFullName'] == agent) & (df['CloseDate'] < monthdelta(now, -12).strftime(date_format)) & (df['CloseDate'] >= monthdelta(now, -13).strftime(date_format))]
            sub_df7 = df[(df['ListAgentFullName'] == agent) & (df['CloseDate'] < monthdelta(now, -12).strftime(date_format)) & (df['CloseDate'] >= monthdelta(now, -15).strftime(date_format))]
            sub_df8 = df[(df['ListAgentFullName'] == agent) & (df['CloseDate'] >= monthdelta(now, -12).strftime(date_format))]
            sub_df9 = df[(df['ListAgentFullName'] == agent) & (df['CloseDate'] < monthdelta(now, -12).strftime(date_format)) & (df['CloseDate'] >= monthdelta(now, -24).strftime(date_format))]
            record.update(get_stats(sub_df1, sub_df2,sub_df3,sub_df4,sub_df5,sub_df6,sub_df7,sub_df8,sub_df9))
        for key, value in stats.items():
            new_stats = {'_id': {'ListOfficeName': ListOfficeName, 'State': key}, 'performance_index': value, "StateOrProvince": StateOrProvince_}
            db_client.marketgrowth.growthstats.update({'_id': {'ListOfficeName': ListOfficeName, 'State': key}, 'performance_index': value}, new_stats, upsert=True, multi=False)

class SampleDistributer(ConfigDistributerSim):
    def distribution_algorithm(self):
        StateOrProvince_ = list(db_client.MLSLite.mlslite_unique.distinct("StateOrProvince"))
        n = int(math.ceil(float(len(StateOrProvince_)) / float(self.get_jobscount())))
        return [StateOrProvince_[i:i + n] for i in xrange(0, len(StateOrProvince_), n)]


class SampleJob(DistributedJobSim):
    zkroot = '/cognubapps/propmix/growth_scheduler'
    zkhost = 'hdp-master.propmix.io:2181'
    distributer = SampleDistributer

    def __jobinit__(self, name):
        self.name = name

    def run(self, StateOrProvince_):
        GrowthData.growth(StateOrProvince_)

job = SampleJob("SampleJob")
job.start()
