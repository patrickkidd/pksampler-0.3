
import fpformat
from qt import *
from Part import Part
from Common import FONT, SMALL_CORNER_RADIUS
import Button

class ComboButton(Button.Button):
    def __init__(self, parent=None, name=None):
        Button.Button.__init__(self, parent, name)
        self.setRoundCorners(True)
        self.setCornerRadius(SMALL_CORNER_RADIUS)

class ComboBox(Part):
    """ PYSIGNAL('valueChanged'), (self, value)
    """
    def __init__(self, parent=None, name=None, f=0):
        Part.__init__(self, parent, name, f)
        self.setFixedSize(300, 75)

        Layout = QHBoxLayout(self)
        Layout.setSpacing(5)
        Layout.setMargin(10)

        self.label = QLabel(self)
        self.label.setText("140.0")
        self.label.setFont(FONT)
        self.label.setAlignment(Qt.AlignCenter)
        Layout.add(self.label)


        ButtonLayout = QGridLayout(None, 2, 2)
        ButtonLayout.setSpacing(2)
        
        self.upButton = ComboButton(self)
        QObject.connect(self.upButton, PYSIGNAL('clicked'),
                        self.slotUp)
        self.upButton.setText("+")
        ButtonLayout.addWidget(self.upButton, 0, 0)
        
        self.upCentButton = ComboButton(self)
        QObject.connect(self.upCentButton, PYSIGNAL('clicked'),
                        self.slotUpCent)
        self.upCentButton.setText("+ .1")
        ButtonLayout.addWidget(self.upCentButton, 0, 1)
        
        self.downButton = ComboButton(self)
        QObject.connect(self.downButton, PYSIGNAL('clicked'),
                        self.slotDown)
        self.downButton.setText("-")
        ButtonLayout.addWidget(self.downButton, 1, 0)
        
        self.downCentButton = ComboButton(self)
        QObject.connect(self.downCentButton, PYSIGNAL('clicked'),
                        self.slotDownCent)
        self.downCentButton.setText("- .1")
        ButtonLayout.addWidget(self.downCentButton, 1, 1)

        Layout.addLayout(ButtonLayout)

    def setValue(self, v):
        v = float(v)
        self.label.setText(fpformat.fix(v, 1))
        self.emit(PYSIGNAL('valueChanged'), (self, self.getValue()))

    def getValue(self):
        t = float(str(self.label.text()))
        return t

    def slotUp(self):
        self.setValue(self.getValue() + 1)
        
    def slotDown(self):
        self.setValue(self.getValue() - 1)
    
    def slotUpCent(self):
        self.setValue(self.getValue() + .1)

    def slotDownCent(self):
        self.setValue(self.getValue() - .1)
    

        
 
def test_ComboBox():
    def p(w, x):
        print 'valueChanged',x
    a = QApplication([])
    w = ComboBox()
    w.show()
    QObject.connect(w, PYSIGNAL('valueChanged'), p)
    a.setMainWidget(w)
    a.exec_loop()
