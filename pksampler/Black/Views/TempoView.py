from qt import *

from Black.GUI.TabWindow import TabView
from Black.GUI.Part import Part
from Black.GUI.Common import VIEW_LAYOUT_SPACING

class TempoPart(Part):
    """ A fmailiar tempo controller view. """
    def __init__(self, parent=None, name=None, f=0):
        Part.__init__(self, parent, name, f)

class TempoView(TabView):
    def __init__(self, parent=None, name=None, f=0):
        TabView.__init__(self, parent, name, f)
        Layout = QHBoxLayout(self,
                             VIEW_LAYOUT_SPACING,
                             VIEW_LAYOUT_SPACING)
        self.tempoPart = TempoPart(self)
        Layout.add(self.tempoPart)


def test_TempoPart():
    a = QApplication([])
    w = TempoPart()
    w.show()
    w.resize(400,400)
    a.setMainWidget(w)
    a.exec_loop()

    
def test_TempoView():
    a = QApplication([])
    w = TempoView()
    w.show()
    w.resize(400,400)
    a.setMainWidget(w)
    a.exec_loop()
