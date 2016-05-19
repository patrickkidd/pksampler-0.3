#!/bin/env python
""" Very specialized widgets that use povray-generateed pixmaps. """

import os
import os.path
import sys
from qt import *
import Globals
import Widgets

    
class Knob(QSlider, Widgets.PixmapRangeControl):
    def __init__(self, imagename, parent=None, name=None):
        QSlider.__init__(self, parent, name)
        Widgets.PixmapRangeControl.__init__(self, imagename, Qt.Vertical)
        #self.SetMask(109, 67, 54, 53)
        self.setFixedSize(54, 53)
        self.setRange(0,127)
        self.step = 1
        self.pageStep = 10
        self.lastPosition = 0
        self.position = 0
        self.buttonPressed = 0
        self.lastY = 0
        self.lastX = 0
        self.setRange(0,127)
        self.setValue(0)
        self.setPixmap(0)
        
    #def setValue(self, v):
    #    Widgets.PixmapRangeControl.setValue(self, 127 - v)
    #    self.position = v
    #    #self.repaint()
        
    def mousePressEvent(self, e):
        #Globals.qApp.palette().color(QPalette.Active, QColorGroup.Dark)
        if e.button() == Qt.LeftButton:
        
            self.buttonPressed = 1
            self.lastY = e.y()
            self.lastX = e.x()
    
            # Reposition - we need to sum the relative positions up to the
            # topLevel or dialog to please move().
            par = self.parentWidget()
            totalPos = self.pos()
    
            if par:
                while par.parentWidget() and not par.isTopLevel() and par.isDialog():
                    totalPos = totalPos + par.pos()
                    par = par.parentWidget()
        
        # reset to center position
        elif e.button() == Qt.RightButton:
            self.position = (self.maxValue() + self.minValue()) / 2.0
            self.update()
            self.emit(PYSIGNAL("valueChanged"), (self.position, None))
            
    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.buttonPressed = 0
            self.lastY = 0
            self.lastX = 0
                
    def mouseMoveEvent(self, e):
        if self.buttonPressed:
            # Dragging by x or y axis when clicked modifies value
            newValue = self.position + (self.lastY - float(e.y()) + float(e.x()) - self.lastX) * self.step
    
            if newValue > self.maxValue():
                self.position = self.maxValue()
            else:
                if newValue < self.minValue():
                    self.position = self.minValue()
                else:
                    self.position = newValue
    
            # don't update if there's nothing to update
            if self.lastPosition == self.position: 
                return
    
            self.setValue(self.position)
            #print self.position
            self.lastY = e.y()
            self.lastX = e.x()
    
            self.update()
    
            self.emit(PYSIGNAL("valueChanged"), (self.position, None))

    def wheelEvent(self, e):
        if e.delta() > 0:
            self.position -= self.pageStep
        else:
            self.position += self.pageStep
    
        if self.position > self.maxValue():
            self.position = self.maxValue()
    
        if self.position < self.minValue():
            self.position = self.minValue()
    
        self.drawPosition()
    
        # Reposition - we need to sum the relative positions up to the
        # topLevel or dialog to please move().
        par = self.parentWidget()
        totalPos = self.pos()
    
        while par.parentWidget() and not par.isTopLevel() and not par.isDialog():
            totalPos += par.pos()
            par = par.parentWidget()
    
        # set it to show for a timeout value
        self.emit(PYSIGNAL("valueChanged"), (self.position, None))
        
    
        

class MixerSlider(QSlider, Widgets.PixmapRangeControl):
    """ This widget totally rocks """
    
    def __init__(self, imagename, parent=None, name=None, f=0):
        QSlider.__init__(self, parent, name)
        Widgets.PixmapRangeControl.__init__(self, imagename, Qt.Vertical)
        #self.SetMask(120, 14, 30, 173)
        self.setFixedSize(30,170)
        self.setRange(0,127)
        self.setSteps(1,5)
        self.setInversePixmaps(1)
        self.setValue(0)

            
            
class SearchSlider(QSlider, Widgets.PixmapRangeControl):
    """ This widget rocks too """
    def __init__(self, parent=None, name=None):
        QSlider.__init__(self, parent, name)
        Widgets.PixmapRangeControl.__init__(self, 'search_slider', Qt.Horizontal)
        #self.SetMask(47, 90, 172, 23)
        self.setFixedSize(172, 23)
        self.setRange(0,127)
        self.setValue(0)
        self.setPixmap(0)
        self.setL33t(True)
        
    def mouseMoveEvent(self, e):
        pass
        
        
class LEDDigit(QWidget, Widgets.PixmapWidget):
    def __init__(self, parent=None, name=None, f=0):
        QWidget.__init__(self, parent, name, f)
        Widgets.PixmapWidget.__init__(self, 'leddigit')
        #self.SetMask(124, 87, 23, 32)
        self.setFixedSize(23,32)
        self.setEnabled(0)
        self.value = 10
        self.setValue(10)
    
    def setValue(self, v):
        if v == '-':
            v == 11
        if v < 0:
            v = 0
        elif v > 11:
            v = 11
            
        if v >= len(self.pixmaps) or v < 0:
            sys.stdout.write('PixmapSlider: no pixmap for value '+str(v)+'\n')
        else:
            self.setPixmap(v)
            
        self.value = v
    
        
class LEDDigitDisplay(QWidget):
    """ A Widget that displays multiple LED's """
    def __init__(self, n_digits=3, parent=None, name=None, f=0):
        QWidget.__init__(self, parent, name, f)
        
        self.digits = []
        for i in range(n_digits):
            d = LEDDigit(self)
            self.digits.append(d)
        self.Rearrange()
        self.digits.reverse()
        self.just = 'right'
        self.default = 10
        
    def justify(self, jstr):
        self.just = jstr

    def Rearrange(self):
        margin = 0
        digit_width = 19
        n_digits = len(self.digits)
        for i in range(n_digits):
            self.digits[i].move(i * digit_width-i, margin)
        
        self.resize(n_digits * digit_width, 
                    self.digits[0].height())
                    
    def setDefaultDigit(self, i):
        self.default = i
    
    def setValue(self, v, index=None):
        """ Set the value as an integer, the digits will be parsed. """
        
        if isinstance(v, float):
            try:
                v = int(v)
            except ValueError, e:
                print ValueError, e
        if index == None:
            
            # 'turn off'
            if v < 0:
                for d in self.digits:
                    d.setValue(10)

            # parse and set the value
            else:
                l = list(str(v))
                for d in self.digits: # default the digits
                    d.setValue(self.default)
                l.reverse()
                for i, c in enumerate(l):
                    if self.just == 'left':
                        i = len(self.digits)-i-1
                    self.setValue(int(c), i)

        else:
            if index < len(self.digits):
                self.digits[index].setValue(v)
            else:
                Globals.PrintErr('LED: invalid index: '+str(index)+', only have '+str(len(self.digits))+' digits.')
    
            
    def setOn(self, a0):
        """ Turn the display on or off. """
        self.setValue(-1)
        # set the last one to '0'
        if not a0:
            self.digits[len(self.digits)-1:].setValue(0)
                
                
    def numDigits(self):
        return len(self.digits)

            
class LED(QWidget, Widgets.PixmapWidget):
    """ A glowing/flashing LED widget.
        Constructor colors:
            'green', 'red', 'blue'
    """
    
    flashDimRate_MS = 70
    
    def __init__(self, imagename, color='green', parent=None, name=None, f=0):
        QWidget.__init__(self, parent, name, f)
        Widgets.PixmapWidget.__init__(self, imagename)
        
        self.on = 0
        self.dimIndex = 0
        self.isFlashing = 0
        #self.dimSeq = [1.0,1.0,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.0]
        self.dimSeq = [1.0,0.9,0.5,0.3]
        self.colorOffset = 0.0
        self.setColor(color)
            
        self.flashDimTimer = QTimer(self)
        QObject.connect(self.flashDimTimer, SIGNAL("timeout()"), self.slotDimTimer)
        
        self.flashFlashTimer = QTimer(self)
        QObject.connect(self.flashFlashTimer, SIGNAL("timeout()"), self.slotFlashTimer)
        
        self.setFixedSize(28,28)
        #self.SetMask(121, 87, 28, 28)
        self.setPixmap(0)
        
    def setPixmap(self, value):
        value = str(value).zfill(2)
        # a little float/int index fix...
        value = float(value)
        Widgets.PixmapWidget.setPixmap(self, value)
        
    def setColor(self, color):
        if color == 'green':
            self.colorOffset = 0.0
        elif color == 'red':
            self.colorOffset = 1.0
        elif color == 'blue':
            self.colorOffset = 2.0
        else:
            self.colorOffset = 0.0

##~     def mouseReleaseEvent(self, e):
##~         if self.isFlashing:
##~             self.stopFlashing()
##~         else:
##~             self.startFlashing()
        
    def setOn(self, a0=0):
        self.stopFlashing()
        self.on = a0
        i = 1.0 + self.colorOffset
        self.setPixmap(i)
        
    def Toggle(self):
        self.setOn(not self.on)
        
    def flashOnce(self):
        self.slotFlashTimer()
        
    def startFlashing(self, msecs=750):
        self.stopFlashing()
        self.isFlashing = 1
        self.slotFlashTimer()
        self.flashFlashTimer.start(msecs)
        
    def stopFlashing(self):
        self.flashFlashTimer.stop()
        self.isFlashing = 0
        self.setPixmap(self.colorOffset)
        
    def slotFlashTimer(self):
        """ flash the bulb once. """
        self.flashDimTimer.stop()
        self.dimIndex = 0
        self.slotDimTimer()
        self.flashDimTimer.start(LED.flashDimRate_MS)
        
    def slotDimTimer(self):
        """ do all of the animating based on the flash sequence. """
        if self.dimIndex < len(self.dimSeq):
            if self.dimSeq[self.dimIndex] == 0.0:
                key = self.dimSeq[self.dimIndex]
            else:
                key = self.dimSeq[self.dimIndex] + self.colorOffset
            self.setPixmap(key)
            self.dimIndex += 1
        else:
            self.flashDimTimer.stop()
            
        
class PushButton(Widgets.PixmapButton):
    def __init__(self, imagename, color='red', parent=None, name=None):
        Widgets.PixmapButton.__init__(self, imagename, color, parent, name)
        #self.SetMask(109,86,50,32)
        self.setFixedSize(50, 30)
        
    def setOn(self, a0):
        if self.isToggleButton() and a0:
            self.AnimatePress()
        Widgets.PixmapButton.setOn(self, a0)
        
        
class TapButton(Widgets.PixmapButton):
    def __init__(self, imagename, color='red', parent=None, name=None):
        Widgets.PixmapButton.__init__(self, imagename, color, parent, name)
        #self.SetMask(108,85,52,50)
        self.setFixedSize(52, 50)
        
        
displayTimer = Globals.DisplayTimer()
class PeakModule(QSlider, Widgets.PixmapRangeControl):
    """ A Peak Meter """
    def __init__(self, imagename, update_method, parent=None, name=None):
        QSlider.__init__(self, parent, name)
        Widgets.PixmapRangeControl.__init__(self, imagename, Qt.Vertical)
        #self.SetMask(129, 13, 8, 167)
        self.setFixedSize(8,167)
        self.update_method = update_method
        self.setAnimated(0)
        self.setRange(0,127)
        self.setPixmap(0)
        
    def mousePressEvent(self, e):
        pass
    def mouseReleaseEvent(self, e):
        pass
    def mouseMoveEvent(self, e):
        pass
        
    def start(self):
        global displayTimer
        displayTimer.register(self)
        
    def stop(self):
        displayTimer.deregister(self)
        self.setValue(0)
        
    def updateDisplay(self):
        v1 = abs(self.update_method())
        v2 = int((v1 / 32768.0) * 127)
        self.setValue(v2)
        

class WidgetStack(Widgets.WidgetStack):

    def __init__(self, parent=None, name='', f=0):
        Widgets.WidgetStack.__init__(self, parent, name, f)
        
    def addWidget(self, w, id=-1, button=None):
        if button == None:
            button = PushButton('button', 'red', self.buttonGroup)
        Widgets.WidgetStack.addWidget(self, w, id, button)



class VerticalJogWheel(QSlider, Widgets.PixmapRangeControl):
    """ works like a range control, but emits value deltas.
        SINGALS:
            PYSIGNAL('moved', (delta,))
    """

    def __init__(self, imagename, parent=None, name=None, f=0):
        QSlider.__init__(self, parent, name)
        Widgets.PixmapRangeControl.__init__(self, imagename, Qt.Vertical)
        #self.SetMask(119, 44, 36, 112)
        self.setFixedSize(36, 112)
        self.setRange(0,23)
        self.setSteps(1,5)
        self.setInversePixmaps(1)
        self.setPixmap(0)
        self.update()
        
        self.pixmapIndex = 0
        self.pressed = None 
        
    def paintEvent(self, e):
        """ Don't draw that bloody stuff. """
        pass
        
    def mousePressEvent(self, e):
        self.pressed = 1
        self.last_y = None
        
    def mouseReleaseEvent(self, e):
        self.pressed = None
        self.last_y = None
        
    def mouseMoveEvent(self, e):
        """ Just take the differences """
        if self.pressed:
            self.pressed = 1
            
            # first move since press
            if self.last_y == None:
                self.last_y = e.y()
            
            # do the move
            else:
                delta = self.last_y - e.y()
                delta /= 2
                if delta == 0: # comeon...gimme at least one..
                    delta = 1
                self.emit(PYSIGNAL('moved'), (delta, ))
                self.last_y = e.y()
                
                # advance the pixmap index
                if self.pixmapIndex + delta > self.maxValue():
                    self.pixmapIndex = (self.pixmapIndex + delta) - self.maxValue()
                    
                # loop down
                elif self.pixmapIndex + delta < 0:
                    self.pixmapIndex = self.maxValue() + (self.pixmapIndex + delta)
                    
                # just advance the pointer
                else:
                    self.pixmapIndex += delta
                    
                # This range control is inversed, and there is no zero index,
                # so advance it over the max value
                if self.pixmapIndex == self.maxValue():
                    self.pixmapIndex = 0

                self.setPixmap(self.pixmapIndex)
                
        
    def setValue(self, new_val):
        """ This shouldn't do anything, as we don't store values. """
        pass

    
    
if __name__ == "__main__": 

    def p(i):
        return
        print i
    a = QApplication([])
    w = MixerSlider('mixerslider')
    b = QPushButton('quit', None)
    QObject.connect(w, SIGNAL('valueChanged(int)'), p)
    QObject.connect(b, SIGNAL('clicked()'), a.quit)
    b.show()

    w.show()
    w.resize(50,50)
    a.setMainWidget(b)
    a.exec_loop()
