""" A widget that fades out the foregroundColor
TODO:
- Get childeren to fade out to their respective colors without the childeren()
  hack
"""


from qt import *

FADE_DELTA = .1
FADE_INTERVAL_MS = 50


class Fadeable(QWidget):
    
    def __init__(self, parent=None, name=None, f=0):
        QWidget.__init__(self, parent, name, f)
        self.gradient = []
        self.gradient_i = 0
        self.fadeDirection = "in"
        self.fadeTimer = QTimer(self)
        QObject.connect(self.fadeTimer, SIGNAL('timeout()'),
                        self.doFade)
        self.fadeColor = QColor()
        self.fadeCallback = None
        self.flashFading = False

    def setColor(self, c):
        self.fadeColor = c
        if self.fadeDirection == 'in':
            self.setPaletteForegroundColor(c)

    def fadeIn(self, callback=None):
        self.fadeDirection = 'in'
        self.fadeCallback = callback
        self.gradient = Fadeable.getGradient(self.paletteBackgroundColor(),
                                             self.fadeColor)
        self.gradient_i = 0
        self.doFade()
        self.fadeTimer.start(FADE_INTERVAL_MS)
                
    def fadeOut(self, callback=None):
        self.fadeDirection = 'out'
        self.fadeCallback = callback
        self.gradient = Fadeable.getGradient(self.fadeColor,
                                             self.paletteBackgroundColor())
        self.gradient_i = 0
        self.doFade()
        self.fadeTimer.start(FADE_INTERVAL_MS)

    def flashFade(self):
        self.flashFading = True
        if self.fadeDirection == 'in':
            self.fadeOut()
        else:
            self.fadeIn()
        self.fadeOut()

        
    def stopFlashFade(self):
        """ Stop flashing with a fade in. """
        self.flashFading = False
        self.fadeIn()

    def doFade(self):
        try:
            c = self.gradient[self.gradient_i]
            self.setPaletteForegroundColor(c)
            self.gradient_i += 1
            # done
            if self.gradient_i >= len(self.gradient):
                if self.flashFading:
                    if self.fadeDirection == 'in':
                        self.fadeOut()
                    else:
                        self.fadeIn()
                else:
                    self.fadeTimer.killTimers()
                    self.gradient_i = 0
                    self.gradient = []
                    if self.fadeCallback:
                        self.fadeCallback()
        except:
            self.fadeTimer.killTimers()
            raise
        
    def getGradient(c1, c2):
        """ Return a list of QColor objects between c1 and c2. """
        o_red = c1.red()
        o_green = c1.green()
        o_blue = c1.blue()
        n_red = c2.red()
        n_green = c2.green()
        n_blue = c2.blue()
        rd = (n_red - o_red) * FADE_DELTA
        gd = (n_green - o_green) * FADE_DELTA
        bd = (n_blue - o_blue) * FADE_DELTA
        r,g,b, = o_red, o_green, o_blue
        
        ret = []
        for i in range(10):
            r = int(r + rd)
            g = int(g + gd)
            b = int(b + bd)
            # validate
            if o_red < n_red and r > n_red: r = n_red
            elif o_red > n_red and r < n_red: r = n_red
            if o_green < n_green and g > n_green: g = n_green
            elif o_green > n_green and g < n_green: g = n_green
            if o_blue < n_blue and b > n_blue: b = n_blue
            elif o_blue > n_blue and b < n_blue: b = n_blue
            c = QColor(int(r),int(g),int(b))
            ret.append(c)
        ret.append(c2)
        return ret
    getGradient = staticmethod(getGradient)



def test_Fadeable():
    a = QApplication([])
    class W(Fadeable):
        def mouseReleaseEvent(self, e):
            if self.fadeDirection == 'in':
                self.fadeOut()
            else:
                self.fadeIn()
    class F(Fadeable):
        def paintEvent(self, e):
            p = QPainter(self)
            p.drawRect(0, 0, self.width(), self.height())
            Fadeable.paintEvent(self, e)
    w = W()
    f = F(w)
    f.setGeometry(100, 100, 100, 100)
    w.show()
    a.setMainWidget(w)
    a.exec_loop()
