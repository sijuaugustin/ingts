'''
Created on Apr 26, 2016

@author: joseph
'''

import SocketServer
import json
from pyspark.mllib.tree import RandomForest
import hashlib
from pyspark import SparkContext
# from pyspark import SQLContext
from pymongo import MongoClient
from pyspark.mllib.classification import LabeledPoint
from pyspark.mllib.clustering import KMeans
from numpy import array
import os
from datetime import datetime
import copy
import zlib


class InsufficientData(Exception):
    pass

sc = SparkContext()


def unix_time_millis(dt):
    epoch = datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0


class Preprocessor:

    def preprocess(self):
        pass

    def clean_and_label_dataset(self):
        pass


class DatabaseManager:

    def connect(self):
        raise NotImplementedError()

    def fetch(self):
        raise NotImplementedError()


class IEstimatePreprocessor(Preprocessor):

    def clean_and_label_dataset(self, target_splits, mongo_dbmanager, database, collection, feature_keys, batch_id, now, target_key):
        dataset = []
        split_dataset = [[] for _ in range(len(target_splits))]
        split_kmeans_dataset = [[] for _ in range(len(target_splits))]
        for index, split in enumerate(target_splits):
            query = [{"StandardStatus": "Sold", 'CloseDate': {'$lt': now}, 'StateOrProvince': batch_id, target_key: {"$gte": split[0], "$lte": split[1]}}, dict([(key, True) for key in feature_keys] + [(target_key, True)])]
            data_subset = mongo_dbmanager.fetch(database, collection, query)  # (self.dependency_key, True)
            records_limit = 10000
            record_counter = 0
            for record in data_subset:
                record["CloseDate"] = unix_time_millis(datetime.strptime(record["CloseDate"], "%Y-%m-%d"))
                try:
                    classifier_label = index
                    for key in feature_keys:
                        if record[key] is not None and str(record[key]).replace('.', '', 1).replace('-', '').replace('e+', '').isdigit():
                            continue
                        else:
                            print record[key], key
                            break
                    else:
                        record['classifier_label'] = classifier_label
                        dataset.append(record)
                        split_dataset[classifier_label].append(record)
                        split_kmeans_dataset[classifier_label].append(record)
                        record_counter += 1
                except:
                    import traceback
                    traceback.print_exc()
                if record_counter == records_limit:
                    break
        return dataset, split_dataset, split_kmeans_dataset


class MongoDBManager(DatabaseManager):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def connect(self):
        self.dbclient = MongoClient(self.ip, self.port)

    def fetch(self, database, collection, query, limit=None):
        stream = self.dbclient[database][collection].find(*query)
        if limit:
            return stream.limit(limit)
        else:
            return stream

    def aggregate(self, database, collection, agr_pipeline):
        return self.dbclient[database][collection].aggregate(agr_pipeline)

    def add_record(self, database, collection, record):
        self.dbclient[database][collection].insert(record)


class BuildEngine():

    def __init__(self, model_version, batch_id, now, target_key, total_splits, rfc_config, rfr_config, hdfs_root, raw_config):
        self.model_version = model_version
        self.batch_id = batch_id
        self.build_config = raw_config
        self.now = now
        self.target_key = target_key
        self.rfc_config = rfc_config
        self.rfr_config = rfr_config
        self.total_splits = total_splits
        self.hdfs_root = hdfs_root
        self.model_build_info = {'version': self.model_version,
                                 'start_time': datetime.now(),
                                 'StateOrProvince': self.batch_id,
                                 'build_config': self.build_config}
        self.classifier_info = {}
        self.regressor_info = []

    def get_property_type_code(self, property_type):
        property_type_code = hashlib.md5(property_type).hexdigest()
        return property_type_code

    def update_build_info(self, property_type, build_info):
        self.model_build_info[property_type] = build_info

    def fetch_target_list(self, mongo_dbmanager, database, collection, target_filter):
        records = mongo_dbmanager.fetch(database, collection, [{'StandardStatus': 'Sold', 'CloseDate': {'$lt': self.now}, 'StateOrProvince': self.batch_id, self.target_key: target_filter}, {self.target_key: True}], 1000)
        target_list = []
        for record in records:
            target_list.append(record[self.target_key])
        target_list.sort()
        return target_list

    def get_target_splits(self, target_list):
        record_quantity = len(target_list)
        print "record_quantity", record_quantity
        l3medians = [(target_list[int(record_quantity * split[0])], target_list[int(record_quantity * split[1]) - 1]) for split in [(0, 0.5), (0.5, 0.75), (0.75, 1)]]
        split_distribution = [int(self.total_splits * .5), int(self.total_splits * .25), int(self.total_splits * .25)]
        target_splits = [(median_config[0][0] + ((median_config[0][1] - median_config[0][0])) * (float(split) / float(median_config[1])), median_config[0][0] + ((median_config[0][1] - median_config[0][0])) * (float(split + 1) / float(median_config[1]))) for median_config in zip(l3medians, split_distribution) for split in range(median_config[1])]
        return target_splits

    def build_regressors(self, split_dataset, split_kmeans_dataset, feature_keys):
        mce_tuples = []
        for dataset, kmeans_dataset in zip(split_dataset, split_kmeans_dataset):
            kmeans_train_set = []
            for item in kmeans_dataset:
                features = [item[column] for column in feature_keys]
                kmeans_train_set.append(array(features))
            print "kmeans_train_set", len(kmeans_train_set)
            del kmeans_dataset
            kmeans_train_set = sc.parallelize(kmeans_train_set)
            clusters = KMeans.train(kmeans_train_set, 100, maxIterations=200,
                                    runs=10, initializationMode="random")
            del kmeans_train_set
            data = []
            for item in dataset:
                features = []
                for column in feature_keys:
                    features.append(item[column])
                data.append(LabeledPoint(item[self.target_key], features))
            del dataset
            data = sc.parallelize(data)

            def preprocess(observation):
                observation.label = float(observation.label / 10000)
                return observation
            data = data.map(preprocess)
            (trainingData, testData) = data.randomSplit([0.7, 0.3])
            # del data
            model = RandomForest.trainRegressor(trainingData, categoricalFeaturesInfo={},
                                                numTrees=self.rfr_config['num_trees'], featureSubsetStrategy=self.rfr_config['feature_subset_strategy'],  # "all",
                                                impurity='variance', maxDepth=self.rfr_config['max_depth'])
            predictions = model.predict(testData.map(lambda x: x.features))
            labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
            testMSE = -1
            try:
                testMSE = labelsAndPredictions.map(lambda (v, p): (v - p) * (v - p)).sum() /\
                    float(testData.count())
            except:
                pass
            mce_tuples.append((model, clusters, testMSE))
        return mce_tuples

    def build_classifier(self, dataset, kmeans_dataset, feature_keys):
        print "kmeans_dataset", len(kmeans_dataset)
        kmeans_train_set = []
        for item in kmeans_dataset:
            features = [item[column] for column in feature_keys]
            kmeans_train_set.append(array(features))
        print "kmeans_train_set", len(kmeans_train_set)
        kmeans_train_set = sc.parallelize(kmeans_train_set)
        clusters = KMeans.train(kmeans_train_set, 100, maxIterations=500,
                                runs=10, initializationMode="random")
        del kmeans_dataset
        del kmeans_train_set
        data = []
        for item in dataset:
            features = [item[column] for column in feature_keys]
            data.append(LabeledPoint(int(item['classifier_label']), features))
        del dataset
        data = sc.parallelize(data)
        (trainingData, testData) = data.randomSplit([0.7, 0.3])
        del data
        model = RandomForest.trainClassifier(trainingData, numClasses=self.total_splits, categoricalFeaturesInfo={},
                                             numTrees=self.rfc_config['num_trees'], featureSubsetStrategy=self.rfr_config['feature_subset_strategy'],  # "all",
                                             impurity='gini', maxDepth=self.rfc_config['max_depth'], maxBins=32)
        predictions = model.predict(testData.map(lambda x: x.features))
        labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
        testErr = labelsAndPredictions.filter(lambda (v, p): v != p).count() / float(testData.count())
        return model, clusters, testErr

    def update_classifier_info(self, test_error, property_type, property_type_code):
        if property_type not in self.model_build_info:
            self.model_build_info[property_type] = {'classifier_info': {'test_error': test_error,
                                                                        'models': {'kmean': os.path.join(self.hdfs_root, 'mlslite_%s_%s_v%s' % (self.batch_id, "kmc", str(self.model_version)) + property_type_code),
                                                                                   'rfc': os.path.join(self.hdfs_root, 'mlslite_%s_%s_v%s' % (self.batch_id, "rfc", str(self.model_version)) + property_type_code),
                                                                                   }
                                                                        }
                                                    }
        else:
            self.model_build_info[property_type]['classifier_info'] = {'test_error': test_error,
                                                                       'models': {'kmean': os.path.join(self.hdfs_root, 'mlslite_%s_%s_v%s' % (self.batch_id, "kmc", str(self.model_version)) + property_type_code),
                                                                                  'rfc': os.path.join(self.hdfs_root, 'mlslite_%s_%s_v%s' % (self.batch_id, "rfc", str(self.model_version)) + property_type_code),
                                                                                  }
                                                                       }

    def update_regressor_info(self, regressor_id, test_error, split, property_type, property_type_code):
        self.model_build_info[property_type]
        if property_type not in self.model_build_info:
            self.model_build_info[property_type] = {'regressor_info': {'%s' % str(regressor_id): {'test_error_mse_dv10k': test_error,
                                                                                                  'split': [split[0], split[1]],
                                                                                                  'models': {'kmean': os.path.join(self.hdfs_root, 'mlslite_%s_%s_%d_v%s' % (self.batch_id, "kmr", regressor_id, str(self.model_version)) + property_type_code),
                                                                                                             'rfr': os.path.join(self.hdfs_root, 'mlslite_%s_%s_%d_v%s' % (self.batch_id, "rfr", regressor_id, str(self.model_version)) + property_type_code)
                                                                                                             }
                                                                                                  }
                                                                       }
                                                    }
        elif 'regressor_info' not in self.model_build_info[property_type]:
            self.model_build_info[property_type]['regressor_info'] = {'%s' % str(regressor_id): {'test_error_mse_dv10k': test_error,
                                                                                                 'split': [split[0], split[1]],
                                                                                                 'models': {'kmean': os.path.join(self.hdfs_root, 'mlslite_%s_%s_%d_v%s' % (self.batch_id, "kmr", regressor_id, str(self.model_version)) + property_type_code),
                                                                                                            'rfr': os.path.join(self.hdfs_root, 'mlslite_%s_%s_%d_v%s' % (self.batch_id, "rfr", regressor_id, str(self.model_version)) + property_type_code)
                                                                                                            }
                                                                                                 }
                                                                      }
        else:
            self.model_build_info[property_type]['regressor_info']['%s' % str(regressor_id)] = {'test_error_mse_dv10k': test_error,
                                                                                                'split': [split[0], split[1]],
                                                                                                'models': {'kmean': os.path.join(self.hdfs_root, 'mlslite_%s_%s_%d_v%s' % (self.batch_id, "kmr", regressor_id, str(self.model_version)) + property_type_code),
                                                                                                           'rfr': os.path.join(self.hdfs_root, 'mlslite_%s_%s_%d_v%s' % (self.batch_id, "rfr", regressor_id, str(self.model_version)) + property_type_code)
                                                                                                           }
                                                                                                }

    def save_build_info(self, mongo_dbmanager, database, collection):
        mongo_dbmanager.add_record(database, collection, self.model_build_info)

    def save_model(self, model, model_type, property_type_code, model_id=None):
        if model_id:
            model.save(sc, os.path.join(self.hdfs_root, 'mlslite_%s_%s_%d_v%s' % (self.batch_id, model_type, model_id, str(self.model_version)) + property_type_code))
        else:
            model.save(sc, os.path.join(self.hdfs_root, 'mlslite_%s_%s_v%s' % (self.batch_id, model_type, str(self.model_version)) + property_type_code))


class ModelBuilderV2:
    def __init__(self, config, infodb_config):
        self.property_types = config['property_types']
        self.features = config['features']
        self.batch_id = config['batch_id']
        self.hdfs_root = config['hdfs_root']
        self.model_version = config['model_version']
        self.total_splits = config['splits']
        self.dbconfig = config['dbconfig']
        self.target_key = config['target']
        self.target_filter = json.loads(config['target_filter'])
        self.now = config['now']
        self.rfc_config = config['rf_config']['rfc_config']
        self.rfr_config = config['rf_config']['rfr_config']
        self.mongo_dbmanager = MongoDBManager(self.dbconfig['ip'], self.dbconfig['port'])
        self.build_engine = BuildEngine(self.model_version, self.batch_id,
                                        self.now, self.target_key, self.total_splits,
                                        self.rfc_config, self.rfr_config, self.hdfs_root, config)
        self.preprocessor = IEstimatePreprocessor()
        self.infodb_config = infodb_config

    def build(self):
        self.mongo_dbmanager.connect()
        for property_type in self.property_types:
            property_type_code = self.build_engine.get_property_type_code(property_type)
            target_list = self.build_engine.fetch_target_list(self.mongo_dbmanager, self.dbconfig['database'], self.dbconfig['collection'], self.target_filter)
            target_splits = self.build_engine.get_target_splits(list(target_list))
            dataset, split_dataset, split_kmeans_dataset = self.preprocessor.clean_and_label_dataset(target_splits, self.mongo_dbmanager, self.dbconfig['database'], self.dbconfig['collection'], self.features[property_type], self.batch_id, self.now, self.target_key)
            classifier_model, classifier_cluster, classifier_test_error = self.build_engine.build_classifier(dataset, dataset, self.features[property_type])
            regressor_mce_tuples = self.build_engine.build_regressors(split_dataset, split_kmeans_dataset, self.features[property_type])

            self.build_engine.save_model(classifier_model, "rfc", property_type_code)
            self.build_engine.save_model(classifier_cluster, "kmc", property_type_code)
            self.build_engine.update_classifier_info(classifier_test_error, property_type, property_type_code)

            for index, mce_tuple in enumerate(regressor_mce_tuples):
                model, clusters, error = mce_tuple
                self.build_engine.save_model(model, "rfr", property_type_code, index)
                self.build_engine.save_model(clusters, "kmr", property_type_code, index)
                self.build_engine.update_regressor_info(index, error, target_splits[index], property_type, property_type_code)
        self.build_engine.save_build_info(self.mongo_dbmanager, self.infodb_config['database'], self.infodb_config['collection'])

    def get_property_type_filter(self):
        raise NotImplementedError()


class iBuildManager(SocketServer.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        data = self.request[0].strip()
        sock = self.request[1]
        try:
            jdata = json.loads(data)
        except:
            jdata = json.loads(zlib.decompress(data))
        if jdata['type'] == 'multi_build':
            print "multi_build [started]"
            sock.sendto(json.dumps({"type": "ACK", "ack": jdata['type'], "data": {"build_message": "multi build [started]"}}),
                        self.client_address)
            for batch_id in jdata['config']['batch_ids']:
                config = copy.deepcopy(jdata['config'])
                config['batch_id'] = batch_id
                model_builder = ModelBuilderV2(config=config, infodb_config=jdata['config']['buildinfodb'])
                model_builder.build()
            print "multi_build [finished]"
        elif jdata['type'] == 'exec':
            exec jdata['script']


class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9992
    server = ThreadedUDPServer((HOST, PORT), iBuildManager)
    server.serve_forever()
