from qt import *
from pksampler.pov import embedded_pixmaps

PIXMAP2 = "scene.png"

a = QApplication([])
w1 = QWidget()
w1.setCaption('from file')
p = QPixmap('scene.png')
w1.setErasePixmap(p)
w1.setFixedSize(p.width(), p.height())

w2 = QWidget()
w2.setCaption('embedded')
i = embedded_pixmaps.uic_findImage(PIXMAP2)
if i.isNull():
    raise "invalid pixmap:",PIXMAP2
p = QPixmap(i)
w2.setErasePixmap(p)
w2.show()
w2.setFixedSize(p.width(), p.height())

a.setMainWidget(w1)
w1.show()
a.exec_loop()

