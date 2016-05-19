""" Sample.py: A Sample widget. """

import os.path
from qt import *
import PKAudio
from sampleform import SampleForm
from Globals import DisplayTimer


displayTimer = DisplayTimer()


class Wrapper(QObject):
    """ QObject wrapper around PKAudio.Sample. """
    
    def __init__(self):
        QObject.__init__(self)
        self.sample = None
        self.volume = PKAudio.Volume('vol')
        self.d = PKAudio.Driver()
        
    def load(self, path):
        if self.sample:
            self.sample.outputPort().disconnect()
            self.sample = None
        self.sample = PKAudio.Sample(path)
        self.sample.outputPort().connect(self.volume.inputPort())
        self.d.getMixer(0).connect(self.volume.outputPort())
        
    def unload(self):
        self.sample.outputPort().disconnect()
        self.sample = None
        
    def play(self):
        if self.sample:
            self.sample.play()
            self.emit(PYSIGNAL('playing'), () )
    
    def stop(self):
        if self.sample:
            self.sample.stop()
            
    def cue(self):
        if self.sample:
            self.sample.stop()
            self.sample.reset()
            
    def atEnd(self):
        if self.sample:
            return self.sample.atEnd()
        else:
            return True
    
    def looping(self):
        if self.sample:
            return self.sample.getLooping()
        else:
            return False
    
    def setLooping(self, a0):
        if self.sample:
            self.sample.setLooping(a0)
    
    def setVolume(self, v):
        self.volume.setVolume(v)
        
    def pos(self):
        if self.sample:
            return self.sample.pos()
        else:
            return 0
            
    def setPos(self, p):
        if self.sample:
            self.sample.pos(p)
            
    def reset(self):
        if self.sample:
            self.sample.reset()
            
    def length(self):
        if self.sample:
            return self.sample.length()
        else:
            return 0


class Sample(SampleForm):
    """ Sample Widget 
        SIGNALS:
            PYSIGNAL('delete'), (self,)
    """

    def __init__(self, parent=None, name=''):
        SampleForm.__init__(self, parent, name)
        self.setFrameStyle(QFrame.Raised)
        self.wrapper = Wrapper()
        displayTimer.register(self)

    def unload(self):
        self.wrapper.stop()
        self.wrapper.unload()
        displayTimer.deregister(self)

    def load(self, path):
        self.wrapper.load(path)
        self.volumeSlider.setValue(100)
        self.titleLabel.setText(os.path.basename(path))
    
    def updateDisplay(self):
        if self.wrapper.atEnd() and not self.wrapper.looping():
            self.wrapper.stop()
            self.wrapper.reset()
        frames = int(self.wrapper.pos())
        self.textLabel.setText(str(frames / 1000))
    
    def reparent(self, parent, point, showit=False):
        if parent:
            c = parent.paletteBackgroundColor()
            self.setPaletteBackgroundColor(c.dark(110))
        SampleForm.reparent(self, parent, 0, point, showit)
    
    ## User controls
    
    def slotPlay(self):
        self.wrapper.play()
    
    def slotCue(self):
        self.wrapper.cue()
    
    def slotVolume(self, v):
        self.wrapper.setVolume(127 - v)
        
    def slotDelete(self):
        self.wrapper.unload()
        self.emit(PYSIGNAL('delete'), (self,))
        
    def slotLooping(self, a0):
        self.wrapper.setLooping(a0)
    
    
def main():
    a = QApplication([])
    PKAudio.start_server()
    w = Sample()
    w.load('/home/ajole/wav/track.wav')
    a.setMainWidget(w)
    w.show()
    a.exec_loop()


if __name__ == "__main__":
    main()
    
    
