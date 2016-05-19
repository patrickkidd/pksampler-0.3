print "***************************************"
print "               test1.py                "
print "***************************************"

from MainWindow import *
from Globals import *
import SampleWidget
import time


class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self, None, 'comeback')
        self.button1 = QPushButton(self, 'hideme')
        self.button1.setGeometry(0,0,100,20)
        self.button2 = QPushButton(self, 'closeme')
        self.button2.setGeometry(0,20,100,20)
        self.child = QWidget()
        self.shown = False
        QObject.connect(self.button1, SIGNAL("clicked()"),
                        self.slot)
        QObject.connect(self.button2, SIGNAL("clicked()"),
                        self.close)
    def slot(self):
        if self.shown:
            self.child.hide()
            self.shown = False
        else:
            self.child.show()
            self.shown = True


##~ PKAudio = Globals.getPKAudio().start_server()
##~ s = SampleWidget.SampleControl()
##~ s.load('/home/ajole/wav/Patrick Kidd - Birdman.wav')
##~ #s.sample.play()
##~ s.slotStart()
##~ s.slotSetZone(0,1)
##~ 
##~ time.sleep(100)

a = QApplication([])
PKAudio.start_server()
w = Widget()
a.setMainWidget(w)
w.show()

s = PKAudio.Sample('/home/ajole/wav/Patrick Kidd - Birdman.wav')
d = PKAudio.Driver()
d.getMixer().connect(s.outputPort())
s.play()

w.show()
a.exec_loop()
