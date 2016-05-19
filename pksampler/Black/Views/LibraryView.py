
import os
from qt import *
from Black.GUI.TabWindow import TabView
from Black.GUI import Part
from Black.GUI import ComboBox, DirPart, Button
from Black.GUI.Common import VIEW_LAYOUT_SPACING
import Conf


class GroovePart(Part):
    def __init__(self, parent=None, name=None, f=0):
        Part.__init__(self, parent, name, f)


class NewGroovePart(Part):
    def __init__(self, parent=None, name=None, f=0):
        Part.__init__(self, parent, name, f)
        Layout = QVBoxLayout(self)
        Layout.setSpacing(VIEW_LAYOUT_SPACING)
        
        Layout.setAlignment(Qt.AlignHCenter)

        self.tempoComboBox = ComboBox(self)
        Layout.add(self.tempoComboBox)
        
        self.dirPart = DirPart(self)
        self.dirPart.addRoot(os.environ['HOME'])
        Layout.add(self.dirPart)

        self.addButton = Button(self)
        self.addButton.setText('Add Groove')
        self.addButton.setFixedHeight(50)
        QObject.connect(self.addButton, PYSIGNAL('clicked'),
                        self.slotAdd)
        Layout.add(self.addButton)

    def slotAdd(self):
        self.emit(PYSIGNAL('add'), ())
        # clear the box



class LibraryView(TabView):
    """ PYSIGNAL('grooveAdded'), (name, path, tempo)
    """
    def __init__(self, parent=None, name=None, f=0):
        TabView.__init__(self, parent, name, f)
        Layout = QHBoxLayout(self,
                             VIEW_LAYOUT_SPACING,
                             VIEW_LAYOUT_SPACING)

        self.groovePart = GroovePart(self, 'groovePart')
        Layout.add(self.groovePart)
        
        self.newGroovePart = NewGroovePart(self, 'newGroovepart')
        self.newGroovePart.setDrawBorder(False)
        self.newGroovePart.setSizePolicy(QSizePolicy.Minimum,
                                         QSizePolicy.Expanding)
        QObject.connect(self.newGroovePart, PYSIGNAL('add'),
                        self.slotAddGroove)
        Layout.add(self.newGroovePart)

    def _doFadeMe(self):
        if self.fadeDirection == 'in':
            self.fadeOut()
        else:
            self.fadeIn()

    def slotAddGroove(self):
        """ Called when the NewGroovePart's add button is clicked. """
        tempo = self.newGroovePart.tempoComboBox.getValue()
        path = self.newGroovePart.dirPart.getLastSelectedPath()
        name = os.path.basename(path)

        grooves = Conf.get('GROOVES')
        grooves = "%s:%s,%s,%i" % (grooves, name, path, tempo)
        Conf.set('GROOVES', grooves)
        self.emit(PYSIGNAL('grooveAdded'), (name, path, tempo))
        
        
def test_LibraryView():
    def p(name, path, tempo):
        print 'grooveAdded',name,path,tempo
    a = QApplication([])
    w = LibraryView(None, 'w')
    w.show()
    w.resize(700,700)
    QObject.connect(w, PYSIGNAL('grooveAdded'), p)
    a.setMainWidget(w)
    a.exec_loop()
    


def test_NewGroovePart():
    a = QApplication([])
    w = NewGroovePart()
    w.show()
    w.resize(400,400)
    a.setMainWidget(w)
    a.exec_loop()
    
