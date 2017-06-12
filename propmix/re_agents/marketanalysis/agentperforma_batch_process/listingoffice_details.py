# -*- coding: utf-8 -*-
"""
Created on Wed Jan 04 15:32:28 2017

@author: vishnu.sk
"""

from cognub.jobmanager import ConfigDistributerSim, DistributedJobSim
from pymongo import MongoClient
import math
from dbauth import DATABASE_ACCESS
db_client = MongoClient("mongo-master.propmix.io", port=33017)
db_client.MLSLite.authenticate(**DATABASE_ACCESS)
db_client.listingoffices.authenticate(**DATABASE_ACCESS)


class ListOfficeData():
    @staticmethod
    def listings(StateOrProvince_):
        pipeline = [{"$match": {'StateOrProvince': {"$ne": None},
                        'StateOrProvince': {"$ne": ""},
                        'ClosePrice': {"$ne": 0},
                        'ListPrice': {"$ne": 0},
                        'ListOfficeName': {"$ne": None},
                        'ListAgentFullName': {"$ne": None},
                        'ListAgentFullName': {"$ne": ""},
                        'ListOfficeName': {"$ne": ""}}},
                    {"$group": {"_id": {'State': "$StateOrProvince",
                                'ListOfficeName': "$ListOfficeName"},
                                'ListingAgents': {"$addToSet": "$ListAgentFullName"},
                                "NumberOfTransactions": {"$sum": 1}}},
                    {"$project": {"_id": 1, "ListingAgents": 1,
                                  "NumberOfTransactions": 1,
                                  "NumberOfAgents": {"$size": "$ListingAgents"}}}]

        Data = list(db_client.MLSLite.mlslite_unique.aggregate(pipeline, allowDiskUse=True))
        for record in Data:
            new_Data = {"_id": record["_id"], "ListingAgents": record["ListingAgents"], "NumberOfAgents": record["NumberOfAgents"], "NumberOfTransactions": record["NumberOfTransactions"], "StateOrProvince": StateOrProvince_}
            db_client.listingoffices.listingofficestats.update({"_id": record["_id"], "ListingAgents": record["ListingAgents"], "NumberOfAgents": record["NumberOfAgents"], "NumberOfTransactions": record["NumberOfTransactions"]}, new_Data, upsert=True, multi=False)


class SampleDistributer(ConfigDistributerSim):
    def distribution_algorithm(self):
        StateOrProvince_ = list(db_client.MLSLite.mlslite_unique.distinct("StateOrProvince"))
        n = int(math.ceil(float(len(StateOrProvince_)) / float(self.get_jobscount())))
        return [StateOrProvince_[i:i + n] for i in xrange(0, len(StateOrProvince_), n)]


class SampleJob(DistributedJobSim):
    zkroot = '/cognubapps/propmix/listingoffice_scheduler'
    zkhost = 'hdp-master.propmix.io:2181'
    distributer = SampleDistributer

    def __jobinit__(self, name):
        self.name = name

    def run(self, StateOrProvince_):
        ListOfficeData.listings(StateOrProvince_)

job = SampleJob("SampleJob")
job.start()
