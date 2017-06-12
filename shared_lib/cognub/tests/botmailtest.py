'''
Created on Nov 24, 2016

@author: joseph
'''
from cognub.unittest import TestSuitBase


class BotMailTestSuit(TestSuitBase):
    from cognub.tests.botmail import BotMailUnitTest
    testcases = [BotMailUnitTest]
    title = "BotMail Test Report"
    description = "BotMail test results"
    resultfile = "./testreports/botmailtests.html"
