'''
Created on Dec 9, 2016

@author: joseph
'''
from sklearn.cluster import KMeans
from .convertors import BaseConvertor
import copy


class KmeanImputer():

    def __init__(self):
        self.avgs = None
        self.km = None
        self.n_features = None

    def fit(self, clean_data, n_clusters=4):
        sums = [0 for _ in range(len(clean_data[0]))]
        n_samples = len(clean_data)
        self.n_features = len(clean_data[0])
        self.km = KMeans(n_clusters=n_clusters)
        self.km.fit(clean_data)
        for record in clean_data:
            sums = [sums[index] + record[index]
                    for index in range(self.n_features)]
        self.avgs = [float(sums[index]) / n_samples
                     for index in range(self.n_features)]

    def impute(self, record, valid_cases):
        imputed_record = copy.deepcopy(record)
        missing_indexes = []
        for index in range(self.n_features):
            if not valid_cases[index](record[index]):
                imputed_record[index] = self.avgs[index]
                missing_indexes.append(index)
        if len(missing_indexes) == 0:
            return record
        km_centroid = self.km.cluster_centers_[
            self.km.predict([imputed_record])[0]]
        for index in missing_indexes:
            imputed_record[index] = km_centroid[index]
        return imputed_record


class CleaningAlgorithm():

    @staticmethod
    def clean_string(value):
        if type(value) is str:
            return value.strp(' \'"_,')
        else:
            return value


class Cleaner():

    @staticmethod
    def kmean_impute(mixed_data, valid_cases, n_clusters=4):
        kmi = KmeanImputer()
        clean_data = [record for record in mixed_data if all([
            valid_cases[index](element)
            for index, element in enumerate(record)])]
        kmi.fit(clean_data, n_clusters)
        cleaned_records = []
        for record in mixed_data:
            cleaned_records.append(kmi.impute(record, valid_cases))
        return cleaned_records

    @staticmethod
    def clean_to_float(data):
        cleaned_records = []

        def float_translate(val):
            cleaned_val = CleaningAlgorithm.clean_string(val)
            result = BaseConvertor.to_float(cleaned_val)
            if result is None:
                return val
            else:
                return result
        for record in data:
            cleaned_records.append(map(float_translate, record))
        return cleaned_records

    @staticmethod
    def string_clean(data):
        cleaned_records = []
        for record in data:
            cleaned_records.append(map(CleaningAlgorithm.clean_string, record))
        return cleaned_records

    @staticmethod
    def index_dataframe(dataframe, index_filed='index'):
        dataframe[index_filed] = range(0, len(dataframe))
        dataframe = dataframe.set_index(index_filed)
        return dataframe

    @staticmethod
    def character_replace(dataframe, fields):
        filtered_data = dataframe.dropna(axis='columns', how='all')
        for field in fields:
            uniq_str = dataframe[field].unique()
            clean_unique = [z for z in uniq_str if str(z) != 'nan']
            for elemnt in clean_unique:
                filtered_data[elemnt] = None
                yn = filtered_data[field].str.contains(
                    elemnt, na=False).astype(int)
                filtered_data[elemnt] = yn
            filtered_data = filtered_data.drop(field, 1)
        return filtered_data
