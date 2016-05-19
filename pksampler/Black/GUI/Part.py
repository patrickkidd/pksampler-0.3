
from qt import QWidget, QColor, QPainter
from Fadeable import Fadeable

PART_CURVE_WIDTH = 50

class Part(Fadeable):
    """ A peice of the pie that has a round rectangle border. """
    def __init__(self, parent=None, name=None, f=0):
        Fadeable.__init__(self, parent, name, f)    
        self.color = QColor('blue')
        self.setColor(self.color)
        self.roundCorners = True
        self.drawBorder = True
        self.cornerRadius = PART_CURVE_WIDTH

    def setRoundCorners(self, on):
        self.roundCorners = on

    def getRoundCorners(self):
        return self.roundCorners

    def setDrawBorder(self, on):
        self.drawBorder = on

    def setCornerRadius(self, r):
        self.cornerRadius = r

    def getCornerRadius(self):
        return self.cornerRadius

    def setColor(self, c):
        self.color = QColor(c)
        self.setPaletteForegroundColor(self.color)
        Fadeable.setColor(self, self.color)
        self.update()

    def paintEvent(self, e):
        """ Draw the border. """
        if self.drawBorder:
            p = QPainter(self)
            if self.roundCorners:
                # draw quarter-circles for borders
                p.drawArc(0, 0, self.cornerRadius, self.cornerRadius, 1440, 1440)
                p.drawArc(0, self.height() - self.cornerRadius,
                          self.cornerRadius, self.cornerRadius, 2880, 1440)
                p.drawArc(self.width() - self.cornerRadius,
                          self.height() - self.cornerRadius,
                          self.cornerRadius, self.cornerRadius, 4320, 1440)
                p.drawArc(self.width() - self.cornerRadius,
                          0, self.cornerRadius, self.cornerRadius, 5760, 1440)
                corner = self.cornerRadius / 2
                p.drawLine(corner, 0, self.width() - corner, 0)
                p.drawLine(0, corner, 0, self.height() - corner)
                p.drawLine(corner, self.height()-1,
                           self.width() - corner, self.height()-1)
                p.drawLine(self.width()-1, corner, self.width()-1,
                           self.height() - corner)
            else:
                p.drawRect(0, 0, self.width(), self.height())
        QWidget.paintEvent(self, e)


def test_Part():
    def p():
        print 'fade done'
    class P(Part):
        def __init__(self):
            Part.__init__(self)
            self.setPaletteBackgroundColor(QColor('black'))
            self.setPaletteForegroundColor(QColor('white'))
        def mouseReleaseEvent(self, e):
            if self.fadeDirection == 'in':
                self.fadeOut(p)
            else:
                self.fadeIn(p)
            Part.mouseReleaseEvent(self, e)
    a = QApplication([])
    w = P()
    w.show()
    a.setMainWidget(w)
    a.exec_loop()

