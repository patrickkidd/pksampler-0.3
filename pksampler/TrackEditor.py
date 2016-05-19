""" User interface for stored track data.
    Includes a wave view and cue editor.
"""

from qt import *
from qtcanvas import *
import threading
import Globals
import Widgets
import PovWidgets

cueLineColor = QColor(85,170,255)
search_res = 1000


class CueSlider(QWidget):
    """ A slider-like widget that selects cue points.
        SIGNALS: PYSIGNAL("valueChanged") (percent)
                 PYSIGNAL("enabled"), ()
                 PYSIGNAL("disabled"), ()
    """

    def __init__(self, useEnableButton, text, parent=None, name=None, f=0):
        QWidget.__init__(self, parent, name, f)
        self.setCaption('PKSampler: Cue Slider')
        self.setFixedHeight(40)
        self.position = 0
        self.lastValue = 0
        self.pressed = 0
        self.enabled = 0
        self.range = 100

        self.leftButton = PovWidgets.PushButton('pk_button', 'blue', self)
        self.leftButton.setGeometry(0,0,20,22)
        self.leftButton.setText("<")
        self.connect(self.leftButton, PYSIGNAL("clicked"), self.slotLeft)

        self.rightButton = PovWidgets.PushButton('pk_button', 'blue', self)
        self.rightButton.setGeometry(20,0,20,22)
        self.rightButton.setText(">")
        self.connect(self.rightButton, PYSIGNAL("clicked"), self.slotRight)

        self.label = QLabel(self)
        self.label.resize(50, 13)
        self.label.setText(text)

        self.valueLabel = QLabel(self)
        self.valueLabel.resize(100, 13)
        self.valueLabel.setAlignment(Qt.AlignRight)
        self.valueLabel.setText("0")

        self.line = QFrame(self)
        self.line.move(0,30)

        if useEnableButton:
            self.enableButton = PovWidgets.PushButton('pk_button', 'red', self)
            self.enableButton.setGeometry(60,0,50,22)
            self.enableButton.setText("Enable")
            self.connect(self.enableButton, PYSIGNAL("toggled"),
                         self.slotEnable)
            self.enableButton.setOn(0)
            self.slotEnable(0)
        else:
            self.enableButton = None
            self.slotEnable(1)
            
        # to set the size
        self.resize(self.size())

    def value(self):
        return self.position

    def slotEnable(self, a0):
        self.enabled = a0
        self.rightButton.setEnabled(a0)
        self.leftButton.setEnabled(a0)
        if self.enabled:
            if self.enableButton:
                self.enableButton.setText("Disable")
            self.line.setPaletteBackgroundColor(cueLineColor)
            self.valueLabel.show()
            self.label.show()
            self.emit(PYSIGNAL("enabled"), ())
        else:
            if self.enableButton:
                self.enableButton.setText("Enable")
            self.line.setPaletteBackgroundColor(self.palette().color(QPalette.Active, QColorGroup.Background))
            self.valueLabel.hide()
            self.label.hide()
            self.emit(PYSIGNAL("disabled"), ())

        self.update()

    def slotRight(self):
        self.SetValue(self.position + search_res)

    def slotLeft(self):
        self.SetValue(self.position - search_res)
        
    def resizeEvent(self, e):
        """ resize the line and move the labels. """
        self.label.move(self.width() - 40, 5)
        self.valueLabel.move(self.width() - 170, 5)
        self.line.resize(self.width(),2)

    def mousePressEvent(self, e):
        # Accept if the pointer was around the line
        if not self.enabled:
            return
        margin = 10
        x = e.x()
        y = e.y()
        lx = self.line.x()
        ly = self.line.y()
        if x > self.line.x() and x < self.line.x() + self.line.width() + margin and \
            y > self.line.y() - margin and y < self.line.y() + margin:
            self.pressed = 1
            e.accept()
            x = e.x() - self.line.x()
            perc = (x * 1.0) / self.line.width()
            self.SetValue(int(self.range * perc))

    def mouseMoveEvent(self, e):
        """ translate an x value into a real value. """
        if not self.enabled:
            return
        margin = 10
        if self.pressed:
            if e.x() > self.line.x() and e.x() < self.line.x() + self.line.width():
                e.accept()
                x = e.x() - self.line.x()
                perc = (x * 1.0) / self.line.width()
                self.SetValue(int(self.range * perc))

    def SetValue(self, value):
        """ Set the slider value in percent. """
        self.SetValuePassive(value)
        self.emit(PYSIGNAL("valueChanged"), (self.position, None))
        
    def SetValuePassive(self, value):
        """ Like setValue(), but doesn't emit valueChanged. """
        if value < 0:
            value = 0
            self.leftButton.setEnabled(0)
        elif value > self.range:
            value = self.range
            self.rightButton.setEnabled(0)
        else:
            self.rightButton.setEnabled(1)
            self.leftButton.setEnabled(1)
        self.position = value
        self.valueLabel.setText(str(self.position / search_res))
        self.update()        
    
    def mouseReleaseEvent(self, e):
        self.pressed = 0

    def paintEvent(self, e):
        """ Draw a triangle on the current location.
            The triangle is currently QSize(8, 6)
        """
        paint = QPainter(self)
        if self.enabled:
            paint.setPen(cueLineColor)
            paint.setBrush(cueLineColor)
        else:
            paint.setPen(self.palette().color(QPalette.Active, QColorGroup.Background))
            paint.setBrush(self.palette().color(QPalette.Active, QColorGroup.Background))

        # Set the points according to the line and self.position
        inc = (self.line.width() * 1.0) / self.range
        y = self.line.y() + self.line.height() + 1
        if self.position > 0:
            x = (self.position * inc) + self.line.x()
            x = int(x)
        else:
            x = self.line.x()
        x1 = x
        y1 = y
        x2 = x - 4
        y2 = y + 6
        x3 = x + 4
        y3 = y + 6

        pointArray = QPointArray([x1,y1,x2,y2,x3,y3])
        paint.drawPolygon(pointArray)
        
    def SetRange(self, range):
        """ Set the maximum value in samples. """
        self.range = range
        


class CueEditor(QWidget):
    """ Interface for editing cue points/loops. """

    def __init__(self, sampleControl, parent=None, name=None, f=0):
        QWidget.__init__(self, parent, name, f)
        self.setCaption('PKSampler: Cue Editor')
        self.setPaletteBackgroundColor(QColor(0,85,255))
        self.x_margin = 10
        
        self.sampleControl = sampleControl
        QObject.connect(self.sampleControl, PYSIGNAL('updated'),
                        self.slotSampleUpdated)

        # 'Cue Editor' Label
        self.cueLabel = QLabel(self)
        self.cueLabel.setText("Cue Editor")
        self.cueLabel.setGeometry(self.x_margin,self.x_margin,200,23)
        cueLabel_font = QFont(self.cueLabel.font())
        cueLabel_font.setPointSize(16)
        cueLabel_font.setItalic(1)
        cueLabel_font.setUnderline(1)
        self.cueLabel.setFont(cueLabel_font)

        # Current cue box
        width = 40
        self.currentCueBox = QLabel(self)
        self.currentCueBox.resize(width,width)
        self.currentCueBox.setAlignment(Qt.AlignCenter)
        self.currentCueBox.setPaletteBackgroundColor(QColor(85,170,255))
        currentCueBox_font = QFont(self.currentCueBox.font())
        currentCueBox_font.setPointSize(23)
        self.currentCueBox.setFont(currentCueBox_font)
        self.currentCueBox.setCursor(QCursor(13))
        
        # Cue Sliders
        
        self.startCueSelector = CueSlider(0, "Start", self)
        self.startCueSelector.move(self.x_margin,50)
        self.connect(self.startCueSelector, PYSIGNAL("valueChanged"), 
            self.slotStartChanged)
            
        self.endCueSelector = CueSlider(1, "End", self)
        self.endCueSelector.move(self.x_margin,
                self.startCueSelector.height() + self.startCueSelector.y() + 5)
        self.connect(self.endCueSelector, PYSIGNAL("valueChanged"),
                self.slotEndChanged)
        self.connect(self.endCueSelector, PYSIGNAL("enabled"), 
                self.slotEndEnabled)
        self.connect(self.endCueSelector, PYSIGNAL("disabled"), 
                self.slotEndDisabled)
            
        # Cue buttons
        
        self.label1 = QLabel("Cue: ", self)
        font = QFont()
        font.setPointSize(11)
        self.label1.setFont(font)
        self.label1.move(self.x_margin,150)
        self.label1.resize(40,20)
        
        # Set up cue buttons / data
        self.cueButtons = []
        font = QFont()
        width = 30
        font.setPointSize(19)
        self.n_cues = 9
        #self.buttonGroup = QButtonGroup(self)
        #self.buttonGroup.setExclusive(1)
        #self.connect(self.buttonGroup, SIGNAL('clicked()'), self.slotCue)
        
        for i in range(Globals.n_cues):
            # buttons
            button = PovWidgets.PushButton('button', parent=self)
            button.setText(str(i))
            button.resize(width,width + (width / 10))
            button.move(self.x_margin + 50 + (width + 10) * i, 140)
            button.setFont(font)
            self.cueButtons.append(button)
            
        self.selectedCue = 0
        self.slotCue(0)
        
        # the little line under the cue buttons
        
        self.cue_underline = QFrame(self)
        self.cue_underline.resize(10, 1)
        c = self.cue_underline.paletteBackgroundColor()
        self.cue_underline.setPaletteBackgroundColor(c.light(125))
        y = self.cueButtons[0].y() + self.cueButtons[0].height() + 5
        self.cue_underline.move(self.x_margin, y)

        self.resize(self.size())
    
    def slotCue(self, index):
        """ Selects a cue button id - 1. """
        
        start = self.startCueSelector.value()
        end = self.endCueSelector.value()
        
        # save the states
        s = self.sampleControl.sample
        if s:
            s.cues[self.selectedCue][0] = start
            s.cues[self.selectedCue][1] = end

        # Activate the buttons
        self.selectedCue = index
        self.cueButtons[self.selectedCue].setOn(1)
        
        start = 0
        end = 0
        
        # get stored values
        if s:
            start = s.cues[self.selectedCue][0]
            end = s.cues[self.selectedCue][1]
            
        # Set the slider positions to new cues
        self.startCueSelector.SetValuePassive(start)
        self.endCueSelector.SetValuePassive(end)
            
        # Set the active cue label
        self.currentCueBox.setText(QString(str(index)))
        

    def slotStartChanged(self, value):
        if value > self.endCueSelector.value():
            self.endCueSelector.SetValue(value + 1000)
            
        s = self.sampleControl.sample
        if s:
            s.cues[s.selectedCue][0] = value
            if s.selectedCue == s.selectedCue:
                s.Reset()

        self.emit(PYSIGNAL('startChanged'), (value, None))

    def slotEndChanged(self, value):
        if value < self.startCueSelector.value():
            self.startCueSelector.SetValue(value)
            value += 1000
            
        s = self.sampleControl.sample
        if s:
            s.cues[s.selectedCue][1] = value
            
        self.emit(PYSIGNAL('endChanged'), (value, None))
        
    def slotEndEnabled(self):
        s = self.sampleControl.sample
        if s:
            s.SetEnd(s.cues[s.selectedCue][1])
            
    def slotEndDisabled(self):
        s = self.sampleControl.sample
        if s:
            s.SetEnd(s.length())

    def resizeEvent(self, e):
        self.currentCueBox.move(self.width() - 60, 4)
        self.startCueSelector.resize(self.width() - self.x_margin * 2
                , self.startCueSelector.height())
        self.endCueSelector.resize(self.width() - self.x_margin * 2
                , self.startCueSelector.height())
        
        l = (self.cueButtons[0].width() + 10) * self.n_cues
        self.cue_underline.resize(l + 50, 1)
        
    def slotSampleUpdated(self):
        """ re-read the length and cue info. """
        s = self.sampleControl.sample
        if s:
            self.startCueSelector.SetRange(s.length())
            self.endCueSelector.SetRange(s.length())
            
            self.startCueSelector.SetValuePassive(s.cues[self.selectedCue][0])
            self.endCueSelector.SetValuePassive(s.cues[self.selectedCue][1])

    def GetCue(self, index):
        """ Return a tuple with frames [start,end] """
        s = self.sampleControl.sample
        if s:
            return s.cues[self.selectedCue]
        else:
            return [0,0]
        
    def SetLength(self, length):
        """ Set the length in samples and reset the cue data. """
        # Set the sliders
        self.startCueSelector.SetRange(length)
        self.endCueSelector.SetRange(length)
        

class WaveDisplay(QCanvasView):
    """ Displays a visual wave readout of wave media. """

    class ReaderThread(threading.Thread):
        """ Fills a wave display from media. """
        def __init__(self, media, display):
            threading.Thread.__init__(self)
            self.display = display
            self.media = media
            self.resolution = 16384

        def run(self):
            """ Fill the display. """
            l = self.media.length()
            raise Exception('implement this!')
            seg = PK.Segment(50)
            reader = PK.MetaReader(self.media)
            s_read = 0
            while s_read < self.media.length() / self.resolution:
                s_read += reader.Read(seg, self.resolution)
                print "read",s_read,"samples"
                self.display.AppendSegment(seg)

    def __init__(self, media, parent=None, name=None, f=0):
        """ Construct a wave display with a MediaLayer as 'media'.
            The display will reset and read all of the data from the
            media device in a different thread.
        """
        QCanvasView.__init__(self, parent, name, f)
        self.setCaption('PKSampler: Wave Display')
        self._canvas = QCanvas()
        self.setCanvas(self._canvas)
        self.mutex = QMutex()
        
        self._canvas.resize(self.width(), self.height())
        self._canvas.resize(self.width(), self.height())
        
        self.thread = WaveDisplay.ReaderThread(media, self)

        # The margin between left and right channels.
        self.numSamples = 0
        self.last_y = -1
        self.last_x = -1
        
        # this coefficient should scale half the band width to the canvas height
        half_canvas_height = self._canvas.height() * 1.0
        self.y_scale = (half_canvas_height / 2) / 32768
        len = media.length() * -1.0
        w = self._canvas.width() * -1.0
        self.x_inc = w / (len / self.thread.resolution) * 2

        media.pos(0)
        self.thread.start()

    def paintEvent(self, e):
        self.mutex.lock()
        QCanvasView.paintEvent(self, e)
        self.mutex.unlock()
        
    def AppendSegment(self, seg):
        """ Place the segment data at the back of the display. """
        self.mutex.lock()
        
        # Add a canvas line to the correct side.
        i=0
        if self.last_y == -1:
            self.last_y = int(seg[0] * self.y_scale) + self._canvas.height() / 2
            self.last_x = 0
            i=2
            
        while i+1 < seg.length():
            line = QCanvasLine(self._canvas)
            l = seg[i]
            r = seg[i+1]
            i += 2
            y = 0
            x = 0
            
            if abs(l) > abs(r):
                y = l
            else:
                y = r
            # scale to canvas height
            y = int(y * self.y_scale)
            # transform to middle canvas y-value
            half_canvas_height = self._canvas.height() / 2
            y += half_canvas_height

            # scale to canvas width
            x = self.last_x + self.x_inc
            
            line.setPoints(self.last_x, self.last_y, x, y)
            line.show()
            
            #print self.last_x,",", self.last_y, x,",", y
            self.last_y = y
            self.last_x = x
            self.numSamples += 1

        self.mutex.unlock()
        self._canvas.update()


class TrackEditor(QFrame):
    """ The main widget. Should be resizable. """
    
    def __init__(self, sampleControl, parent=None, name=None, f=0):        
        QFrame.__init__(self, parent, name, f)
        self.setCaption('PKSampler: Track Editor')
        self.setFrameStyle(QFrame.Box | QFrame.Sunken)
        
        self.cueEditor = CueEditor(sampleControl, self, "Cue Editor")
        self.cueEditor.show()
        self.cueEditor.resize(self.width() - 4, self.height() - 4)
        self.cueEditor.move(2,2)
    
    def resizeEvent(self, e):
        self.cueEditor.resize(self.width() - 4, self.height() - 4)
        
    def SetTrackLength(self, length):
        """ Set the cue editor's length in samples. """
        self.cueEditor.SetLength(length)
        
        
if __name__ == "__main__":
    import SampleControl
    import PKAudio
    PKAudio.start_server()
    a = QApplication([])
    s = SampleControl.SampleControl()
    w = TrackEditor(s)
    w.show()
    a.setMainWidget(w)
    a.exec_loop()
