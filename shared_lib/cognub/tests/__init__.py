from cognub.unittest import TestSuitBase
import unittest
from cognub.logging import BaseLoggerFactory


class SampleLogger(BaseLoggerFactory):
        logpath = "./sample.log"
        logger_names = ["Main"]
        level = BaseLoggerFactory.DEBUG


class SampleModule():

    def __init__(self, batch_id, logger):
        self.logger = logger
        self.logger.info("Initializing Module")
        self.batch_id = batch_id

    def collect_data(self):
        self.logger.info("Collecting records from database of batch %s sample %s, %s", self.batch_id, "1", "2")
        return "Collected Records"

    def preprocess_data(self, data):
        self.logger.info("Preprocessing records of batch %s", self.batch_id)
        return "Preprocessed Records"

    def build_model(self, preprocessed_records):
        self.logger.info("Building model for batch %s", self.batch_id)
        return "Model", "Build Info"

    def save_model(self, model):
        self.logger.info("Saving model for batch %s", self.batch_id)

    def save_build_info(self, build_info):
        self.logger.info("Saving model build info for batch %s", self.batch_id)


class ModelBuilder():

    def __init__(self, batch_id, logger):
        self.logger = logger
        self.module = SampleModule(batch_id, logger)

    def build(self):
        self.logger.info("Buil Started")
        data = self.module.collect_data()
        preprocessed_data = self.module.preprocess_data(data)
        model, build_info = self.module.build_model(preprocessed_data)
        self.module.save_model(model)
        self.module.save_build_info(build_info)
        self.logger.info("Buil Finished")


class SampleTest(unittest.TestCase):

    def test_01_initialize_module(self):
        '''Initializing Sample Module'''
        logger = SampleLogger().get_logger("Main")
        self.__class__.module = SampleModule("10", logger)

    def test_02_collecting_data(self):
        '''Collecting records from MongoDb'''
        self.__class__.records = self.__class__.module.collect_data()
        self.assertEqual(self.__class__.records, "Collected Records")

    def test_03_preprocess_data(self):
        '''Preprocessing Records'''
        self.__class__.preprocessed_data = self.__class__.module.preprocess_data(self.__class__.records)

    def test_04_build_model(self):
        '''Building model from records'''
        self.__class__.model, self.__class__.build_info = self.__class__.module.build_model(self.__class__.preprocessed_data)

    def test_05_save_model(self):
        '''Saving model build'''
        self.__class__.module.save_model(self.__class__.model)

    def test_06_save_build_info(self):
        '''Saving Build Information'''
        self.__class__.module.save_build_info(self.__class__.build_info)


class SampleTestSuit(TestSuitBase):
    testcases = [SampleTest]
    title = "Sample Test"
    description = "Model build prototype and a Unittest sample"
    resultfile = "./reports/sample/testreport.htm"

if __name__ == '__main__':
    logger = SampleLogger().get_logger("Main")
    builder = ModelBuilder("Batch 01", logger)
    builder.build()
