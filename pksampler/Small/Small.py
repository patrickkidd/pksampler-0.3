""" Small.py: main module for the small project."""

import os, os.path
import Queue
from qt import *
import Sample
from Selector import Selector
from SampleGroup import SampleGroup
import Widgets
import PKAudio

SELECTOR_WIDTH = 260
SELECTOR_HEIGHT = 384
CACHED_SAMPLES = 10
NUM_SAMPLE_GROUPS = 10


def Print(*s):
    print 'Small:',
    for i in s:
        print '',i,
    print

def PrintErr(*s):
    print ' ** Small:',
    for i in s:
        print '',i,
    print

    
class TrackFrame(QFrame):
    """ Holds a track in a colorable frame.         
        SIGNALS:
            PYSIGNAL('selected'), (self,)
            PYSIGNAL('loaded'), (self,)
            PYSIGNAL('unloaded'), (self,)
            PYSIGNAL('collapsed'), (self,)
            PYSIGNAL('expanded'), (self,)
    """
    
    def __init__(self, track=None, margin=5, parent=None, name=None, f=0):
        """ Insert the track into a frame with margin 'margin'. """
        QFrame.__init__(self, parent, name, f)
        self.setFrameStyle(FRAME_STYLE)
        if palette:
            self.setPalette(palette)
        self.margin = margin
        if track != None:
            self.track = track
        else:
            self.track = SampleWidget.SampleWidget()
        self.resize(self.track.width() + margin * 2, self.track.height() + margin * 2)
        self.track.reparent(self, QPoint(margin, margin))
        self.connect(self.track, PYSIGNAL('loaded'), self.slotLoaded)
        self.connect(self.track, PYSIGNAL('unload'), self.slotUnload)
        self.connect(self.track, PYSIGNAL('collapsed'), self.slotCollapsed)
        self.connect(self.track, PYSIGNAL('expanded'), self.slotExpanded)
        self.mousePressed = 0
    
    def slotLoaded(self):
        self.emit(PYSIGNAL('loaded'), (self,))
    
    def slotUnload(self):
        self.hide()
        self.emit(PYSIGNAL('unloaded'), (self,))
        self.close(1)
        
    def slotCollapsed(self):
        self.resize(self.track.width() + self.margin*2, self.track.height() + self.margin*2)
        self.emit(PYSIGNAL('collapsed'), (self,))
        
    def slotExpanded(self):
        self.resize(self.track.width() + self.margin*2, self.track.height() + self.margin*2)
        self.emit(PYSIGNAL('expanded'), (self,))
        
    def mousePressEvent(self, e):
        self.mousePressed = 1
        return QFrame.mousePressEvent(self, e)
        
    def mouseReleaseEvent(self, e):
        self.mousePressed = 0
        self.emit(PYSIGNAL('selected'), (self,))
        e.accept()
        
    def mouseMoveEvent(self, e):
        """ Drag a pointer to 'self' """
        if self.mousePressed:
            Globals.dragObject = QTextDrag('PKSampler: dragging a track', self)
            Globals.dragObject.trackFrame = self
            Globals.dragObject.dragCopy()


class MainWindow(QWidget):
    def __init__(self, parent=None, name='', f=0):
        QWidget.__init__(self, parent, name, f)
        self.setFixedWidth(1024)
        self.setFixedHeight(768)
        
        
        ## UPPER PANEL
        
        self.upperPanel = QFrame(self)
        self.upperPanel.setFixedWidth(self.width())
        self.upperPanel.setFixedHeight(self.height() / 2)
        UpperLayout = QHBoxLayout(self.upperPanel)
        
        # Main SampleGroup
        self.mainSampleGroup = SampleGroup(self.upperPanel)
        self.mainSampleGroup.setSizePolicy(QSizePolicy.Expanding,
                                           QSizePolicy.Expanding)
        UpperLayout.addWidget(self.mainSampleGroup)
        
        
        ## LOWER PANEL
        
        self.lowerPanel = QFrame(self)
        self.lowerPanel.setGeometry(0, 
                                    self.height() / 2, 
                                    self.width(), 
                                    self.height() / 2)
        LowerLayout = QHBoxLayout(self.lowerPanel)
        
        # WidgetStack
        self.widgetStack = Widgets.WidgetStack(self.lowerPanel)
        self.widgetStack.setSizePolicy(QSizePolicy.Expanding, 
                                       QSizePolicy.Expanding)
        LowerLayout.addWidget(self.widgetStack)
        for i in range(NUM_SAMPLE_GROUPS):
            group = SampleGroup(None)
            self.widgetStack.addWidget(group)
        
        # Selector
        self.selector = Selector(self.lowerPanel)
        self.selector.addPath(os.path.join(os.environ['HOME'], 'wav'))
        self.selector.setFixedWidth(SELECTOR_WIDTH) 
        self.selector.setFixedHeight(SELECTOR_HEIGHT)
        self.selector.move(self.width()-SELECTOR_WIDTH,
                           self.height()-SELECTOR_HEIGHT)
        self.selector.openAll()
        QObject.connect(self.selector, PYSIGNAL('selected'), 
                        self.slotSelected)
        LowerLayout.addWidget(self.selector)
        
        ## SAMPLES
        
        self.freeSamples = Queue.Queue()
        self.busySamples = []
        for i in range(CACHED_SAMPLES):
            self.newSample()
            
    def newSample(self):
        s = Sample.Sample()
        self.freeSamples.put(s)
        QObject.connect(s, PYSIGNAL('delete'), 
                        self.slotDeleteSample)
        
    def slotSelected(self, path):
        if not self.freeSamples.qsize():
            self.newSample()
        sample = self.freeSamples.get()
        try:
            sample.load(path)
        except:
            self.freeSamples.put(sample)
            return
        self.busySamples.append(sample)
        self.mainSampleGroup.add(sample)
        
    def slotDeleteSample(self, sample):
        self.busySamples.remove(sample)
        self.freeSamples.put(sample)
        

def main():
    a = QApplication([])
    PKAudio.start_server()
    w = MainWindow()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
    
    

if __name__ == "__main__":
    main()
    
