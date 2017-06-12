'''
Created on Oct 26, 2016

@author: joseph
'''
import unittest


class PriceTrendUnitTest(unittest.TestCase):

    def test_00_GetZipStatus(self):
        from cognub.propmixapi import PriceTrendAPI
        self.assertGreater(len(PriceTrendAPI().get_zipstatus()), 0)

    def test_01_GetPriceTrend(self):
        from cognub.propmixapi import PriceTrendAPI
        self.assertEqual("week_52_low" in PriceTrendAPI().get_trend("33156"), True)
