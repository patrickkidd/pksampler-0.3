""" Animation.py: animates widgets. """

from qt import *

UPDATE_INTERVAL = 100
ANIM_PIXELS = 100


class Animation(QObject):
    """ An animated reparent from one widget to another. 
        The widget is moved as a seperate window.
        SIGNALS:
            PYSIGNAL("done"), (self, widget)
    """
    
    objects = []
    
    def animate(widget, destWidget, destPoint=QPoint(0,0), sizeAdjust=False, doneFunc=None):
        """ Run an animation, delete the animation object afterwards. """
        obj = Animation(widget, destWidget, destPoint, sizeAdjust)
        Animation.objects.append(obj)
        QObject.connect(obj, PYSIGNAL("done"), Animation._animdone)
        if doneFunc:
            QObject.connect(obj, PYSIGNAL("done"), doneFunc)
            obj.doneFunc = doneFunc
        obj.start()
    animate = staticmethod(animate)
    
    def _animdone(obj):
        """ Private static method to delete the animation object after it is done. """
        Animation.objects.remove(obj)
        QObject.disconnect(obj, PYSIGNAL("done"), Animation._animdone)
        if hasattr(obj, "doneFunc"):
            QObject.disconnect(obj, PYSIGNAL("done"), obj.doneFunc)
    _animdone = staticmethod(_animdone)
        
    def __init__(self, widget, destWidget, destPoint=QPoint(0,0), sizeAdjust=False):
        """ widget is the widget to move,
            destWidget is the widget to animate to,
            destPoint is the point on destWidget to animate to,
            sizeAdjust is...I can't remember.
            
            SIGNALS:
                PYSIGNAL("done"), (widget,)
        """
        QObject.__init__(self)
        self.widget = widget
        self.destWidget = destWidget
        self.destPoint = destPoint
        self.dropSeq = []
        self.dropSizeSeq = []
        self.sizeAdjust = sizeAdjust
        
    def start(self):
        """ start the animation. """
        self.animDone = False
        
        # calculate points, anim data
        self.origPoint = self.widget.mapToGlobal(QPoint(0,0))
        animDestPoint = self.destWidget.mapToGlobal(self.destPoint)

        # find the height, width diff and divide into segments
        self.dropSeq = []
        
        x = self.origPoint.x()
        y = self.origPoint.y()
        
        finished = False
        while not finished:
        
            if self.origPoint.x() > animDestPoint.x():
                x = x - ANIM_PIXELS
                if x < animDestPoint.x():
                    x = animDestPoint.x()
            else:
                x = x + ANIM_PIXELS
                if x > animDestPoint.x():
                    x = animDestPoint.x()
                
            if self.origPoint.y() > animDestPoint.y():
                y = y - ANIM_PIXELS
                if y < animDestPoint.y():
                    y = animDestPoint.y()
            else:
                y = y + ANIM_PIXELS
                if y > animDestPoint.y():
                    y = animDestPoint.y()
            
            self.dropSeq.append(QPoint(x,y))
            if x == animDestPoint.x() and y == animDestPoint.y():
                finished = True
            if self.sizeAdjust:
                factor = (1.0 * i) / ANIM_FRAMES
                x = factor * self.widget.width()
                y = factor * self.widget.height()
                self.dropSizeSeq.append([x,y])
        self.dropSizeSeq.reverse()
        
        self.widget.reparent(None, self.origPoint)
        self.widget.show()
        self.widget.raiseW()
        self.dropIndex = 0
        self.timerEvent(None)
        self.startTimer(UPDATE_INTERVAL)
        
    def timerEvent(self, e):
        """ One click of animation. """
        if self.dropIndex < len(self.dropSeq):
            # animate
            i = self.dropIndex
            self.widget.move(self.dropSeq[i])
            if len(self.dropSizeSeq) > i:
                self.widget.resize(self.dropSizeSeq[i][0], self.dropSizeSeq[i][1])
            self.dropIndex += 1
        else:
            # done
            self.killTimers()
            self.dropIndex = 0
            self.dropSeq = []
            self.dropSizeSeq = []
            self.animDone = True
            self.widget.reparent(self.destWidget, self.destPoint, True)
            self.emit(PYSIGNAL("done"), (self, self.widget))
                
    def done(self):
        return animDone
    

    
def test_Animation():

    class TestWidget(QWidget):
        def __init__(self, dest, parent=None, name='', f=0):
            QWidget.__init__(self, parent, name, f)
            self.setPaletteBackgroundColor(QColor('red'))
            self.orig = parent
            self.dest = dest
            
        def mouseReleaseEvent(self, e):
            self.animation = Animation(self, self.dest)
            self.animation.start()
            self.orig, self.dest = (self.dest, self.orig)
        
    a = QApplication([])
    w1 = QWidget(None, 'w1')
    w2 = QWidget(None, 'w2')
    w1.setGeometry(10,10,75,75)
    w2.setGeometry(150, 10, 75, 75)
    tw = TestWidget(w2, w1)
    a.setMainWidget(w1)
    w1.show()
    w2.show()
    a.exec_loop()
    
    
def test_static_Animation():
    def doneFunc(obj, widget):
        print "doneFunc",widget
    class TestWidget(QWidget):
        def __init__(self, dest, parent=None, name='', f=0):
            QWidget.__init__(self, parent, name, f)
            self.setPaletteBackgroundColor(QColor('red'))
            self.orig = parent
            self.dest = dest
            
        def mouseReleaseEvent(self, e):
            Animation.animate(self, self.dest, doneFunc=doneFunc)
            self.orig, self.dest = (self.dest, self.orig)
        
    a = QApplication([])
    w1 = QWidget(None, 'w1')
    w2 = QWidget(None, 'w2')
    w1.setGeometry(10,10,75,75)
    w2.setGeometry(150, 10, 75, 75)
    tw = TestWidget(w2, w1)
    a.setMainWidget(w1)
    w1.show()
    w2.show()
    a.exec_loop()
    
if __name__ == "__main__":
    test_static_Animation()
    
