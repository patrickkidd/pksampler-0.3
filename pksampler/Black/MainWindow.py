""" MainWindow.py: the main module for the Black package. """

from qt import *
from GUI import Tab, TabWindow, TabView
from Views import *
from SampleControl import SampleControl
from GUI import TAB_WIDTH, TAB_HEIGHT


BASE_COLOR = QColor('blue')

class MainWindow(TabWindow):
    def __init__(self, parent=None, name=None, f=0):
        TabWindow.__init__(self, parent, name, f)
        self.setPaletteForegroundColor(BASE_COLOR)
        
        ## TOP SIDE
        
        self.sampleView = SampleView(self)
        self.addTab(Tab(Qt.AlignTop, self, 'Samples'),
                    self.sampleView)
                    
        ## LEFT SIDE

        self.tempoView = TempoView(self)
        self.addTab(Tab(Qt.AlignLeft, self, 'Tempo'),
                    self.tempoView)
        
        self.controlPanel = ControlPanelView(self)
        self.addTab(Tab(Qt.AlignLeft, self, 'Control\nPanel'),
                    self.controlPanel)

        ## RIGHT SIDE

        self.grooveSelector = SelectorView(self)
        QObject.connect(self.grooveSelector, PYSIGNAL('selected'),
                        self.slotGrooveSelected)
        t = Tab(Qt.AlignRight, self, 'Grooves')
        t.setColor(BASE_COLOR.light(150))
        self.addTab(t, self.grooveSelector)

        self.allSelector = SelectorView(self)
        self.allSelector.addPath('/home/ajole/wav')
        QObject.connect(self.allSelector, PYSIGNAL('selected'),
                        self.slotSampleSelected)
        self.samplesTab = Tab(Qt.AlignRight, self, 'All\nSamples')
        self.addTab(self.samplesTab, self.allSelector)

        self.libraryView = LibraryView(self)
        QObject.connect(self.libraryView, PYSIGNAL('selected'),
                        self.slotProfileSelected)
        self.libraryTab = Tab(Qt.AlignRight, self, 'Library')
        self.libraryTab.setColor(QColor('orange'))
        self.addTab(self.libraryTab, self.libraryView)
        
        
        ## BOTTOM SIDE

        self.hostsLabel = QLabel("Network\nHosts", self)
        self.hostsLabel.setAlignment(Qt.AlignCenter)
        self.hostsLabel.setFont(QFont('Helvetica', 12, QFont.Bold))
        self.hostsLabel.resize(TAB_WIDTH, TAB_HEIGHT)
        
        self.setPaletteForegroundColor(QColor('blue'))
        self.setFixedSize(1024,768)

    def resizeEvent(self, e):
        self.hostsLabel.move(TAB_WIDTH, self.height() - TAB_HEIGHT)
        TabWindow.resizeEvent(self, e)

    def slotSampleSelected(self, path):
        s = SampleControl()
        s.load(path)
        if s.isLoaded():
            self.sampleView.add(s)

    def slotProfileSelected(self, profile):
        pass

    def slotGrooveSelected(self, profile):
        pass


def main():
    import pkaudio
    pkaudio.start_server()
    pkaudio.load_module('pksample')
    pkaudio.load_module('pkmuter')
    pkaudio.load_module('pkeffect')
    pkaudio.load_module('pkpeakmodule')
    pkaudio.load_module('pksplitter')
    a = QApplication([])
    w = MainWindow()
    w.show()
    a.setMainWidget(w)
    a.exec_loop()
    

