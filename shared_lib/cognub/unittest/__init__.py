import unittest
import StringIO
import HTMLTestRunner
import os


class TestSuitBase(unittest.TestCase):
    testcases = []
    title = 'Basic Test'  # '<Propmix API Test>'
    description = 'Basic Test Results'  # 'Propmix API Test Results.'
    resultfile = './testreports.html'

    def test0(self):
        self.suite = unittest.TestSuite()
        buf = StringIO.StringIO()
        runner = HTMLTestRunner.HTMLTestRunner(buf)
        runner.run(self.suite)
        self.assert_('</html>' in buf.getvalue())

    def test_main(self):
        self.suite = unittest.TestSuite()
        self.suite.addTests([unittest.defaultTestLoader.loadTestsFromTestCase(test_case) for test_case in self.testcases])
        buf = StringIO.StringIO()
        runner = HTMLTestRunner.HTMLTestRunner(stream=buf,
                                               title=self.title,
                                               description=self.description
                                               )
        runner.run(self.suite)
        byte_output = buf.getvalue()
        resultdir = os.path.dirname(self.__class__.resultfile)
        if not os.path.exists(resultdir):
            os.makedirs(resultdir)
        reportfile = open(self.__class__.resultfile, "w")
        reportfile.write(byte_output)
        reportfile.close()

    @classmethod
    def runsuit(cls):
        suite = unittest.TestLoader().loadTestsFromTestCase(cls)
        unittest.TextTestRunner().run(suite)


def demo():
    class SampleOutputTestBase(unittest.TestCase):
        """ Base TestCase. Generates 4 test cases x different content type. """
        MESSAGE = 'basic test'

        def test_1(self):
            print self.MESSAGE

        def test_2(self):
            import sys
            self.assertEqual(sys.stderr, self.MESSAGE)

        def test_3(self):
            self.fail(self.MESSAGE)

        def test_4(self):
            raise RuntimeError(self.MESSAGE)

    class SampleTestSuit(TestSuitBase):
        testcases = [SampleOutputTestBase]
        title = '<Sample Test>'
        description = 'Sample Test Results.'

    SampleTestSuit.runsuit()


if __name__ == "__main__":
    demo()
