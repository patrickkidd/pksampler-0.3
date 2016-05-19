from qt import *

class W(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setPaletteForegroundColor(QColor('red'))
    def paintEvent(self, e):
        p = QPainter(self)
        p.drawLine(0, 0, self.width(), self.height())

a = QApplication([])
w = W()
w.show()
a.setMainWidget(w)
a.exec_loop()
