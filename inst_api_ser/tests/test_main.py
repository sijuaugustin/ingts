'''
Created on Dec 23, 2016

@author: joseph
'''
from settings import TEST_HOST, TEST_API_KEY
from heatmap.test import HeatMapAPIUnitTest
from rfm.test import RFMAPIUnitTest
from cognub.unittest import TestSuitBase
import sys

tests = [HeatMapAPIUnitTest, RFMAPIUnitTest]
for test in tests:
    test.HOST = TEST_HOST
    test.API_KEY = TEST_API_KEY


class RFMTestSuit(TestSuitBase):
    testcases = tests
    title = "Insights API's unittest"
    description = "Insights API's test results"
    resultfile = '../reports/testreport.html' if len(sys.argv) == 1 else sys.argv[1]

if __name__ == '__main__':
    RFMTestSuit.runsuit()
