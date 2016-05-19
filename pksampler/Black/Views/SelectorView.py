
from qt import *
from Black.GUI import TabView, Button, Part
from Black.GUI import DirPart, FilePart
from Black.GUI.Common import VIEW_LAYOUT_SPACING


class SelectorView(TabView):
    def __init__(self, parent=None, name=None, f=0):
        TabView.__init__(self, parent, name, f)
        Layout = QHBoxLayout(self)
        Layout.setSpacing(VIEW_LAYOUT_SPACING)
        Layout.setMargin(VIEW_LAYOUT_SPACING)
        
        self.dirPart = DirPart(self)
        QObject.connect(self.dirPart, PYSIGNAL('selected'), self.slotDir)
        Layout.add(self.dirPart)
        
        self.filePart = FilePart(self)
        QObject.connect(self.filePart, PYSIGNAL('selected'), self.slotFile)
        Layout.add(self.filePart)

        self.setSizePolicy(QSizePolicy.Expanding, 
                           QSizePolicy.Expanding)

    def slotFile(self, path):
        self.emit(PYSIGNAL('selected'), (path,))
        
    def slotDir(self, path):
        self.filePart.setPath(path)

    def addPath(self, p):
        self.filePart.setPath(p) # TODO: remove this!
        self.dirPart.addRoot(p)

def test_SelectorView():
    def p(path):
        print path
    a = QApplication([])
    w = SelectorView()
    w.addPath('/home/ajole/wav')
    w.show()
    w.resize(700,700)
    QObject.connect(w, PYSIGNAL('selected'), p)
    a.setMainWidget(w)
    a.exec_loop()
    

