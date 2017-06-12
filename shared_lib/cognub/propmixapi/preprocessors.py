'''
Created on May 12, 2016

@author: joseph
'''
import numpy as np
import traceback
import datetime


class InvalidFeatureValue(Exception):
    pass


def dsto_labeled_points(dataset, feature_keys):
    from pyspark.mllib.classification import LabeledPoint
    data = []
    for item in dataset:
        features = []
        for column in feature_keys:
            try:
                if item[column] is not None and str(item[column]).replace('.', '', 1).replace('-', '').isdigit():
                    features.append(float(item[column]))
                else:
                    raise InvalidFeatureValue()
            except:
                break
        else:
            data.append(LabeledPoint(float(item['ClosePrice']) / float(item['LivingArea']), features))
    return data

# ["item['CloseDate'] = (datetime.datetime.strptime(item['CloseDate'], '%Y-%m-%d') - datetime.datetime(1970,1,1)).total_seconds()",
#                                                                        "item['CloseDate'] = (datetime.datetime.strptime(item['ModificationTimestamp'].split(' ')[0], '%Y-%m-%d') - datetime.datetime(1970,1,1)).total_seconds()"]
# "float(item['ClosePrice'])/float(item['LivingArea'])"


def mongo_dsto_nparray(input_dataset, feature_keys, preprocess_script=None, target_script=None):
    targets_list = []
    features_list = []
    for item in input_dataset:
        features = []
        if preprocess_script is not None:
            for script in preprocess_script:
                try:
                    exec script
                except:
                    continue
                break
        for column in feature_keys:
            try:
                if item[column] is not None and str(item[column]).replace('.', '', 1).strip('-').replace('e+', '').isdigit():
                    features.append(float(item[column]))
                else:
                    raise InvalidFeatureValue()
            except:
                break
        else:
            target = None
            if target_script is not None:
                try:
                    exec "target = %s" % (target_script)
                    targets_list.append(target)
                except:
                    continue
            features_list.append(features)
    return np.asarray(features_list, dtype="double"), np.asarray(targets_list, dtype="double")


def mongo_dsto_norm_nparray(input_dataset, feature_keys, preprocess_script="item['CloseDate'] = (datetime.datetime.strptime(item['CloseDate'], '%Y-%m-%d') - datetime.datetime(1970,1,1)).total_seconds()"):
    from cognub.propmixapi.normalizers import NPNormalizer
    targets_list = []
    features_list = []
    for item in input_dataset:
        features = []
        exec preprocess_script
        for column in feature_keys:
            try:
                if item[column] is not None and str(item[column]).replace('.', '', 1).strip('-').isdigit():
                    features.append(float(item[column]))
                else:
                    raise InvalidFeatureValue()
            except:
                break
        else:
            targets_list.append(float(item['ClosePrice']) / float(item['LivingArea']))
            features_list.append(features)
    return NPNormalizer().fit(features_list).transform(features_list), np.asarray(targets_list, dtype="double")


def dict_to_nparray(input_data, feature_keys, preprocess_script="input_data['CloseDate'] = (datetime.datetime.strptime(input_data['CloseDate'],'%Y-%m-%d') - datetime.datetime(1970,1,1)).total_seconds()"):
    features = []
    exec preprocess_script
    for column in feature_keys:
        try:
            if input_data[column] is not None and str(input_data[column]).replace('.', '', 1).strip('-').isdigit():
                features.append(float(input_data[column]))
            else:
                raise InvalidFeatureValue()
        except:
            break
    else:
        return np.asarray(features, dtype='double')


def dsto_norm_labeled_points(input_dataset, feature_keys, preprocess_script="item['CloseDate'] = (datetime.datetime.strptime(item['CloseDate'], '%Y-%m-%d') - datetime.datetime(1970,1,1)).total_seconds()"):
    from pyspark.mllib.classification import LabeledPoint
    from cognub.propmixapi.normalizers import NPNormalizer
    datamap = {'targets': [], 'features': []}
    for item in input_dataset:
        features = []
        exec preprocess_script
        for column in feature_keys:
            try:
                if item[column] is not None and str(item[column]).replace('.', '', 1).strip('-').isdigit():
                    features.append(float(item[column]))
                else:
                    raise InvalidFeatureValue()
            except:
                break
        else:
            datamap['targets'].append(float(item['ClosePrice']) / float(item['LivingArea']))
            datamap['features'].append(features)

    datamap['features'] = NPNormalizer().fit(datamap['features']).transform(datamap['features'])
    dataset = []
    for index, target in enumerate(datamap['targets']):
        dataset.append(LabeledPoint(target, datamap['features'][index]))
    return dataset
