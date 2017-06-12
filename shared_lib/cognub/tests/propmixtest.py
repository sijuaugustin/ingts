'''
Created on Oct 28, 2016

@author: joseph
'''
from cognub.unittest import TestSuitBase


class PropmixAPIFullTest(TestSuitBase):
    from cognub.tests.ipricetrend import PriceTrendUnitTest
    testcases = [PriceTrendUnitTest]
    title = "Propmix API Tests"
    description = "Propmix API Full Test Results"


class IEstimateModelBuildTest(TestSuitBase):
    from cognub.tests.iestimate import iEstimateUnitTest
    testcases = [iEstimateUnitTest]
    title = "iEstimate Build Test"
    description = "iEstimate Build Test Results"
