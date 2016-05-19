""" SampleGroup.py: Visual and logical grouping of Samples. """

from qt import *
import PKAudio


FRAME_STYLE = QFrame.TabWidgetPanel | QFrame.Raised


class SampleGroup(QFrame):
    def __init__(self, parent=None, name='', f=0):
        QFrame.__init__(self, parent, name, f)
        self.setFrameStyle(FRAME_STYLE)
        self.scrollView = QScrollView(self)
        self.scrollView.setSizePolicy(QSizePolicy.Expanding,
                                      QSizePolicy.Expanding)
        self.scrollView.viewport().setPaletteBackgroundColor(QColor('white'))
        MainLayout = QHBoxLayout(self)
        MainLayout.addWidget(self.scrollView)
        
        Layout = QHBoxLayout(self.scrollView.viewport(), 
                             QBoxLayout.LeftToRight)
        Layout.setSpacing(10)
        spacer = QSpacerItem(10, 10, 
                             QSizePolicy.Expanding, 
                             QSizePolicy.Minimum)
        self.sampleLayout = QHBoxLayout(Layout)
        Layout.addItem(spacer)
        
    def add(self, sample):
        sample.hide()
        QObject.connect(sample, PYSIGNAL('delete'),
                        self.remove)
        sample.reparent(self.scrollView.viewport(), 
                        QPoint(0,0), True)
        self.sampleLayout.addWidget(sample)
        
    def remove(self, sample):
        if sample.parent() == self.scrollView.viewport():
            self.sampleLayout.remove(sample)
            sample.reparent(None, QPoint(0,0))


def main():
    import Sample
    a = QApplication([])
    PKAudio.start_server()
    w = SampleGroup()
    w.add(Sample.Sample())
    w.add(Sample.Sample())
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
    

if __name__ == "__main__":
    main()
