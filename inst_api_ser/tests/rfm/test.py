'''
Created on Dec 15, 2016

@author: vishnu.sk
'''

import unittest
from cognub.unittest import TestSuitBase


class RFMAPIUnitTest(unittest.TestCase):
    HOST = None
    API_KEY = None

    def test_00_init(self):
        from lib import RFMapi
        self.__class__.rfm = RFMapi(host=self.__class__.HOST, api_key=self.__class__.API_KEY)

    def test_01_best_fit(self):
        params = {'address': '1514 Cherry Flats Rd, Miami, AZ 85539, USA',
                  'SI_PropertyType': 'Residential',
                  'Zip': 85539,
                  'radius': 2,
                  'GLA': 1200,
                  'Beds': 3,
                  'Baths': 2,
                  'LotSizeArea': 7500,
                  'YearBuilt': 1990,
                  'StoriesTotal': 1,
                  'Distance': 0,
                  'MonthsBack': 36,
                  'City': 'Miami',
                  'State': 'AZ'}
        result = self.__class__.rfm.best_fit(**params)
        self.assertGreater(len(result), 0)
        print result
        for record in result:
            self.assertIn('AgentName', record, msg=None)

    def test_02_get_details(self):
        params = {'agent': 'Read Northen', 'State': 'NC', 'zip': 28411}
        result = self.__class__.rfm.get_details(**params)
        self.assertGreater(len(result), 0)
        self.assertEqual("Agent Information" in self.__class__.rfm.get_details('Read Northen', 'NC', '28411'), True)

    def test_03_get_top10(self):
        params = {'level': 'State', 'value': 'IL'}
        result = self.__class__.rfm.get_top10(**params)
        print result
        self.assertGreater(len(result), 0)
        self.assertEqual("Top Agents" in self.__class__.rfm.get_top10('State', 'IL'), True)


class RFMTestSuit(TestSuitBase):
    from settings import TEST_API_KEY
    from settings import TEST_HOST
    RFMAPIUnitTest.HOST = TEST_HOST
    RFMAPIUnitTest.API_KEY = TEST_API_KEY
    testcases = [RFMAPIUnitTest]
    title = "RFM API unittest"
    description = "RFM API test results."

if __name__ == '__main__':
    RFMTestSuit.runsuit()
