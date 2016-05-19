
import unittest
import pkaudio
from PKAudio import *

START_SERVER = 1

class ServerTest(unittest.TestCase):

    def setUp(self):
        pkaudio.connect(startserver=START_SERVER)
        
    def tearDown(self):
        pkaudio.disconnect()


class TestWrappers(ServerTest):
    
    def test_module(self):
        s1 = Sample('/home/ajole/wav/track.wav')
        self.assertEqual(s1.numInputs(), 0)
        self.assertEqual(s1.numOutputs(), 1)
        d = Driver()
        m = d.getMixer(0)
        m.connect(s1.outputPort())
        
        info = pkaudio.getModuleInfo(m.id())
        self.assertEqual(len(info['ins']), 1)
        
        s2 = Sample('/home/ajole/wav/track.wav')
        m.connect(s2.outputPort())
        info = pkaudio.getModuleInfo(m.id())
        self.assertEqual(len(info['ins']), 2)
        
        s1.outputPort().disconnect()
        info = pkaudio.getModuleInfo(m.id())
        self.assertEqual(len(info['ins']), 1)
        self.assertEqual(m.numInputs(), 1)
        
        s2.outputPort().disconnect()
        info = pkaudio.getModuleInfo(m.id())
        self.assertEqual(len(info['ins']), 0)
        self.assertEqual(m.numInputs(), 0)
        
        
class TestSampleControl(ServerTest):

    def test_samplecontrol(self):
        from SampleControl import SampleControl
        l = []
        for i in range(10):
            l.append(SampleControl())
        print 'done'


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestWrappers))
    suite.addTest(unittest.makeSuite(TestSampleControl))
    unittest.TextTestRunner(verbosity=2).run(suite)
