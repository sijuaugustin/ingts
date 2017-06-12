'''
Created on Dec 12, 2016

@author: joseph
'''
from scipy.spatial import distance
import scipy.stats


class DistanceCalculator():

    @staticmethod
    def eucledian(vector_a, vector_b):
        return distance.euclidean(vector_a, vector_b)

    @staticmethod
    def batch_eucledian(subject, records):
        return [DistanceCalculator.eucledian(subject, record)
                for record in records]


class Ranker():

    @staticmethod
    def rank_pd(dataframe, source_col, target_col='rank'):
        dataframe[target_col] = scipy.stats.rankdata(dataframe[source_col])
        return dataframe

    @staticmethod
    def percentile_rank(dataframe, source_col='rank', target_col='percentile'):
        norm_perentiles = (len(dataframe.index) -
                           dataframe[source_col]) / (len(dataframe.index) - 1)
        dataframe[target_col] = norm_perentiles * 100
        return dataframe
