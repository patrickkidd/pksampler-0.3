
from qt import *
from Part import *

TAB_WIDTH = 100
TAB_HEIGHT = 100
MARGIN = 2


class TabView(Part):
    """ A main widget that is associated with a tab. """
    def __init__(self, parent=None, name=None, f=0):
        Part.__init__(self, parent, name, f)
        self.move(TAB_WIDTH + 5, TAB_HEIGHT + 5)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setDrawBorder(False)

        
class Tab(QLabel):
    def __init__(self, align, parent=None, name='Control Tab', f=0):
        QLabel.__init__(self, parent, name, f)
        self.setFixedSize(TAB_WIDTH, TAB_HEIGHT)
        self.setAlignment(Qt.AlignCenter)
        self.align = align
        self.color = QColor('blue')
        self.setColor(self.color)
        self.setText(name)
        self.setFont(QFont( "Helvetica", 10, QFont.Bold ))
    
    def setColor(self, c):
        self.color = c
        self.colors = (self.color,)
        self.setPaletteForegroundColor(self.color)
        self.colors = (self.color,)
        
    def getColor(self):
        return self.color

    def setSelected(self):
        """ Sets this tab selected, tells the MainWindow. """
        self.emit(PYSIGNAL('clicked'), (self,))
        
    def mouseReleaseEvent(self, e):
        self.setSelected()
        
    def paintEvent(self, e):
        """ Just draw the appropriate part of the border. """
        self.erase()
        p = QPainter(self)
        
        if self.parent():
            self.setPaletteBackgroundColor(self.parent().paletteBackgroundColor())

        # set up the corrdinates
        if self.align == Qt.AlignLeft:
            x,y,w,h = (MARGIN,MARGIN,self.width()+30,self.height()-MARGIN)
        elif self.align == Qt.AlignRight:
            x,y,w,h = (-30,MARGIN,self.width()+30,self.height()-MARGIN)
        elif self.align == Qt.AlignTop:
            x,y,w,h = (MARGIN,MARGIN,self.width()-MARGIN,self.height()+30)
        elif self.align == Qt.AlignBottom:
            x,y,w,h = (MARGIN,-30,self.width()-MARGIN,self.height()+30)
        
        xRnd = TAB_WIDTH / 4
        yRnd = TAB_HEIGHT / 4
        
        for c in self.colors:
            r = QRect(x,y,w,h)
            p.setPen(c)
            p.drawRoundRect(r, xRnd, yRnd)
            x,y,w,h = (x+1,y+1,w,h)
        
        QLabel.paintEvent(self, e)
        
        
class TabWindow(QWidget):
    """ This is just a giant tab widget. """
    def __init__(self, parent=None, name=None, f=0):
        QWidget.__init__(self, parent, name, f)
        self.setPaletteBackgroundColor(QColor('black'))
        self.leftTabs = []
        self.rightTabs = []
        self.topTabs = []
        self.bottomTabs = []
        self.selectedTab = None
        self.views = []
        self.viewStack = QWidgetStack(self)

    def addTab(self, tab, view):
        if tab.align == Qt.AlignLeft and not tab in self.leftTabs:
            self.leftTabs.append(tab)
        elif tab.align == Qt.AlignRight and not tab in self.rightTabs:
            self.rightTabs.append(tab)
        elif tab.align == Qt.AlignTop and not tab in self.topTabs:
            self.topTabs.append(tab)
        elif tab.align == Qt.AlignBottom and not tab in self.bottomTabs:
            self.bottomTabs.append(tab)
        view.setPaletteBackgroundColor(self.paletteBackgroundColor())
        self.views.append((view, tab))
        self.viewStack.addWidget(view)
        QObject.connect(tab, PYSIGNAL('clicked'), self.slotSelected)
        tab.show()
        self.rearrange()
        tab.setSelected()
    
    #def deleteTab(self, tab):
    #    if tab in self.leftTabs:
    #            self.leftTabs.remove(tab)
    #    elif tab in self.rightTabs:
    #            self.rightTabs.remove(tab)
    #    elif tab in self.topTabs:
    #            self.topTabs.remove(tab)
    #    elif tab in self.bottomTabs:
    #            self.bottomTabs.remove(tab)
    #    tab.reparent(None, QPoint(0,0))
    #    QObject.disconnect(tab, PYSIGNAL('clicked'), self.slotSelected)
        
    def rearrange(self):
        x1 = (len(self.topTabs) * TAB_WIDTH) / 2
        x2 = (self.width() / 2)
        x =  x2 - x1
        y = 0
        for t in self.topTabs:
            t.move(x, y)
            x += TAB_WIDTH
        
        x1 = (len(self.bottomTabs) * TAB_WIDTH) / 2
        x2 = (self.width() / 2)
        x =  x2 - x1
        y = self.height() - TAB_HEIGHT
        for t in self.bottomTabs:
            t.move(x,y)
            x += TAB_WIDTH
            
        y1 = (len(self.leftTabs) * TAB_HEIGHT) / 2
        y2 = (self.height() / 2)
        y =  y2 - y1
        x = 0
        for t in self.leftTabs:
            t.move(x, y)
            y += TAB_HEIGHT
        
        y1 = (len(self.rightTabs) * TAB_HEIGHT) / 2
        y2 = (self.height() / 2)
        y =  y2 - y1
        x = self.width() - TAB_WIDTH
        for t in self.rightTabs:
            t.move(x, y)
            y += TAB_HEIGHT
    
    def resizeEvent(self, e):
        self.rearrange()
        self.viewStack.setGeometry(TAB_WIDTH + 5,
                                    TAB_HEIGHT + 5,
                                    self.width() - 10 - TAB_WIDTH * 2,
                                    self.height() - 10 - TAB_HEIGHT * 2)
        QWidget.resizeEvent(self, e)
        
    def slotSelected(self, tab):
        """ Called when a tab is clicked. """
        old_v, old_t = None, None
        if not tab == self.selectedTab:
            for v, t in self.views:
                if t == self.selectedTab:
                    old_v, old_t = v, t
                #if tab == t:
                #    new_v, new_t = v, t
            self.selectedTab = tab
            if old_v:
                old_v.fadeOut(self.doShowSelectedTabView)
            self.update()

    def doShowSelectedTabView(self):
        """ Private function. """
        for v, t in self.views:
            if t == self.selectedTab:
                break
        self.viewStack.raiseWidget(v)
        v.fadeIn()

        
    def paintEvent(self, e):
        """ Draw the main border for the selected widget. """
        if not self.selectedTab:
            return
        
        t = self.selectedTab
        if t.align == Qt.AlignLeft:
            p1 = t.mapTo(self, QPoint(t.width()-15, 0))
            p2 = t.mapTo(self, QPoint(t.width()+15, t.height()))
        elif t.align == Qt.AlignRight:
            p1 = t.mapTo(self, QPoint(-15, 0))
            p2 = t.mapTo(self, QPoint(15, t.height()))
        elif t.align == Qt.AlignTop:
            p1 = t.mapTo(self, QPoint(0, t.height()-15))
            p2 = t.mapTo(self, QPoint(t.width(), t.height()+15))
        elif t.align == Qt.AlignBottom:
            p1 = t.mapTo(self, QPoint(0, -15))
            p2 = t.mapTo(self, QPoint(t.width(), 15))

        p = QPainter(self)
        p.setPen(QColor(t.color))

        p.drawRect(QRect(TAB_WIDTH,
                         TAB_HEIGHT,
                         self.width() - TAB_WIDTH * 2,
                         self.height() - TAB_HEIGHT * 2))
        self.erase(QRect(p1, p2))


    
def test_Tabs():
    a = QApplication([])
    w = QWidget()
    w.setPaletteBackgroundColor(QColor('black'))
    t1 = Tab(Qt.AlignLeft, w)
    t2 = Tab(Qt.AlignRight, w)
    t3 = Tab(Qt.AlignTop, w)
    t4 = Tab(Qt.AlignBottom, w)
    t2.move(t1.x() + t1.width() + 5, 0)
    t3.move(t2.x() + t1.width() + 5, 0)
    t4.move(t3.x() + t1.width() + 5, 0)
    w.show()
    a.setMainWidget(w)
    a.exec_loop()
    
def test_TabWindow():
    a = QApplication([])
    w = TabWindow()
    cs = ['blue', 'red', 'yellow', 'green']
    for i in (Qt.AlignLeft, Qt.AlignRight, Qt.AlignBottom, Qt.AlignTop):
        for j in range(4):
            v = TabView()
            v.setDrawBorder(True)
            v.setRoundCorners(True)
            t = Tab(i, w, 'Tab %i' % j)
            t.setColor(QColor(cs[j]))
            v.setColor(QColor(cs[j]))
            w.addTab(t, v)
            w.show()
    a.setMainWidget(w)
    a.exec_loop()

