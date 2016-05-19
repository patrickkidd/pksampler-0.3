""" PK utils test suite. """

import unittest
from pkutils import execCmd, checkForPKAudio, checkForQt


class TestCaseBase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestUtils(TestCaseBase):
    
    def test_execCmd(self):
        status, out = execCmd('echo "uh huh"')
        self.assertEqual(out, 'uh huh')

        status, out = execCmd('this_command_cannnnt_possibly_exits')
        self.assertEqual(True, 'command not found' in out)

    def test_checkForQt(self):
        self.assertEqual(True, checkForQt())

    def test_checkForPKAudio(self):
        self.assertEqual(True, checkForPKAudio(['0.3']))
        
    ## INSERT MORE TESTS AS YOU ENCOUNTER PROBLEMS...

        
if __name__ == '__main__':
    print """
*** This is the test suite for the 'pk install utils'. ***

"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestUtils))
    unittest.TextTestRunner(verbosity=2).run(suite)
