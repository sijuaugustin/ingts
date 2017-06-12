# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 17:44:16 2017

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


class PricingData():
    @staticmethod
    def price(StateOrProvince_):
        def monthdelta(date, delta):
            m, y = (date.month + delta) % 12, date.year + ((date.month) + delta - 1) // 12
            if not m:
                m = 12
            d = min(date.day, [31, 29 if y % 4 == 0 and not y % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])
            return date.replace(day=d, month=m, year=y)
        pipeline = [{"$match": {'StateOrProvince': {"$ne": None},
                                'StateOrProvince': {"$ne": ""},
                                'ListOfficeName':'TheMLSonline.com',
                                'CloseDate': {'$gte': monthdelta(now, -12).strftime('%Y-%m-%d')},
                                'ClosePrice': {"$ne": 0},
                                'StandardStatus' : "Sold",
                                'ClosePrice': {"$ne": None},
                                'ClosePrice': {"$ne": ""},
                                'ListPrice': {"$ne": ""},
                                'ListPrice': {"$ne": None},
                                'ListPrice': {"$ne": 0},
                                'PostalCode': {"$ne": ""},
                                'PostalCode': {"$ne": None},
                                'PropertySubType': {"$ne": None},
                                'PropertySubType': {"$ne": ""}}},
                    {"$project":
                     {"ListPrice": 1,
                      "CloseDate": 1,
                      "StateOrProvince": 1,
                      "City": 1,
                      "PostalCode": 1,
                      "ClosePrice": 1,
                      "StandardStatus": 1,
                      "PropertySubType": 1}}]
        Data_ = list(db_client.MLSLite.mlslite_unique.aggregate(pipeline))
        df = pd.DataFrame(Data_)
        
        def cleanup(df):
            df = df[df.PropertySubType.notnull()]
            df = df[df.PropertySubType != ""]
            df = df[df.ClosePrice != 0]
            df = df[df.ListPrice != 0]
            df = df[df.PostalCode != ""]
            df = df[df.PostalCode.notnull()]
            df = df.dropna()
            return df
        
        df = cleanup(df)
        unique_properties = df['PropertySubType'].unique()
        unique_zip = df['PostalCode'].unique()
        spans = [1, 2, 3, 6, 12]
        
        stats = {}
        def get_stats(sub_df1,sub_df2,sub_df3,sub_df4,sub_df5,sub_df6,sub_df7,sub_df8,sub_df9,sub_df10,sub_df11,sub_df_1,sub_df_2,sub_df_3,sub_df_4,sub_df_5,sub_df_6,sub_df_7,sub_df_8,sub_df_9,sub_df_10,sub_df_11):
            record = {}
            rec = {}
            rec_ = {}
            record_count1 = sub_df1.shape[0]
            record_count2 = sub_df2.shape[0]
            record_count3 = sub_df3.shape[0]
            record_count4 = sub_df4.shape[0]
            record_count5 = sub_df5.shape[0]
            record_count6 = sub_df6.shape[0]
            record_count7 = sub_df7.shape[0]
            record_count8 = sub_df8.shape[0]
            record_count9 = sub_df9.shape[0]
            record_count10 = sub_df10.shape[0]
            record_count11 = sub_df11.shape[0]
            record_count_1 = sub_df_1.shape[0]
            record_count_2 = sub_df_2.shape[0]
            record_count_3 = sub_df_3.shape[0]
            record_count_4 = sub_df_4.shape[0]
            record_count_5 = sub_df_5.shape[0]
            record_count_6 = sub_df_6.shape[0]
            record_count_7 = sub_df_7.shape[0]
            record_count_8 = sub_df_8.shape[0]
            record_count_9 = sub_df_9.shape[0]
            record_count_10 = sub_df_10.shape[0]
            record_count_11 = sub_df_11.shape[0]
            rec['0-100000'] = record_count1
            rec['100000-200000'] = record_count2
            rec['200000-300000'] = record_count3
            rec['300000-400000'] = record_count4
            rec['400000-500000'] = record_count5
            rec['500000-600000'] = record_count6
            rec['600000-700000'] = record_count7
            rec['700000-800000'] = record_count8
            rec['800000-900000'] = record_count9
            rec['900000-1000000'] = record_count10
            rec['1000000+'] = record_count11
            rec_['0-100000'] = record_count_1
            rec_['100000-200000'] = record_count_2
            rec_['200000-300000'] = record_count_3
            rec_['300000-400000'] = record_count_4
            rec_['400000-500000'] = record_count_5
            rec_['500000-600000'] = record_count_6
            rec_['600000-700000'] = record_count_7
            rec_['700000-800000'] = record_count_8
            rec_['800000-900000'] = record_count_9
            rec_['900000-1000000'] = record_count_10
            rec_['1000000+'] = record_count_11
            record['ClosePrice'] = rec
            record['ListPrice'] = rec_
            record['Span'] = 'last %d Month' % (monthback)
            return record
        
        stats['All'] = {}   
        for zip in unique_zip:
            stats[zip] = {}
            stats[zip]['All'] = {}
            for property_type in unique_properties:
                stats[zip][property_type] = {}
                for monthback in spans:
                    record = stats[zip][property_type]['last %d Month' % monthback] = {}
                    sub_df1 = df[(df['PostalCode'] == zip) & (df['ClosePrice'] > 0) & (df['ClosePrice'] <= 100000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                    sub_df2 = df[(df['PostalCode'] == zip) & (df['ClosePrice'] > 100000) & (df['ClosePrice'] <= 200000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]                
                    sub_df3 = df[(df['PostalCode'] == zip) & (df['ClosePrice'] > 200000) & (df['ClosePrice'] <= 300000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                    sub_df4 = df[(df['PostalCode'] == zip) & (df['ClosePrice'] > 300000) & (df['ClosePrice'] <= 400000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                    sub_df5 = df[(df['PostalCode'] == zip) & (df['ClosePrice'] > 400000) & (df['ClosePrice'] <= 500000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]  
                    sub_df6 = df[(df['PostalCode'] == zip) & (df['ClosePrice'] > 500000) & (df['ClosePrice'] <= 600000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                    sub_df7 = df[(df['PostalCode'] == zip) & (df['ClosePrice'] > 600000) & (df['ClosePrice'] <= 700000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                    sub_df8 = df[(df['PostalCode'] == zip) & (df['ClosePrice'] > 700000) & (df['ClosePrice'] <= 800000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                    sub_df9 = df[(df['PostalCode'] == zip) & (df['ClosePrice'] > 800000) & (df['ClosePrice'] <= 900000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                    sub_df10 = df[(df['PostalCode'] == zip) & (df['ClosePrice'] > 900000) & (df['ClosePrice'] <= 1000000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                    sub_df11 = df[(df['PostalCode'] == zip) & (df['ClosePrice'] > 1000000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                    sub_df_1 = df[(df['PostalCode'] == zip) & (df['ListPrice'] > 0) & (df['ListPrice'] <= 100000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                    sub_df_2 = df[(df['PostalCode'] == zip) & (df['ListPrice'] > 100000) & (df['ListPrice'] <= 200000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]                
                    sub_df_3 = df[(df['PostalCode'] == zip) & (df['ListPrice'] > 200000) & (df['ListPrice'] <= 300000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                    sub_df_4 = df[(df['PostalCode'] == zip) & (df['ListPrice'] > 300000) & (df['ListPrice'] <= 400000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                    sub_df_5 = df[(df['PostalCode'] == zip) & (df['ListPrice'] > 400000) & (df['ListPrice'] <= 500000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                    sub_df_6 = df[(df['PostalCode'] == zip) & (df['ListPrice'] > 500000) & (df['ListPrice'] <= 600000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                    sub_df_7 = df[(df['PostalCode'] == zip) & (df['ListPrice'] > 600000) & (df['ListPrice'] <= 700000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                    sub_df_8 = df[(df['PostalCode'] == zip) & (df['ListPrice'] > 700000) & (df['ListPrice'] <= 800000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                    sub_df_9 = df[(df['PostalCode'] == zip) & (df['ListPrice'] > 800000) & (df['ListPrice'] <= 900000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                    sub_df_10 = df[(df['PostalCode'] == zip) & (df['ListPrice'] > 900000) & (df['ListPrice'] <= 1000000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                    sub_df_11 = df[(df['PostalCode'] == zip) & (df['ListPrice'] > 1000000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                    record.update(get_stats(sub_df1,sub_df2,sub_df3,sub_df4,sub_df5,sub_df6,sub_df7,sub_df8,sub_df9,sub_df10,sub_df11,sub_df_1,sub_df_2,sub_df_3,sub_df_4,sub_df_5,sub_df_6,sub_df_7,sub_df_8,sub_df_9,sub_df_10,sub_df_11))
                    
            for monthback in spans:
                property_type = "All"
                record = stats[zip][property_type]['last %d Month' % monthback] = {}
                sub_df1 = df[(df['PostalCode'] == zip) & (df['ClosePrice'] > 0) & (df['ClosePrice'] <= 100000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df2 = df[(df['PostalCode'] == zip) & (df['ClosePrice'] > 100000) & (df['ClosePrice'] <= 200000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df3 = df[(df['PostalCode'] == zip) & (df['ClosePrice'] > 200000) & (df['ClosePrice'] <= 300000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df4 = df[(df['PostalCode'] == zip) & (df['ClosePrice'] > 300000) & (df['ClosePrice'] <= 400000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df5 = df[(df['PostalCode'] == zip) & (df['ClosePrice'] > 400000) & (df['ClosePrice'] <= 500000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df6 = df[(df['PostalCode'] == zip) & (df['ClosePrice'] > 500000) & (df['ClosePrice'] <= 600000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df7 = df[(df['PostalCode'] == zip) & (df['ClosePrice'] > 600000) & (df['ClosePrice'] <= 700000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df8 = df[(df['PostalCode'] == zip) & (df['ClosePrice'] > 700000) & (df['ClosePrice'] <= 800000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df9 = df[(df['PostalCode'] == zip) & (df['ClosePrice'] > 800000) & (df['ClosePrice'] <= 900000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df10 = df[(df['PostalCode'] == zip) & (df['ClosePrice'] > 900000) & (df['ClosePrice'] <= 1000000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df11 = df[(df['PostalCode'] == zip) & (df['ClosePrice'] > 1000000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_1 = df[(df['PostalCode'] == zip) & (df['ListPrice'] > 0) & (df['ListPrice'] <= 100000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_2 = df[(df['PostalCode'] == zip) & (df['ListPrice'] > 100000) & (df['ListPrice'] <= 200000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_3 = df[(df['PostalCode'] == zip) & (df['ListPrice'] > 200000) & (df['ListPrice'] <= 300000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_4 = df[(df['PostalCode'] == zip) & (df['ListPrice'] > 300000) & (df['ListPrice'] <= 400000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_5 = df[(df['PostalCode'] == zip) & (df['ListPrice'] > 400000) & (df['ListPrice'] <= 500000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_6 = df[(df['PostalCode'] == zip) & (df['ListPrice'] > 500000) & (df['ListPrice'] <= 600000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_7 = df[(df['PostalCode'] == zip) & (df['ListPrice'] > 600000) & (df['ListPrice'] <= 700000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_8 = df[(df['PostalCode'] == zip) & (df['ListPrice'] > 700000) & (df['ListPrice'] <= 800000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_9 = df[(df['PostalCode'] == zip) & (df['ListPrice'] > 800000) & (df['ListPrice'] <= 900000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_10 = df[(df['PostalCode'] == zip) & (df['ListPrice'] > 900000) & (df['ListPrice'] <= 1000000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_11 = df[(df['PostalCode'] == zip) & (df['ListPrice'] > 1000000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                record.update(get_stats(sub_df1,sub_df2,sub_df3,sub_df4,sub_df5,sub_df6,sub_df7,sub_df8,sub_df9,sub_df10,sub_df11,sub_df_1,sub_df_2,sub_df_3,sub_df_4,sub_df_5,sub_df_6,sub_df_7,sub_df_8,sub_df_9,sub_df_10,sub_df_11))
        
        zip = 'All'
        stats['All']['All'] = {}
        for property_type in unique_properties:
            stats['All'][property_type] = {}
            for monthback in spans:
                record = stats['All'][property_type]['last %d Month' % monthback] = {}
                sub_df1 = df[(df['ClosePrice'] > 0) & (df['ClosePrice'] <= 100000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df2 = df[(df['ClosePrice'] > 100000) & (df['ClosePrice'] <= 200000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df3 = df[(df['ClosePrice'] > 200000) & (df['ClosePrice'] <= 300000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df4 = df[(df['ClosePrice'] > 300000) & (df['ClosePrice'] <= 400000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df5 = df[(df['ClosePrice'] > 400000) & (df['ClosePrice'] <= 500000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df6 = df[(df['ClosePrice'] > 500000) & (df['ClosePrice'] <= 600000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df7 = df[(df['ClosePrice'] > 600000) & (df['ClosePrice'] <= 700000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df8 = df[(df['ClosePrice'] > 700000) & (df['ClosePrice'] <= 800000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df9 = df[(df['ClosePrice'] > 800000) & (df['ClosePrice'] <= 900000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df10 = df[(df['ClosePrice'] > 900000) & (df['ClosePrice'] <= 1000000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df11 = df[(df['ClosePrice'] > 1000000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_1 = df[(df['ListPrice'] > 0) & (df['ListPrice'] <= 100000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_2 = df[(df['ListPrice'] > 100000) & (df['ListPrice'] <= 200000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_3 = df[(df['ListPrice'] > 200000) & (df['ListPrice'] <= 300000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_4 = df[(df['ListPrice'] > 300000) & (df['ListPrice'] <= 400000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_5 = df[(df['ListPrice'] > 400000) & (df['ListPrice'] <= 500000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_6 = df[(df['ListPrice'] > 500000) & (df['ListPrice'] <= 600000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_7 = df[(df['ListPrice'] > 600000) & (df['ListPrice'] <= 700000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_8 = df[(df['ListPrice'] > 700000) & (df['ListPrice'] <= 800000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_9 = df[(df['ListPrice'] > 800000) & (df['ListPrice'] <= 900000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_10 = df[(df['ListPrice'] > 900000) & (df['ListPrice'] <= 1000000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_11 = df[(df['ListPrice'] > 1000000) & (df['PropertySubType'] == property_type) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                record.update(get_stats(sub_df1,sub_df2,sub_df3,sub_df4,sub_df5,sub_df6,sub_df7,sub_df8,sub_df9,sub_df10,sub_df11,sub_df_1,sub_df_2,sub_df_3,sub_df_4,sub_df_5,sub_df_6,sub_df_7,sub_df_8,sub_df_9,sub_df_10,sub_df_11))
        
                
            for monthback in spans:
                property_type = "All"
                record = stats['All'][property_type]['last %d Month' % monthback] = {}
                sub_df1 = df[(df['ClosePrice'] > 0) & (df['ClosePrice'] <= 100000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df2 = df[(df['ClosePrice'] > 100000) & (df['ClosePrice'] <= 200000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df3 = df[(df['ClosePrice'] > 200000) & (df['ClosePrice'] <= 300000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df4 = df[(df['ClosePrice'] > 300000) & (df['ClosePrice'] <= 400000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df5 = df[(df['ClosePrice'] > 400000) & (df['ClosePrice'] <= 500000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df6 = df[(df['ClosePrice'] > 500000) & (df['ClosePrice'] <= 600000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df7 = df[(df['ClosePrice'] > 600000) & (df['ClosePrice'] <= 700000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df8 = df[(df['ClosePrice'] > 700000) & (df['ClosePrice'] <= 800000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df9 = df[(df['ClosePrice'] > 800000) & (df['ClosePrice'] <= 900000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df10 = df[(df['ClosePrice'] > 900000) & (df['ClosePrice'] <= 1000000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df11 = df[(df['ClosePrice'] > 1000000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_1 = df[(df['ListPrice'] > 0) & (df['ListPrice'] <= 100000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_2 = df[(df['ListPrice'] > 100000) & (df['ListPrice'] <= 200000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_3 = df[(df['ListPrice'] > 200000) & (df['ListPrice'] <= 300000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_4 = df[(df['ListPrice'] > 300000) & (df['ListPrice'] <= 400000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_5 = df[(df['ListPrice'] > 400000) & (df['ListPrice'] <= 500000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_6 = df[(df['ListPrice'] > 500000) & (df['ListPrice'] <= 600000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_7 = df[(df['ListPrice'] > 600000) & (df['ListPrice'] <= 700000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_8 = df[(df['ListPrice'] > 700000) & (df['ListPrice'] <= 800000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_9 = df[(df['ListPrice'] > 800000) & (df['ListPrice'] <= 900000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_10 = df[(df['ListPrice'] > 900000) & (df['ListPrice'] <= 1000000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                sub_df_11 = df[(df['ListPrice'] > 1000000) & (df['CloseDate'] >= monthdelta(now, -monthback).strftime(date_format))]
                record.update(get_stats(sub_df1,sub_df2,sub_df3,sub_df4,sub_df5,sub_df6,sub_df7,sub_df8,sub_df9,sub_df10,sub_df11,sub_df_1,sub_df_2,sub_df_3,sub_df_4,sub_df_5,sub_df_6,sub_df_7,sub_df_8,sub_df_9,sub_df_10,sub_df_11))
        
        for key, value in stats.items():
            new_stats = {'_id': {'ListOfficeName': ListOfficeName, 'PostalCode': key}, 'performance_index': value, "StateOrProvince": StateOrProvince_}
            db_client.pricing.brokeragepricingstats.update({'_id': {'ListOfficeName': ListOfficeName, 'PostalCode': key}, 'performance_index': value}, new_stats, upsert=True, multi=False)

class SampleDistributer(ConfigDistributerSim):
    def distribution_algorithm(self):
        StateOrProvince_ = list(db_client.MLSLite.mlslite_unique.distinct("StateOrProvince"))
        n = int(math.ceil(float(len(StateOrProvince_)) / float(self.get_jobscount())))
        return [StateOrProvince_[i:i + n] for i in xrange(0, len(StateOrProvince_), n)]


class SampleJob(DistributedJobSim):
    zkroot = '/cognubapps/propmix/price_scheduler'
    zkhost = 'hdp-master.propmix.io:2181'
    distributer = SampleDistributer

    def __jobinit__(self, name):
        self.name = name

    def run(self, StateOrProvince_):
        PricingData.price(StateOrProvince_)

job = SampleJob("SampleJob")
job.start()
