#!/bin/env python
""" Generic Widget classes. """

from qt import *
import Globals
import math
import os
from pov import embedded_pixmaps

use_gradients = 1

# a factor to speed up animations, reducing CPU requirments
# this is basically a 'skip frames' value
ANIMATION_COEF = 2

class Gradient:
    Vertical = 0
    Horizontal = 1
    
def gradient(pixmap, ca, cb, eff, ncols):
    """ Returns a gradient width the start and end colors. 
    eff should be Gradient.Vertical or Gradient.Horizontal
    """
    
    x=0
    y=0
    
    rca = ca.red()
    rDiff = cb.red() - rca
    
    gca = ca.green()
    gDiff = cb.green() - gca
    
    bca = ca.blue()        
    bDiff = cb.blue() - bca
    
    rl = rca << 16
    gl = gca << 16
    bl = bca << 16
    
    
    if eff == Gradient.Vertical:
        rcdelta = (1<<16) / (pixmap.height() * rDiff)
        gcdelta = (1<<16) / (pixmap.height() * gDiff)
        bcdelta = (1<<16) / (pixmap.height() * bDiff)
    else:
        print (1<<16) ,pixmap.width() * rDiff
        rcdelta = (1<<16) / (pixmap.width() * rDiff)
        gcdelta = (1<<16) / (pixmap.width() * gDiff)
        bcdelta = (1<<16) / (pixmap.width() * bDiff)
        
    p = QPainter(pixmap)
    
    # these for-loops could be merged, but the if's in the inner loop
    # would make it slow
    if eff == Gradient.Vertical:
        for y in range(pixmap.height()):
            rl += rcdelta
            gl += gcdelta
            bl += bcdelta
            p.setPen(QColor(rl>>16, gl>>16, bl>>16))
            p.drawLine(0, y, pixmap.width()-1, y)
            
    else:
        for x in pixmap.width():
            rl += rcdelta
            gl += gcdelta
            bl += bcdelta
            p.setPen(QColor(rl>>16, gl>>16, bl>>16))
            p.drawLine(x, 0, x, pixmap.height()-1)
                
    return pixmap
Globals.psyco_bind(gradient)


        
class PixmapWidget:
    """ A widget that is drawn with pixmaps. """
    
    cache = {}
    
    def cacheName(self, name):
        """ Cache all pixmaps whose names start with 'name'. """
        if not name in PixmapWidget.cache:
            pixmaps = {}
            for entry in embedded_pixmaps.embed_image_vec:
                fn = entry[8] 
                if fn.startswith(name):
                    label = fn[len(name):fn.rfind('.')]
                    i = embedded_pixmaps.uic_findImage(fn)
                    p = QPixmap(i)
                    if not p.isNull():
                        pixmaps[label] = p
            PixmapWidget.cache[name] = pixmaps
    ## NO PSYCO
    
    def __init__(self, name):
        """ 'name' is a list of paths to pixmaps to load. """
        self.widget_name = name
        self.cacheName(name)
        self.pixmaps = PixmapWidget.cache[name]

    def setPixmap(self, label):
        orig_label = label
        label = str(label)
        for i in range(5):
            if not label in self.pixmaps:
                # try another '0'
                label = '0'+label
        p = self.pixmaps[label]
        self.setPaletteBackgroundPixmap(p)
    Globals.psyco_bind(setPixmap)

    def SetMask(self, x, y, w, h):
        """ Only use a portion of the pixmap, as described by the above box.
            The x,y are the upper-left corner, and w,h are the dimensions.
        """
        new_pixmaps = {}
        for i in self.pixmaps:
            old_p = self.pixmaps[i]
            new_p = QPixmap(QSize(w,h))
            bitBlt(new_p, 0,0, old_p, x, y, w, h, Qt.CopyROP)
            new_pixmaps[i] = new_p
        self.pixmaps = new_pixmaps
        self.setFixedSize(w,h)
    Globals.psyco_bind(SetMask)
    
        
class PixmapButton(QPushButton, PixmapWidget):
    """ Takes bitmaps, animates clicks, and can change colors. """
    
    AnimRes = 50
    NumFrames = 3
    
    def __init__(self, imagename, color='red', parent=None, name=None):
        """ 'imagename' is the prefix matching desired filenames
            'color' should be ['red' | 'blue' | 'green']
            Example: PixmapButton('start_button', 'red', None)
            will load all red pixmaps that start with 'start_button',
            like start_button0.png and start_button1.png, if they are available.
        """
        if name:
            QPushButton.__init__(self, parent, name)
        else:
            QPushButton.__init__(self, parent, imagename)
        PixmapWidget.__init__(self, imagename)
        
        self.animTimer = QTimer(self)
        QObject.connect(self.animTimer, SIGNAL("timeout()"), self.slotAnimTimer)
        self.animIndex = 0
        self.animDirection = 'down'  ## ['down','down_up', 'up']
        
        QObject.connect(self, SIGNAL('toggled(bool)'), self.slotToggled)
        
        #set the color
        color = color.lower()
        self.setColor(color)
        self.AnimateClick()
        
    def drawButton(self, painter):
        """ don't draw qpushbutton stuff. """
        pass
        
    def animate(self):
        """ Set self.animDirection then call this. """
        self.animTimer.stop()
        if self.animDirection == 'up':
            self.animIndex = 2
        else:
            self.animIndex = 0
        self.slotAnimTimer()
        self.animTimer.start(PixmapButton.AnimRes)
        
    def setColor(self, color):
        self.color = color
        if color == 'red':
            self.colorOffset = 0
        elif color == 'green':
            self.colorOffset = PixmapButton.NumFrames
        elif color == 'blue':
            self.colorOffset = PixmapButton.NumFrames * 2
        else:
            self.colorOffset = 0
        self.animate()
    
    def slotAnimTimer(self):
        if self.animDirection == 'down':
            if self.animIndex < PixmapButton.NumFrames:
                self.setPixmap(self.animIndex + self.colorOffset)
                self.animIndex += 1
            else:
                self.animTimer.stop()
            
        elif self.animDirection == 'up':
            if self.animIndex >= 0:
                self.setPixmap(self.animIndex + self.colorOffset)
                self.animIndex -= 1
            else:
                self.animTimer.stop()
                
        elif self.animDirection == 'down_up':
            if self.animIndex < PixmapButton.NumFrames:
                self.setPixmap(self.animIndex + self.colorOffset)
                self.animIndex += 1
            elif self.animIndex == PixmapButton.NumFrames:
                self.animDirection = 'up'
                self.animIndex = 2
    Globals.psyco_bind(slotAnimTimer)

    def mousePressEvent(self,e):
        if not self.isToggleButton():
            self.animDirection = 'down'
            self.AnimatePress()
        QPushButton.mousePressEvent(self, e)
        
    def mouseReleaseEvent(self, e=None):
        if not self.isToggleButton():
            self.animDirection = 'up'
            self.AnimateRelease()
        if e != None:
            QPushButton.mouseReleaseEvent(self, e)
        
    def slotToggled(self, a0):
        if self.isOn():
            self.AnimatePress()
        else:
            self.AnimateRelease()
                
    
    ## ANIMATE METHODS
    
    def AnimateClick(self):
        self.animDirection = 'down_up'
        self.animate()
        
    def AnimatePress(self):
        self.animDirection = 'down'
        self.animate()
        
    def AnimateRelease(self):
        self.animDirection = 'up'
        self.animate()
                
        

class PixmapRangeControl(QRangeControl, PixmapWidget):
    """ Loads all the pixmaps in a directory, and controls the drawing. """
    
    AnimRes = 10
    
    def __init__(self, imagename, orientation):
        """ Pass a name of pixmaps labeled '[0-n].png'
            'name' should be the a-z prefix to the files.
            Uses 'name' to cache the pixmaps for other like instances.
        """
        PixmapWidget.__init__(self, imagename)
        self.inverse = 0
        self.orientation = orientation
        self.l33t = 0
        
        self.animTimer = QTimer(self)
        QObject.connect(self.animTimer, SIGNAL("timeout()"), self.slotAnim)
        self.animFrames = {}
        self.animIndex = 0
        self.animated = 1
        
    def paintEvent(self, e):
        """ Don't draw that bloody stuff. """
        pass
        
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
        #print 'PixmapRangeControl.mousePressEvent', v
        self.setValue(v)
            
    def mouseReleaseEvent(self, e):
        pass
        
    def mouseMoveEvent(self, e):
        self.mousePressEvent(e)
        
    def setValue(self, new_val):
        """ Moves/Animates the slider into position, sets the value,
            emits 'clicked()'
        """
        new_val = int(new_val)
        if self.animated:

            if self.animTimer.isActive():
                self.animTimer.stop()
                
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
                        current += 4 * ANIMATION_COEF
                    elif current < slow_end:
                        current += 2 * ANIMATION_COEF
                    else:
                        current += 1 * ANIMATION_COEF
                    if current > new_val:
                        current = new_val
                    self.animFrames[i] = current
                    i += 1
            else:
                while current > new_val:
                    if current > fast_end:
                        current -= 4 * ANIMATION_COEF
                    elif current > slow_end:
                        current -= 2 * ANIMATION_CEOF
                    else:
                        current -= 1 * ANIMATION_COEF
                
                    if current < new_val:
                        current = new_val
                    self.animFrames[i] = current
                    i += 1
    
            self.animIndex = 0
            self.slotAnim()
            self.animTimer.start(PixmapRangeControl.AnimRes)
            
        else:
            try:
                QSlider.setValue(self, int(new_val))
            except TypeError:
                # for test/debugging
                print type(new_val)
                raise
            self.setPixmap(self.value())
            
        # not animated, but maybe l33t
        if self.l33t:
            QSlider.setValue(self, int(new_val))
    Globals.psyco_bind(setValue)
            
            
    def slotAnim(self):
        """ Process the next animation frame. """
        if self.animIndex < len(self.animFrames):
            self.setPixmap(self.animFrames[self.animIndex])
            if not self.l33t:
                QSlider.setValue(self, self.animFrames[self.animIndex])
            self.animIndex += 1
        else:
            self.animTimer.stop()
            
    def setPixmap(self, value):
        """ used internally to set the current pixmap. """
        if value < self.minValue():
            value = self.minValue()
        elif value > self.maxValue():
            value = self.maxValue()
        if self.inverse:
            value = str((self.maxValue() - self.minValue()) - value)
        PixmapWidget.setPixmap(self, value)
            
            
    ## MORE PUBLIC STUFF
            
    def setL33t(self, a0):
        """ if a0 is true, SIGNAL('valueChanged(int)') is only emitted once per animation. """
        self.l33t = a0
        
    def setInversePixmaps(self, inverse):
        """ Reverses the action of the range control. """
        self.inverse = inverse
        
    def setAnimated(self, a0):
        self.animated = a0
        
    def getAnimated(self):
        return self.animated

        
class OutputWidget(QWidget):
    def __init__(self, parent=None, name=None, f=0):
        QWidget.__init__(self, parent, name, f)
        
        self.textBrowser = QTextBrowser(self)
        self.textBrowser.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.layout = QBoxLayout(self, QBoxLayout.LeftToRight, 0, 0)
        self.layout.add(self.textBrowser)
        self.startTimer(500)
        
    def timerEvent(self, e):
        # get this to read some sort of output
        #self.textBrowser.append(Globals.PK.readStdout())
        pass
        
        
class WidgetStack(QWidget):
    """ A widget stack with buttons that switch between them. 
        Functions just like a QWidget stack, except, the signals are converted to PYSIGNALs.
    """
    def __init__(self, parent=None, name=None, f=0):
        QWidget.__init__(self, parent, name, f)
    
        layout = QHBoxLayout(self,0,0,"stackLayout")

        self.widgetStack = QWidgetStack(self, 'widgetStack')
        self.widgetStack.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,
                                                   QSizePolicy.Expanding))
        layout.addWidget(self.widgetStack)
        
        self.buttonGroup = QVButtonGroup(self)
        self.buttonGroup.setFrameStyle(QFrame.TabWidgetPanel | QFrame.Raised)
        self.buttonGroup.setMinimumWidth(55)
        self.buttonGroup.setInsideMargin(3)
        self.buttonGroup.setInsideSpacing(15)
        self.buttonGroup.setExclusive(1)
        self.buttonGroup.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                                   QSizePolicy.Expanding))
        QObject.connect(self.buttonGroup, SIGNAL('clicked(int)'),
                        self.slotButton)
        layout.addWidget(self.buttonGroup)
        
        QObject.connect(self.widgetStack, SIGNAL('aboutToShow(int)'),
                        self.slotATS)
        QObject.connect(self.widgetStack, SIGNAL('aboutToShow(QWidget*)'),
                        self.slotATS)

        self.n_widgets = 0
        
    def slotButton(self, id):
        self.raiseWidget(id)
        
    def slotATS(self, a0):
        self.emit(PYSIGNAL('aboutToShow'), (a0,))
        
    def addWidget(self, w, id=-1, button=None):
        """ Set the name of w to the new button's text. """
        self.widgetStack.addWidget(w, id)
        id = self.widgetStack.id(w)
        if button == None:
            button = QPushButton(self.buttonGroup)
        else:
            button.reparent(self.buttonGroup, QPoint(0,0))
        button.setToggleButton(1)
        self.buttonGroup.insert(button, id)
        self.n_widgets += 1
        
        # get the correct button to show
        self.raiseWidget(w)
        return id
        
    def removeWidget(self, w):
        id = self.widgetStack.id(w)
        button = self.buttonGroup.find(id)
        self.buttonGroup.remove(button)
        button.reparent(None, QPoint(0,0))
        w.reparent(None, QPoint(0,0))
        self.n_widgets -= 1
        return self.widgetStack.removeWidget(w)
        
    def widget(self, id):
        return self.widgetStack.widget(id)
        
    def id(self, widget):
        return self.widgetStack.id(widget)
        
    def findButton(self, w):
        id = self.id(w)
        return self.buttonGroup.find(id)
        
    def visibleWidget(self):
        return self.widgetStack.visibleWidget()
        
    def raiseWidget(self, a0):
        """ a0 can be an int or a widget. """
        if isinstance(a0, int):
            widget = self.widget(a0)
            button = self.findButton(widget)
        elif isinstance(a0, QWidget):
            widget = a0
            button = self.findButton(widget)
        else:
            raise ValueError('no such widget on the WidgetStack')
        button.setOn(1)
        return self.widgetStack.raiseWidget(a0)
        
    def numWidgets(self):
        """ Return the number of widgets added with 'addWidget()' """
        return self.n_widgets
        
    
if __name__ == "__main__":
    a = QApplication([])
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    
    #w = CollapsableBuddy()
    #c = Collapsable(w)
    #c.show()
    #c.SetUncollapsedSize(QSize(200,200))
    #w.setText("Widgets.PushButton")    
    w = Knob()
    
    w.show()
    a.setMainWidget(w)
    a.exec_loop()
