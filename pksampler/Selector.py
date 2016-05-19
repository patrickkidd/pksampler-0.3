#!/bin/env python
""" File,Directory/Stored Sample group view """

import os
from qt import *
import Globals
import Widgets

dirPixmap_closed = None
dirPixmap_open = None
filePixmap = None


groove_color = QColor(84, 84, 255)
file_color = QColor(255, 129, 50)
flash_interval = 50
container_gradient = 120
nameplate_gradient = 190
selectable_gradient = 150
bounce_padding = 0  # mouseMoveEvent fixer : msecs


def draw_dark_gradient(painter, delta, x1, x2, y1, y2):
    """ x2 must be greater than x1. """
    if not Widgets.use_gradients:
        return
    orig_color = QColor(painter.pen().color())
    diff = x2 - x1
    delta = diff / (delta - 100)
    tally = 100
    for i in range(diff):
        if not i % delta: tally += 1
        color = orig_color.dark(tally)
        painter.setPen(color)
        painter.drawLine(x1+i, y1, x1+i, y2)
    Globals.psyco_bind(draw_dark_gradient)

class SelectorItem(QLabel):
    """ An SelectorItem is expected to decide its own size, and
        use signals to notify the parent of the change.
        You might want to set the background color in the ctor.
        Subclasses should emit:
            PYSIGNAL('resized'), () -  after widget has new size
    """
    def __init__(self, parent=None, name=None, f=0):
        QLabel.__init__(self, parent, name, f)
        self.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.setLineWidth(1)
        if Globals.qVersion() >= 3:
            self.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.original_size = QSize(200,30)
        self.resize(self.original_size)

class SelectableItem(SelectorItem):
    """ An item that contains an id as a means of locating an object, 
        and emits a selected signal when clicked.
        The background color is drawn 15% lighter than the parent.
        self.path contains the path passed to the ctor.
        emits:
            PYSIGNAL('selected'), ()
    """
    
    num_flashes = 7 # number of times to flash when selected
    
    def __init__(self, id, parent=None, name=None, f=0):
        SelectorItem.__init__(self, parent, name, f)
        self.setFrameStyle(QFrame.NoFrame)
        self.setFixedSize(self.size())
        c = self.paletteBackgroundColor()
        self.setPaletteBackgroundColor(c.light(115))
        self.baseColor = self.paletteBackgroundColor()
        font = QFont()
        font.setBold(1)
        self.setFont(font)
        self.setText("  "+id)
        self.id = id
        self.flashTimer = QTimer(self)
        self.cur_flashes = 0
        QObject.connect(self.flashTimer, SIGNAL('timeout()'), self.flashEvent)
        
    def setPaletteBackgroundColor(self, color):
        """ Set the background color """
        self.baseColor = color
        SelectorItem.setPaletteBackgroundColor(self, color)
        
    def flashEvent(self):
        """ flash the timer"""
        if self.cur_flashes == SelectableItem.num_flashes:
            self.flashTimer.stop()
            self.cur_flashes = 0
            SelectorItem.setPaletteBackgroundColor(self, self.baseColor)
        elif self.cur_flashes % 2:
            SelectorItem.setPaletteBackgroundColor(self, self.baseColor)
        else:
            SelectorItem.setPaletteBackgroundColor(self, self.baseColor.light(200))
        self.cur_flashes += 1

    def mouseReleaseEvent(self, e):
        self.cur_flashes = 0
        self.flashEvent()
        if not self.flashTimer.isActive():
            self.flashTimer.start(flash_interval)
        self.emit(PYSIGNAL('selected'), (self.id, ))

    def paintEvent(self, e):
        painter = QPainter(self)
        color = self.paletteBackgroundColor().light(115)
        painter.setPen(color)
        painter.setBrush(color)
        rect = QRect(0,3,self.width(),self.height() - 6)
        painter.drawRoundRect(rect, 0, 0)
        draw_dark_gradient(painter, selectable_gradient, self.width() / 4, self.width(), 3, self.height()-4)
        QLabel.paintEvent(self, e)

        
class FileItem(SelectableItem):
    """ Draws a clickable file or dir widget. 
        emits: 
            PYSIGNAL('selected') (path, )
    """
    def __init__(self, path, parent=None, name=None, f=0):
        SelectableItem.__init__(self, path, parent, name, f)
        self.setText("  "+QFileInfo(path).baseName().ascii())

        
class ContainerItem(SelectorItem):
    """ Contains SelectableItems or other containers.
        Override 'openContainer' to update self.items, then call
        ContainerItem.openContainer()
        SIGNALS:
            PYSIGNAL('resized'), ()
    """
    
    class NamePlate(SelectorItem):
        """ Used by an open container to display the name and be a collapse button. 
            SIGNALS: 
                PYSIGNAL('clicked'), ()
        """
        def __init__(self, parent, name, f=0):
            SelectorItem.__init__(self, parent, name, f)
            self.setText("  "+name)
            
        def mouseReleaseEvent(self, e):
            if Globals.qVersion() >= 3:
                e.accept()
            self.emit(PYSIGNAL("clicked"), ())
            
        def paintEvent(self, e):
            painter = QPainter(self)
            painter.setPen(self.paletteBackgroundColor())
            draw_dark_gradient(painter, nameplate_gradient, self.width() / 4, self.width(),0, self.height())
            SelectorItem.paintEvent(self, e)
    
    def __init__(self, id, parent, name=None, f=0):
        SelectorItem.__init__(self, parent, name, f)
        
        self.id = id
        self.l_margin = 20
        self.opened = 0
        self.items = []
        self.frame_style = self.frameStyle()        
        self.setText("   " + id)

        self.namePlate = ContainerItem.NamePlate(self, id)
        c = self.paletteBackgroundColor()
        self.namePlate.setPaletteBackgroundColor(c.dark(150))
        self.namePlate.move(0,0)
        self.namePlate.hide()
        self.connect(self.namePlate, PYSIGNAL('clicked'), self.closeContainer)
        
    def mousePressEvent(self, e):
        # no ignore/accept in < qt < 3
        if Globals.qVersion() >= 3:
            e.accept()
    
    def mouseMoveEvent(self, e):
        # no ignore/accept in < qt < 3
        if Globals.qVersion() >= 3:
            e.ignore()
 
    def mouseReleaseEvent(self, e):
        # no ignore/accept in < qt < 3
        if Globals.qVersion() >= 3:
            e.accept()
        if e.x() > 0 and e.y() > 0 and e.x() < self.width() and e.y() < self.height():
            self.toggleOpen()
            
    def paintEvent(self, e):
        if not self.opened:
            painter = QPainter(self)
            painter.setPen(self.paletteBackgroundColor())
            draw_dark_gradient(painter, container_gradient, self.width() / 4, self.width(),0, self.height())
        SelectorItem.paintEvent(self, e)
        
    def repaint(self):
        for i in self.items:
            i.repaint()
        SelectorItem.repaint(self)
            
    def toggleOpen(self):
        if self.opened:
            self.closeContainer()
        else:
            self.openContainer()
        
    def closeContainer(self):
        # prevent the open/closing of dragging
        self.opened = 0
        self.setFrameStyle(self.frame_style)
        self.namePlate.hide()
        
        for item in self.items:
            item.reparent(None, QPoint(0,0))
            self.disconnect(item, PYSIGNAL('resized'), self.slotResize)
            self.disconnect(item, PYSIGNAL('selected'), self.slotResize)
            
        self.items = []
        self.resize(self.original_size)
        self.setText(self.namePlate.text())
        self.emit(PYSIGNAL('resized'), ())

    def openContainer(self):
        self.opened = 1
        # the nameplate is only used when the widget is expanded.
        self.namePlate.show()
        # avoid food-poisoning from bad leftovers
        self.setText("")
        self.frame_style = self.frame_style
        self.setFrameStyle(QFrame.NoFrame)
        self.slotResize()
        
    def update(self):
        print 'ContainerItem update'
    
    def removeItems(self):
        l = self.items
        for item in l:
            QObject.disconnect(item, PYSIGNAL('selected'), self.slotSelected)
            QObject.disconnect(item, PYSIGNAL('resized'), self.slotResize)
            self.items.remove(item)
            
    def items(self):
        """ return a list of the child items """
        return list(self.items)
        
    def slotResize(self):
        if not len(self.items):
            return

        height_tally = 0
        width = 0
        orig_height = self.original_size.height()
        
        for item in self.items:
            # arrange the widgets, add the height
            item.move(self.l_margin, height_tally + orig_height)
            height_tally += item.height()
            
            # store the largest width
            if item.width() > width:
                width = item.width()
            item.show()
        
        self.resize(width + self.l_margin, height_tally + orig_height)
        self.emit(PYSIGNAL('resized'), ())
        
    def slotSelected(self, path):
        self.emit(PYSIGNAL('selected'), (path, ))
        
        
class DirItem(ContainerItem):
    """ Self explainatory. """
    def __init__(self, path, parent=None, name=None, f=0):
        if path.endswith('/'):
            path = path[:len(path)-1]
        id = path[path.rfind('/')+1:]
        ContainerItem.__init__(self, id, parent, name, f)
        self.path = path
            
    def openContainer(self):
        dir = QDir(self.path)
        self.removeItems()
        fileItems = []
        for fi in dir.entryInfoList():
            item = None
            name = fi.fileName().ascii()
            
            if fi.isFile() and Globals.file_supported(fi.filePath()):
                item = FileItem(fi.filePath().ascii(), self)
                item.setPaletteBackgroundColor(file_color)
                fileItems.append(item)
                
            elif fi.isDir() and not name == '.' and not name == '..':
                item = DirItem(fi.filePath().ascii(), self)
                self.items.append(item)
                
            if item:
                item.show() # leave this!
                self.connect(item, PYSIGNAL('resized'), self.slotResize)
                self.connect(item, PYSIGNAL('selected'), self.slotSelected)
                
        # add file items after directories
        for fi in fileItems:
            self.items.append(fi)
        ContainerItem.openContainer(self)
        
        
class GrooveContainerItem(ContainerItem):
    def __init__(self, category, parent=None, name=None, f=0):
        ContainerItem.__init__(self, category, parent, name, f)
        
    def openContainer(self):
        self.removeItems()
        for category, id in Globals.get_grooves():
            if category == self.id:
                item = SelectableItem(id, self)
                item.setPaletteBackgroundColor(groove_color)
                QObject.connect(item, PYSIGNAL('selected'), self.slotSelected)
                QObject.connect(item, PYSIGNAL('resized'), self.slotResize)
                self.items.append(item)
        ContainerItem.openContainer(self)
        
    def slotSelected(self, name):
        id = self.id.strip(' ')
        ContainerItem.slotSelected(self, 'groove:'+self.id+','+name)
        
        
class Selector(QWidget):
    """ Arranges selectable directories. """
    
    def __init__(self, parent=None, name=None, f=0):    
        QWidget.__init__(self, parent, name, f)
        self.setPaletteBackgroundColor(self.paletteBackgroundColor().light(125))
        self.last_y = -1
        self.containerItems = {}
        c = self.paletteBackgroundColor()
        self.resize(self.size())
        
        self.moveTickTally = 0
        self.backplate = QWidget(self)
        self.processScrollEvent(0)
        self.initial_y_time = QTime()
    
    def addPath(self, path):
        """ Add a directory view. """
        if not path in self.containerItems and os.path.isdir(path):
            self.containerItems[path] = DirItem(path, self.backplate)
            #self.containerItems[path].move(2,2)
            self.connect(self.containerItems[path], PYSIGNAL('selected'),
                        self.slotSelected)
            self.connect(self.containerItems[path], PYSIGNAL('resized'),
                        self.slotResize)
            self.containerItems[path].show()
        self.rearrange()
                        
    def updateGrooveCategories(self):
        """ Re-add the category items. """
        # add the grooves
        for category, id in Globals.get_grooves():
            # add new categories
            if not category in self.containerItems:
                self.containerItems[category] = GrooveContainerItem(category, self.backplate)
                QObject.connect(self.containerItems[category], PYSIGNAL('selected'),
                                self.slotSelected)
                QObject.connect(self.containerItems[category], PYSIGNAL('resized'),
                                self.slotResize)
                self.containerItems[category].show()
        self.rearrange()
        
    def remove(self, id):
        """ Remove an item by id. """
        if id in self.containerItems:
            item = self.containerItems[id]
            del self.containerItems[id]
            self.disconnect(item, PYSIGNAL('selected'), self.slotSelected)
            self.disconnect(item, PYSIGNAL('resized'), self.slotResize)
            item.reparent(None, QPoint(0,0))
            item.hide()
        self.rearrange()
            
    def removeItem(self, item):
        """ Remove an item by reference. """
        for id in self.containerItems:
            if self.containerItems[id] == item:
                self.remove(id)
                return
    
    def openAll(self):
        for path in self.containerItems:
            self.containerItems[path].openContainer()
            
    def closeAll(self):
        for path in self.containerItems:
            self.containerItems[path].closeContainer()
            
    def rearrange(self):
        """ Set the backplate size, arrange the SelectorItems on it. """
        biggest_width = 0
        total_height = 0
        
        # sort the containers by type
        grooveContainers = []
        miscContainers = []
        for path in self.containerItems:
            c = self.containerItems[path]
            if c.__class__ == GrooveContainerItem:
                grooveContainers.append(c)
            else:
                miscContainers.append(c)
        
        # use this to order the containers
        groups = [miscContainers, grooveContainers]
        for g in groups:
            for c in g:
                c.move(0,total_height)
                total_height += c.height()
                if biggest_width < c.width():
                    biggest_width = c.width()
        
        self.backplate.resize(biggest_width, total_height)
        
        # set the scroll cursor if necessary
        if Globals.qVersion() >= 3:
            if total_height > self.height():
                self.setCursor(QCursor(Qt.SizeVerCursor))
            else:
                self.setCursor(QCursor(Qt.PointingHandCursor))
                
                
    def repaint(self):
        for item in self.containerItems:
            self.containerItems[item].repaint()
        QWidget.repaint(self)
        
    def processScrollEvent(self, e_y):
        """ Move the backplate according to mouse/wheel move event. """
            
        # only scroll if it is taller than self
        if self.backplate.height() > self.height():
            
            if self.last_y >= 0:
                delta = e_y - self.last_y
                new_y = self.backplate.y() + delta
                
                # keep backplate inside the bottom
                if new_y + self.backplate.height() < self.height():
                    new_y = self.height() - self.backplate.height()
                    
                # keep backplate inside the top
                elif new_y > 0:
                    new_y = 0
                
                self.last_y = e_y
                self.backplate.move(self.backplate.x(), new_y)
                
            else:
                self.last_y = e_y
            
        # if backplate fits in self, just move it to the origin
        else:
            self.backplate.move(2,2)
        
    def mouseReleaseEvent(self, e):
        self.last_y = -1
        self.moveTickTally = 0
        if Globals.qVersion() >= 3:
            e.accept()
                
    def mouseMoveEvent(self, e):
        """ Scroll/Drag the SelectorItems. """
        # first move in a while
        if self.last_y == -1:
            self.initial_y_time = QTime.currentTime()
            self.processScrollEvent(e.y())
        # test time against first move
        elif self.initial_y_time.addMSecs(bounce_padding) < QTime.currentTime():
            self.processScrollEvent(e.y())

            
        if Globals.qVersion() >= 3:
            e.accept()
        
    def wheelEvent(self, e):
        e.accept()
        self.last_y = 0
        self.processScrollEvent(e.delta() / 2)
        self.last_y = -1
        
    def slotSelected(self, path):
        self.emit(PYSIGNAL('selected'), (path,))
        
    def resizeEvent(self, e):
        self.slotResize()
        
    def slotResize(self):
        """ Called when a child SelectorItem is resized. """
        self.rearrange()

            
if __name__ == '__main__':
    a = QApplication([])
    w = Selector()
    w.addPath('/home/ajole/wav')
    conf = Globals.ConfFile()
    #conf.setUseGradients(0)
    #conf.save()
    Widgets.use_gradients = conf.getUseGradients()
    w.updateGrooveCategories()
    w.openAll()
    w.show()
    a.setMainWidget(w)
    a.exec_loop()
    
