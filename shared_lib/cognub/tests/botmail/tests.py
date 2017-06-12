'''
Created on Nov 24, 2016

@author: joseph
'''
from unittest import TestCase


class BotMailUnitTest(TestCase):

    def test_01_InitializeBotMail(self):
        from cognub.botmail import BotMail
        self.__class__.botmail = BotMail()

    def test_02_SendMail(self):
        from cognub.botmail.recipients import test_recepients
        self.__class__.botmail.send_mail("BotMail unittest", "Hello this is an auto generated email from BotMail unittest.", to=test_recepients)

    def test_03_SendSecondMail(self):
        from cognub.botmail.recipients import test_recepients
        self.__class__.botmail.send_mail("BotMail unittest second mail", "Hello this is an auto generated second email from BotMail unittest.", to=test_recepients)
