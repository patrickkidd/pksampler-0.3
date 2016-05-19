""" A button.
    TODO:
    - Get the filled-in circle when pressed to reflect the corner radius.
"""


from qt import *
from Part import Part

FLASH_INTERVAL_MS = 750

class Button(QLabel, Part):
    def __init__(self, parent=None, name=None):
        Part.__init__(self)
        QLabel.__init__(self, name, parent)
        self.setAlignment(Qt.AlignCenter)
        self.resize(100, 40)
        self.setText(name)
        
        self.flashTimer = QTimer(self)
        QObject.connect(self.flashTimer, SIGNAL('timeout()'),
                        self.slotFlash)
        self.flashOff = False
        self.toggleButton = False
        self.toggled = False
        self.down = False

    # FLASHING STUFF

    def startFlashing(self):
        self.flashTimer.start(FLASH_INTERVAL_MS)

    def stopFlashing(self):
        self.flashTimer.killTimers()
        self.flashOff = False

    def slotFlash(self):
        self.flashOff = not self.flashOff
        self.update()

    # BUTTON STUFF

    def setToggleButton(self, on):
        self.toggleButton = on

    def setOn(self, on):
        self.toggled = on
        self.update()
        
    def isOn(self):
        if self.toggleButton:
            return self.toggled
        else:
            return False
    
    def mousePressEvent(self, e):
        self.down = True
        self.update()
        
    def mouseReleaseEvent(self, e):
        self.down = False
        if self.toggleButton:
            self.toggled = not self.toggled
            self.emit(PYSIGNAL('toggled'), (self, self.toggled,))
        else:
            self.emit(PYSIGNAL('clicked'), (self,))
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        if not self.flashOff:
            # draw the inner color if down
            if (self.toggleButton and self.toggled) or self.down:
                p.setBrush(self.paletteForegroundColor().light(150))
                r = QRect(0, 0, self.width(), self.height())
                if self.getRoundCorners():
                    p.drawRoundRect(r)
                else:
                    p.drawRect(r)
                p.setBrush(Qt.NoBrush)
            Part.paintEvent(self, e)
        QLabel.drawContents(self, p)


def test_Button():
    a = QApplication([])
    w = QWidget()
    b = Button(w, 'a button')
    b.setToggleButton(True)
    b.setCornerRadius(15)
    b.setPaletteForegroundColor(QColor('blue'))
    b.resize(300,300)
    def p(on):
        print 'on',on
    QObject.connect(b, PYSIGNAL('toggled'), p)
    w.show()
    a.setMainWidget(w)
    a.exec_loop()

