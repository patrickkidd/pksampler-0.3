"""
TODO:
  - Maybe create a 'View' subclass or something (_getPart, etc...)?
  - Read the directories when a dir Item is opened, not when its parent is opened.
"""



import os, os.path
from qt import *
from Black.GUI import Part
from Common import FONT, WidgetCache
from Button import Button
import Globals

FILE_COLOR = QColor('orange')
DIR_COLOR = QColor('blue')
ITEM_SIZE = QSize(190, 50)
DIR_X_OFFSET = 25


        
class Item(Button):
    def __init__(self, parent=None, name=None):
        Button.__init__(self, parent, name)
        self.setFixedSize(ITEM_SIZE)
        
    def setPath(self, p):
        self.path = p
        bn = os.path.basename(self.path)
        i = bn.rfind('.')
        if i > 0:
            bn = bn[:i]
        self.setText(bn)

    def getPath(self):
        return self.path


## FILE PART

class FilePart(Part):
    """ PYSIGNAL('selected'), (path,) """
    
    MARGIN = 10

    def __init__(self, parent=None, name=None, f=0):
        Part.__init__(self, parent, name, f)
        self.cache = WidgetCache(Item, self)
        self.shown = []
        self.parts = [] # connected parts
        self.path = ''
        
    def resizeEvent(self, e):
        self.rearrange()
        Part.resizeEvent(self, e)

    def slotSelected(self, f):
        self.emit(PYSIGNAL('selected'), (f.getPath(),))

    def _getPart(self):
        f = self.cache.get()
        if not f in self.parts:
            f.setColor(FILE_COLOR)
            QObject.connect(f, PYSIGNAL('clicked'), self.slotSelected)
            self.parts.append(f)
        return f

    def setPath(self, p):
        """ Populate the view with files in a path
            An empty string will clear the view.
        """
        # clear
        for f in self.shown:
            f.hide()
            self.cache.put(f)
        self.shown = []

        # populate
        if os.path.isdir(p):
            for fn in os.listdir(p):
                fp = os.path.join(p,fn)
                if os.path.isfile(fp) and Globals.file_supported(fp):
                    f = self._getPart()
                    f.setPath(fp)
                    f.show()
                    self.shown.append(f)
        self.rearrange()

    def rearrange(self):
        y = 0
        x = FilePart.MARGIN
        for f in self.shown:
            f.move(x, y + FilePart.MARGIN)
            y += f.height()
            if f.y() + f.height() * 2 > self.height() - FilePart.MARGIN:
                x += f.width() + FilePart.MARGIN
                y = 0


## DIR PART

class DirPart(Part):
    """ Only shows directories. """
    
    def __init__(self, parent=None, name=None, f=0):
        Part.__init__(self, parent, name, f)
        self.cache = WidgetCache(Item, self)
        self.shown = []
        self.items = [] # connected parts
        self.roots = {}
        self.selected = None
        self.lastSelectedPath = ''

    def getLastSelectedPath(self):
        return self.lastSelectedPath

    def _getPart(self):
        """ initialize the directories here. """
        d = self.cache.get()
        d.setColor(DIR_COLOR)
        d.setRoundCorners(False)
        d.setToggleButton(True)
        self.shown.append(d)
        d.kids = []
        QObject.connect(d, PYSIGNAL('toggled'), self.slotToggled)
        return d

    def addRoot(self, path):
        if not path in self.roots:
            item = self._getPart()
            item.setPath(path)
            self.roots[path] = item
            # tell it its childeren
            for fn in os.listdir(path):
                fp = os.path.join(path, fn)
                if os.path.isdir(fp) and \
                       not os.path.basename(fp).startswith('.'):
                    child = self._getPart()
                    child.setPath(fp)
                    child.hide()
                    item.kids.append(child)
        self.rearrange()

    def _arrangeDirItem(self, item, y):
        """ Arrange all the item's kids under item. """
        if item.isOn():
            for child in item.kids:
                child.move(item.x() + DIR_X_OFFSET, y)
                y += child.height()
                child.show()
                if child.isOn():
                    y = self._arrangeDirItem(child, y)
        return y
        
    def rearrange(self):
        y = 15
        for path, item in self.roots.items():
            item.move(15, y)
            y = item.y() + item.height()
            y = self._arrangeDirItem(item, y)
                
    def slotToggled(self, item, on):
        """ Update a [shown] item. """
        self.lastSelectedPath = item.getPath()
        if on:
            path = item.getPath()
            # tell it its childeren
            for fn in os.listdir(path):
                fp = os.path.join(path, fn)
                if os.path.isdir(fp) and \
                       not os.path.basename(fp).startswith('.'):
                    nItem = self._getPart()
                    nItem.setPath(fp)
                    item.kids.append(nItem)
        else:
            for i in item.kids:
                i.hide()
                self.shown.remove(i)
                self.cache.put(item)
                item.kids = []
        self.rearrange()
        self.emit(PYSIGNAL('selected'), (self.lastSelectedPath, ))



def test_FilePart():
    def p(path):
        print path
    a = QApplication([])
    f = FilePart()
    f.setPath('/home/ajole/wav')
    f.show()
    QObject.connect(f, PYSIGNAL('selected'), p)
    a.setMainWidget(f)
    a.exec_loop()
    
    
def test_DirPart():
    def p(path):
        print path
    def fade():
        if w.fadeDirection == 'in':
            w.fadeOut()
        else:
            w.fadeIn()
    from Part import Part
    a = QApplication([])
    w = Part()
    w.resize(400,400)
    w.setPaletteBackgroundColor(QColor('black'))
    Layout = QVBoxLayout(w)
    d = DirPart(w)
    b = QPushButton('Fade me', w)
    d2 = DirPart(w)
    d2.addRoot('/home/ajole/wav')
    Layout.add(d)
    Layout.add(d2)
    Layout.add(b)
    b.show()
    QObject.connect(b, SIGNAL('clicked()'), fade)
    d.addRoot('/home/ajole/wav')
    w.show()
    QObject.connect(d, PYSIGNAL('selected'), p)
    a.setMainWidget(w)
    a.exec_loop()
    
