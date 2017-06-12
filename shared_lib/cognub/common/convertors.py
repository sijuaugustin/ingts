'''
Created on Dec 12, 2016

@author: joseph
'''
import pandas as pd


class BaseConvertor():

    @staticmethod
    def convert_to_pd(data, features, fltr=None):
        result_list = []
        for list_item in data:
            feature_vector = []
            for column in features:
                feature_vector.append(list_item[column])
            result_list.append(feature_vector)
        data_frame = pd.DataFrame(data=result_list, columns=features)
        if fltr is not None:
            return data_frame[data_frame[fltr[0]] == fltr[1]]
        return data_frame

    @staticmethod
    def to_float(val):
        try:
            return float(val)
        except:
            return None

    @staticmethod
    def to_json(dataframe):
        return dataframe.to_json(path_or_buf=None, orient='records',
                                 date_format='epoch', double_precision=10,
                                 force_ascii=True, date_unit='ms', default_handler=None)
