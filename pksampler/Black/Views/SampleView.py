""" SampleView.py: A view that groups samples. """

from qt import *
from Black.GUI import TabView, Part, Button, Slider
import SampleControl
import Globals
from Black.GUI.Common import FONT, VIEW_LAYOUT_SPACING
from Black.GUI.Common import SMALL_CORNER_RADIUS as BUTTON_RADIUS

ROWS = 7
COLS = 8

COLOR = QColor('blue').light(150)

BUTTON_COLORS = {'playing' : QColor('green'),
                 'cued' : QColor('red'),
                 'paused' : QColor('yellow'),
                }
ZONE_COLOR = QColor('red')
SAMPLE_BUTTON_SIZE = QSize(150,30)
CONTROL_WIDTH = 70


displayTimer = Globals.DisplayTimer()

class Control(Part):
    def __init__(self, parent=None, name=None, f=0):
        Part.__init__(self, parent, name, f)
        self.setMinimumWidth(275)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        self.setColor(COLOR)
        self.sample = None

        self.label = QLabel(self)
        self.label.setFont(FONT)
        self.label.setFixedWidth(200)

        self.posLabel = QLabel(self)
        self.posLabel.setFont(QFont( "Helvetica", 11, QFont.Bold ))
        self.posLabel.setAlignment(Qt.AlignRight)
        self.posLabel.setGeometry(175, 50, 105, 35)
        
        self.mainZone = Button(self, 'Main Output')
        self.mainZone.setRoundCorners(False)
        self.mainZone.setToggleButton(True)
        self.mainZone.setFixedSize(CONTROL_WIDTH, 35)
        #self.mainZone.setColor(ZONE_COLOR)
        QObject.connect(self.mainZone, PYSIGNAL('toggled'),
                        self.slotMainMute)
            
        self.mainVolume = Slider(Qt.Vertical, self)
        self.mainVolume.setAnimated(False)
        self.mainVolume.setMinimumWidth(CONTROL_WIDTH)
        #self.mainVolume.setL33t(True)
        QObject.connect(self.mainVolume, SIGNAL('valueChanged(int)'),
                        self.slotMainVolume)

        self.cueZone = Button(self, 'Cue Output')
        self.cueZone.setGeometry(90, 50, 70, 25)
        self.cueZone.setFixedSize(CONTROL_WIDTH, 35)
        self.cueZone.setRoundCorners(False)
        self.cueZone.setToggleButton(True)
        #self.cueZone.setColor(ZONE_COLOR)
        QObject.connect(self.cueZone, PYSIGNAL('toggled'),
                        self.slotCueMute)
        self.cueVolume = Slider(Qt.Vertical, self)
        self.cueVolume.setAnimated(False)
        self.cueVolume.setMinimumWidth(CONTROL_WIDTH)
        #self.cueVolume.setL33t(True)
        QObject.connect(self.cueVolume, SIGNAL('valueChanged(int)'),
                        self.slotCueVolume)


        self.play = Button(self, 'play')
        self.play.move(175, 100)
        self.play.setFixedSize(CONTROL_WIDTH, 35)
        self.play.setCornerRadius(BUTTON_RADIUS)
        QObject.connect(self.play, PYSIGNAL('clicked'), self.slotPlay)
        
        self.cue = Button(self, 'cue')
        self.cue.move(175, 155)
        self.cue.setFixedSize(CONTROL_WIDTH, 35)
        self.cue.setCornerRadius(BUTTON_RADIUS)
        QObject.connect(self.cue, PYSIGNAL('clicked'), self.slotCue)
            
        self.pause = Button(self, 'pause')
        self.pause.move(175, 210)
        self.pause.setCornerRadius(BUTTON_RADIUS)
        self.pause.setFixedSize(CONTROL_WIDTH, 35)
        QObject.connect(self.pause, PYSIGNAL('clicked'), self.slotPause)
        
        self.loop = Button(self, 'loop')
        self.loop.setToggleButton(True)
        self.loop.setFixedSize(CONTROL_WIDTH, 35)
        self.loop.setCornerRadius(BUTTON_RADIUS)
        QObject.connect(self.loop, PYSIGNAL('toggled'), self.slotToggleLoop)


        Layout = QGridLayout(self, 8, 2)
        Layout.setAlignment(Qt.AlignHCenter)
        Layout.setSpacing(5)
        Layout.setMargin(15)
        Layout.addMultiCellWidget(self.label, 0, 0, 0, 1)
        Layout.addMultiCellWidget(self.posLabel, 1, 1, 0, 1)
        Layout.addWidget(self.mainZone, 2, 0)
        Layout.addWidget(self.cueZone, 2, 1)
        Layout.addWidget(self.mainVolume, 3, 0)
        Layout.addWidget(self.cueVolume, 3, 1)
        Layout.addWidget(self.play, 4, 0)
        Layout.addWidget(self.cue, 4, 1)
        Layout.addWidget(self.pause, 5, 0)
        Layout.addWidget(self.loop, 5, 1)

        self.setEnabled(False)
                
    #def paintEvent(self, e):
    #    """ Draw *everything* """
    #    Part.paintEvent(self, e)

    def setSample(self, sample):
        """ Pass None to reset and disable the widget. """
        if sample == self.sample:
            return
        self.sample = sample
        if sample:
            self.label.setText(sample.getShortName().upper())
            self.mainVolume.setValue(sample.getVolume(zone=0))
            self.cueVolume.setValue(sample.getVolume(zone=1))
            self.mainZone.setOn(sample.getZone(0))
            self.cueZone.setOn(sample.getZone(1))
            self.loop.setOn(sample.looping())
            self.setEnabled(True)
        else:
            self.mainVolume.setValue(0)
            self.cueVolume.setValue(0)
            self.setEnabled(False)

    def slotMainMute(self, b, on):
        self.sample.slotSetZone(0, on)

    def slotCueMute(self, b, on):
        self.sample.slotSetZone(1, on)
        
    def slotMainVolume(self, v):
        self.sample.setVolume(self.mainVolume.maxValue() - v, zone=0)
        
    def slotCueVolume(self, v):
        self.sample.setVolume(self.cueVolume.maxValue() - v, zone=1)

    def slotPlay(self):
        self.sample.slotStart()
        global displayTimer
        displayTimer.register(self)

    def slotCue(self):
        self.sample.slotCue()
        global displayTimer
        displayTimer.deregister(self)

    def slotPause(self):
        self.sample.slotPause()
        global displayTimer
        displayTimer.deregister(self)

    def slotToggleLoop(self, b, on):
        self.sample.slotLooping(on)

    def updateDisplay(self):
        p = int(self.sample.pos())
        self.posLabel.setText(str(p / 1000))
        


class SampleButton(Button, SampleControl.Listener):
    def __init__(self, sample, parent=None, name=None):
        Button.__init__(self, parent, name)
        SampleControl.Listener.__init__(self, sample)
        if sample.isPlaying():
            self.slotStart()
        elif sample.pos() == 0:
            self.slotCue()
        else:
            self.slotPause()

    def slotStart(self):
        self.setPaletteForegroundColor(BUTTON_COLORS['playing'])
        self.startFlashing()

    def slotPause(self):
        self.setPaletteForegroundColor(BUTTON_COLORS['paused'])
        self.stopFlashing()

    def slotCue(self):
        self.setPaletteForegroundColor(BUTTON_COLORS['cued'])
        self.stopFlashing()


class SampleView(TabView):
    """ Groups samples into buttons and contains a single control widget. """
    
    def __init__(self, parent=None, name=None, f=0):
        TabView.__init__(self, parent, name, f)
        Layout = QHBoxLayout(self)
        Layout.setSpacing(VIEW_LAYOUT_SPACING)
        Layout.setMargin(VIEW_LAYOUT_SPACING)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.label = QLabel('hey', self)
        self.label.move(100, 100)

        # group widget
        self.group = QWidget(self)
        GroupLayout = QGridLayout(self.group, ROWS, COLS, 0)
        GroupLayout.setMargin(3)
        GroupLayout.setSpacing(5)
        GroupLayout.setAutoAdd(True)
        Layout.addWidget(self.group)

        # control widget
        self.control = Control(self, "controlWidget")
        Layout.addWidget(self.control)
        
        self.buttons = []
        
    def add(self, sample):
        button = SampleButton(sample, self.group)
        button.setFixedSize(SAMPLE_BUTTON_SIZE)
        button.setCornerRadius(BUTTON_RADIUS)
        button.show()
        button.setText(sample.getShortName())
        QObject.connect(button, PYSIGNAL('clicked'), self.slotSelected)
        self.buttons.append(button)
        
    def remove(self, sample):
        for button in self.buttons:
            if button.sample == sample:
                self.buttons.remove(button)
                QObject.disconnect(button, 
                                   PYSIGNAL('clicked'),
                                   self.slotSelected)
                button.reparent(None, QPoint(0, 0))

    def slotSelected(self, button):
        self.selectSample(button.sample)

    def selectSample(self, sample):
        for b in self.buttons:
            if b.sample == sample:
                self.selectedSample = b.sample
                self.control.setSample(b.sample)



class _Sample(QObject):
    def __init__(self, name):
        QObject.__init__(self, None, name)
        self._volumes = [0,0]
        self._pos = 0
        self.zones = [False, False]
        self._looping = False
        self._playing = False
    def getShortName(self):
        return str(self.name())
    def setVolume(self, v, zone=0):
        self._volumes[zone] = v
        print 'sample:volume',v
    def getVolume(self, zone=0):
        return self._volumes[zone]
    def getZone(self, zone=0):
        return self.getVolume(zone)
    def slotStart(self):
        print 'sample:start'
        self._playing = True
    def slotCue(self):
        print 'sample:cue'
        seelf._playing = False
    def slotPause(self):
        print 'sample:pause'
        self.playing = False
    def pos(self):
        return self._pos
    def slotSetZone(self, zone, on):
        self.zones[zone] = on
        print 'zone',zone,on
    def looping(self):
        return self._looping
    def slotLooping(self, on):
        self._looping = on
    def isPlaying(self):
        return self._playing
    

def test_Control():
    a = QApplication([])
    w = Control()
    w.setPaletteBackgroundColor(QColor('black'))
    w.setSample(_Sample('Sample 1'))
    w.setSample(_Sample('Sample 2'))
    w.show()
    b = QPushButton(None, 'fade me')
    def fade():
        if w.fadeDirection == 'in':
            w.fadeOut()
        else:
            w.fadeIn()
    QObject.connect(b, SIGNAL('clicked()'), fade)
    b.show()
    a.setMainWidget(w)
    a.exec_loop()

def test_SampleView():
    a = QApplication([])
    w = SampleView()
    w.add(_Sample('Sample 1'))
    w.add(_Sample('Sample 2'))
    w.show()
    w.resize(1000, w.height())
    b = QPushButton(None)
    b.setText('fade me')
    def fade():
        if w.fadeDirection == 'in':
            w.fadeOut()
        else:
            w.fadeIn()
    QObject.connect(b, SIGNAL('clicked()'), fade)
    b.show()
    a.setMainWidget(w)
    a.exec_loop()

def test_Slider():
    a = QApplication([])
    w = Slider()
    def p(v):
        print 'valueChanged',v
    QObject.connect(w, SIGNAL('valueChanged(int)'), p)
    w.show()
    w.resize(50, 200)
    a.setMainWidget(w)
    a.exec_loop()

def main():
    test_Control()
