'''
Created on Dec 16, 2016

@author: vishnu.sk
'''

import unittest
from cognub.unittest import TestSuitBase


class HeatMapAPIUnitTest(unittest.TestCase):
    HOST = None
    API_KEY = None

    def test_00_init(self):
        from lib import HeatMapAPI
        self.__class__.heatmap = HeatMapAPI(host=self.__class__.HOST, api_key=self.__class__.API_KEY)

    def test_01_state_county_data(self):
        params = {'listings': 'Closed_Listings', 'span': '5Y', 'attribute': 'ClosePrice'}
        result = self.__class__.heatmap.state_county_data(**params)
        self.assertGreater(len(result), 0)
        self.assertEqual("CountyData" in self.__class__.heatmap.state_county_data('Closed_Listings', '5Y', 'ClosePrice'), True)

    def test_02_zip_data(self):
        params = {'listings': 'Active_Listings', 'radius': '5', 'latitude': '42.355812', 'longitude': '-71.073302', 'span': '5Y', 'attribute': 'ListPrice'}
        result = self.__class__.heatmap.zip_data(**params)
        print result
        self.assertGreater(len(result), 0)
        self.assertIn('FeatureCollection', result['type'], msg=None)


class HeatMapTestSuit(TestSuitBase):
    testcases = [HeatMapAPIUnitTest]
    title = "HeatMap API unittest"
    description = "HeatMap API test results."

if __name__ == '__main__':
    HeatMapTestSuit.runsuit()
