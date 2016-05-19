""" Common.py: commonly-used widgets.
    TODO:
     - Get Fadeable to fade different parts of the widget
       (i.e. foregroundColor, backgroundColor, both, border, etc)
"""

from qt import *
from Queue import Queue
import Globals

ANIM_RES = 10
FONT = QFont( "Helvetica", 15, QFont.Bold )
SMALL_CORNER_RADIUS = 25
VIEW_LAYOUT_SPACING = 10

class WidgetCache(Queue):
    """ Caches sample widgets in a queue. """

    def __init__(self, ctor, arg=None):
        Queue.__init__(self)
        self.ctor = ctor
        self.arg = arg

    def get(self):
        # if empty, read ahead
        if self.qsize() == 0:
            if self.arg:
                o = self.ctor(self.arg)
            else:
                o = self.ctor()
            self.put(o)
        return Queue.get(self)

    def put(self, o):
        Queue.put(self, o)
        


class Slider(QSlider):
    
    def __init__(self, orientation=Qt.Vertical, parent=None, name=None):
        """ Pass a name of pixmaps labeled '[0-n].png'
            'name' should be the a-z prefix to the files.
            Uses 'name' to cache the pixmaps for other like instances.
        """
        QSlider.__init__(self, parent, name)
        self.orientation = orientation
        self.l33t = False
        
        self.animTimer = QTimer(self)
        QObject.connect(self.animTimer, SIGNAL("timeout()"), self.slotAnim)
        self.animFrames = {}
        self.animIndex = 0
        self.animated = True

        
    def paintEvent(self, e):
        """ Don't draw that bloody stuff. """
        p = QPainter(self)
        pen = p.pen()
        brush = p.brush()

        # value box
        perc = (self.value() * 1.0) / self.maxValue()
        y = self.height() - (self.height() * perc)
        c = self.paletteForegroundColor().light(125)
        p.setBrush(c)
        p.setPen(self.paletteBackgroundColor())
        pen = p.pen()
        pen.setWidth(3)
        p.setPen(pen)
        p.drawRect(0, self.height() - y, self.width(), y)

        # outline
        p.setPen(self.paletteForegroundColor())
        p.setBrush(Qt.NoBrush)
        p.drawRect(0,0, self.width(), self.height())
        QWidget.paintEvent(self, e)
        
    def mousePressEvent(self, e):
        margin = 5
        if self.orientation == Qt.Vertical:
            if e.y() > self.height() - margin:
                v = self.maxValue()
            elif e.y() < margin:
                v = self.minValue()
            else:
                v = (((e.y()-15)* 1.0) / (self.height() - 30)) * self.maxValue()   
        else:
            if e.x() > self.width() - margin:
                v = self.maxValue()
            elif e.x() < margin:
                v = self.minValue()
            else:
                v = (((e.x()-15)* 1.0) / (self.width() - 30)) * self.maxValue()
        self.setValue(v)
            
    def mouseReleaseEvent(self, e):
        pass
        
    def mouseMoveEvent(self, e):
        self.mousePressEvent(e)
        
    def setValue(self, new_val):
        """ Moves/Animates the slider into position, sets the value, emits 'clicked()' """
        if self.animated:

            if self.animTimer.isActive():
                self.animTimer.stop()
            new_val = int(new_val)
            
            # find the speed ranges
            old_val = self.value()
            travel = (new_val - old_val)
            if new_val > old_val:
                fast_end = old_val + int(travel * .6)
                slow_end = old_val + int(travel * .75)
            else:
                fast_end = old_val - int(travel * .6)
                slow_end = old_val - int(travel * .75)
                
            # calculate the animation frames
            self.animFrames = {}
            current = old_val
            i = 0
            if new_val > old_val:
                while current < new_val:
                    if current < fast_end:
                        current += 4
                    elif current < slow_end:
                        current += 2
                    else:
                        current += 1
                    if current > new_val:
                        current = new_val
                    self.animFrames[i] = current
                    i += 1
            else:
                while current > new_val:
                    if current < fast_end:
                        current -= 4
                    elif current > slow_end:
                        current -= 2
                    else:
                        current -= 1
                
                    if current < new_val:
                        current = new_val
                    self.animFrames[i] = current
                    i += 1
    
            self.animIndex = 0
            self.slotAnim()
            self.animTimer.start(ANIM_RES)
            
        else:
            QRangeControl.setValue(self, new_val)
            self.update()
            
        # not animated, but maybe l33t
        if self.l33t:
            QRangeControl.setValue(self, new_val)
            
    def slotAnim(self):
        """ Process the next animation frame. """
        if self.animIndex < len(self.animFrames):
            self.update()
            if not self.l33t:
                QSlider.setValue(self, self.animFrames[self.animIndex])
            self.animIndex += 1
        else:
            self.animTimer.stop()
            
    ## MORE PUBLIC STUFF
    
    def setL33t(self, a0):
        """ if a0 is true, a signal is only emitted once per animation. """
        self.l33t = a0
        
    def setAnimated(self, a0):
        self.animated = a0
        
    def getAnimated(self):
        return self.animated
