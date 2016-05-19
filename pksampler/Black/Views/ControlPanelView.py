from qt import *

from Black.GUI.TabWindow import TabView
from Black.GUI.Part import Part
from Black.GUI.Common import VIEW_LAYOUT_SPACING


class TempoWidget(Part):
    def __init__(self, parent=None, name=None, f=0):
        Part.__init__(self, parent, name, f)

class ControlPanelView(TabView):
    def __init__(self, parent=None, name=None, f=0):
        TabView.__init__(self, parent, name, f)
        Layout = QHBoxLayout(self,
                             VIEW_LAYOUT_SPACING,
                             VIEW_LAYOUT_SPACING)
        
        self.tempoWidget = TempoWidget(self)
        Layout.add(self.tempoWidget)
        

