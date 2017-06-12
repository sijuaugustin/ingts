'''
Created on Nov 16, 2016

@author: joseph
'''
import unittest
import json


class iEstimateUnitTest(unittest.TestCase):
    from cognub.propmixapi.datasets.featuresconf import features_mlslite

    conf_record = {"batch_id": "FL",
                   "splits": 6,
                   "now": "2016-04-01",
                   "property_types": ["All"],
                   "model_version": "0.9.1.MLSLite.03.T",
                   "remarks": "None",
                   "rf_config": {"rfc_config": {"num_trees": 10,
                                                "feature_subset_strategy": "all",
                                                "max_depth": 10
                                                },
                                 "rfr_config": {"num_trees": 10,
                                                "feature_subset_strategy": "all",
                                                "max_depth": 10
                                                },
                                 },
                   "dbconfig": {"ip": "52.91.122.15",
                                "port": 33017,
                                "database": "MLSLite",
                                "collection": "listing_unique",
                                },
                   "buildinfodb": {"ip": "52.91.122.15",
                                   "port": 33017,
                                   "database": "infodb",
                                   "collection": "iestimate_buildinfo",
                                   },
                   "hdfs_root": "hdfs://hdp-master.propmix.io:8020/models/iestimate/mlslite",
                   "features": {"All": features_mlslite},
                   "target": "ClosePrice",
                   "target_filter": json.dumps({"$gt": 10000,
                                                "$lt": 7000000}),
                   "dependency": "ClosePrice",
                   }

    def test_00_Initialize(self):
        from cognub.projects.iestimate import BuildEngine, IEstimatePreprocessor, MongoDBManager, IEstimateLoggerFactory 
        config = self.__class__.conf_record
        self.__class__.property_types = config['property_types']
        self.__class__.features = config['features']
        self.__class__.batch_id = config['batch_id']
        self.__class__.hdfs_root = config['hdfs_root']
        self.__class__.model_version = config['model_version']
        self.__class__.total_splits = config['splits']
        self.__class__.dbconfig = config['dbconfig']
        self.__class__.target_key = config['target']
        self.__class__.target_filter = json.loads(config['target_filter'])
        self.__class__.now = config['now']
        self.__class__.rfc_config = config['rf_config']['rfc_config']
        self.__class__.rfr_config = config['rf_config']['rfr_config']
        logger_factory = IEstimateLoggerFactory()
        self.__class__.mongo_dbmanager = MongoDBManager(self.dbconfig['ip'], self.dbconfig['port'], logger_factory.get_logger("Database"))
        self.__class__.build_engine = BuildEngine(self.__class__.model_version, self.__class__.batch_id,
                                                  self.__class__.now, self.__class__.target_key, self.__class__.total_splits,
                                                  self.__class__.rfc_config, self.__class__.rfr_config, self.__class__.hdfs_root, config, logger_factory.get_logger("BuildEngine"))
        self.__class__.preprocessor = IEstimatePreprocessor(logger_factory.get_logger("Preprocessor"))
        self.__class__.infodb_config = config['buildinfodb']

    def test_01_ConnectDatabase(self):
        self.__class__.mongo_dbmanager.connect()

    def test_02_GetPropertyTypeCode(self):
        self.__class__.property_type = self.__class__.property_types[0]
        self.__class__.property_type_code = self.__class__.build_engine.get_property_type_code(self.__class__.property_type)

    def test_03_FetchTargetList(self):
        self.__class__.target_list = self.__class__.build_engine.fetch_target_list(self.__class__.mongo_dbmanager, self.__class__.dbconfig['database'], self.__class__.dbconfig['collection'], self.__class__.target_filter)

    def test_04_GetTargetSplits(self):
        self.__class__.target_splits = self.__class__.build_engine.get_target_splits(list(self.__class__.target_list))

    def test_05_CleanAndLabelDataset(self):
        self.__class__.dataset, self.__class__.split_dataset, self.__class__.split_kmeans_dataset = self.__class__.preprocessor.clean_and_label_dataset(self.__class__.target_splits, self.__class__.mongo_dbmanager, self.__class__.dbconfig['database'], self.__class__.dbconfig['collection'], self.__class__.features[self.__class__.property_type], self.__class__.batch_id, self.__class__.now, self.__class__.target_key)

    def test_06_BuildClassifier(self):
        self.__class__.classifier_model, self.__class__.classifier_cluster, self.__class__.classifier_test_error = self.__class__.build_engine.build_classifier(self.__class__.dataset, self.__class__.dataset, self.__class__.features[self.__class__.property_type])

    def test_07_BuildRegressors(self):
        self.__class__.regressor_mce_tuples = self.build_engine.build_regressors(self.__class__.split_dataset, self.__class__.split_kmeans_dataset, self.__class__.features[self.__class__.property_type])

    def test_08_SaveClassifierModel(self):
        self.__class__.build_engine.save_model(self.__class__.classifier_model, "rfc", self.__class__.property_type_code)

    def test_09_SaveL1Kmean(self):
        self.__class__.build_engine.save_model(self.__class__.classifier_cluster, "kmc", self.__class__.property_type_code)

    def test_10_UpdateClassifierInfo(self):
        self.__class__.build_engine.update_classifier_info(self.__class__.classifier_test_error, self.__class__.property_type, self.__class__.property_type_code)

    def test_10_SaveRegressors(self):
        for index, mce_tuple in enumerate(self.__class__.regressor_mce_tuples):
            model, _, _ = mce_tuple
            self.__class__.build_engine.save_model(model, "rfr", self.__class__.property_type_code, index)

    def test_11_SaveL2Kmeans(self):
        for index, mce_tuple in enumerate(self.__class__.regressor_mce_tuples):
            _, clusters, _ = mce_tuple
            self.__class__.build_engine.save_model(clusters, "kmr", self.__class__.property_type_code, index)

    def test_12_UpdateRegressorInfo(self):
        for index, mce_tuple in enumerate(self.__class__.regressor_mce_tuples):
            _, _, error = mce_tuple
            self.__class__.build_engine.update_regressor_info(index, error, self.__class__.target_splits[index], self.__class__.property_type, self.__class__.property_type_code)

    def test_13_SaveBuildInfo(self):
        self.__class__.build_engine.save_build_info(self.__class__.mongo_dbmanager, self.__class__.infodb_config['database'], self.__class__.infodb_config['collection'])
