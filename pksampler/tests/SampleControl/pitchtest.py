""" pitchtest.py """

from qt import *
from SampleControl import SampleControl
from pitchtestform import pitchtestform
import PKAudio
import random

FILEPATH = "/home/ajole/wav/Document 1.wav"
NUM_SAMPLES = 2

class PitchTest(pitchtestform):

    def __init__(self,parent = None,name = None,fl = 0):
        pitchtestform.__init__(self,parent,name,fl)
        
        self.sliders = {}
        self.samples = {}
        mixer = PKAudio.Driver().getMixer()
        
        for i in range(NUM_SAMPLES):
            slider = getattr(self, 'slider'+str(i+1))
            #self.samples[slider] = SampleControl()
            #self.samples[slider].load(FILEPATH)
            #self.samples[slider].slotLooping(True)
            #self.samples[slider].slotStart()
            #self.samples[slider].slotVolume(50)
            #self.samples[slider].slotSetZone(0, True)
            self.samples[slider] = PKAudio.Sample(FILEPATH)
            volume = PKAudio.Volume()
            volume.setVolume(100)
            self.samples[slider].outputPort().connect(volume.inputPort())
            mixer.connect(volume.outputPort())
            self.samples[slider].play()
            self.samples[slider].setLooping(True)
        QObject.connect(slider, SIGNAL('valueChanged(int)'),
                        self.slotSlider)
        self.sliders = list(self.samples)
                        
        # the timer
        random.seed()
        self.timer = QTimer(self)
        QObject.connect(self.timer, SIGNAL('timeout()'),
                        self.slotTimer)
        self.timer.start(100)
            
    def slotSlider(self, v):
        slider = self.sender()
        #self.samples[slider].slotPitch(v * 1.0)
        self.samples[slider].setPitch(v * 1.0)
        
    def slotTimer(self):
        i = random.randint(0, NUM_SAMPLES-1)
        slider = self.sliders[i]
        r = random.random()
        slider.setValue(r * 127)
        
def run():
    a = QApplication([])
    PKAudio.start_server()
    w = PitchTest()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
    
if __name__ == '__main__':
    run()
