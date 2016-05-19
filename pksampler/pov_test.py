from qt import *
from Globals import loadPixmap
from pov import embedded_pixmaps

a = QApplication([])
w = QWidget()
a.setMainWidget(w)
w.show()
w.setErasePixmap(embedded_pixmaps.loadPixmap('outer_peak_module069.bmp'))

a.exec_loop()

