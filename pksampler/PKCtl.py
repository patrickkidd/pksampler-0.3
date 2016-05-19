#!/bin/env python
""" A widget that provides access to pk modules. """

import sys
from qt import *
import Globals
from PKCtlForm import PKCtlForm

PKAudio = Globals.getPKAudio()

port_width = 10
canvas_color = QColor(105, 153, 216)
mixer_color = QColor(111, 173, 94)


class Draggable:
    def __init__(self):
        self.m_pressed = 0
        self.last_point = QPoint(self.x(), self.y())

    def mousePressEvent(self, e):
        self.m_pressed = 1
        self.last_x = e.x()
        self.last_y = e.y()
        
    def mouseMoveEvent(self, e):
        if self.m_pressed:
            self.move(self.x() - (self.last_x - e.x()), \
                      self.y() - (self.last_y - e.y()))
            self.emit(PYSIGNAL("moved"), ())
            
    def mouseReleaseEvent(self, e):
        self.m_pressed = 0
        
        

class PortWidget(QLabel):
    """ A little guy that looks like a box. """
    
    def __init__(self, pk_port, parent=None, name=None, f=0):
        QLabel.__init__(self, parent, name, f)
        self.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.setFixedSize(10,10)
        self.port = pk_port
        if self.port:
            if self.port.type() == PKAudio.Port.Input:
                color = QColor('red')
            else:
                color = QColor('green')
            self.setPaletteBackgroundColor(QColor("red"))
        

    def mousePressEvent(self, e):
        self.emit(PYSIGNAL("mousePressEvent"), ())
        

    def mouseReleaseEvent(self, e):
        self.emit(PYSIGNAL("mousePressEvent"), ())
        

    
class ModuleWidget(QLabel, Draggable):

    def __init__(self, pk_module, parent=None, name=None, f=0):
        QLabel.__init__(self, parent, name, f)
        self.setFixedSize(100,30)
        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.setFrameStyle(QFrame.Box | QFrame.Sunken)
        self.setText(pk_module.name())
        modname = pk_module.name()
        
        self.module = pk_module
        self.port_widgets = []
    
        n_outs = self.module.numOutputs()
        for i in range(n_outs):
            pw = PortWidget(self.module.outputPort(i), self)            
            pw.move((self.width() - n_outs * (port_width + 2)) + i * (port_width + 2), 2)
            pw.setText(str(i))
            self.port_widgets.append(pw)
                
        n_ins = self.module.numInputs()
        for i in range(n_ins):
            pw = PortWidget(self.module.inputPort(i), self)
            pw.move((self.width() - n_ins * (port_width + 2)) + i * (port_width + 2), self.height() - (port_width + 2))
            pw.setText(str(i))
            self.port_widgets.append(pw)

    def numPorts(self):
        return len(self.port_widgets)
        
    def getPortWidget(self, i):
        return self.port_widgets[i]
        
        
class Canvas(QWidget):
    """ A nifty graphical representation of the library's modules. """

    def __init__(self, parent=None, name=None, f=0):
        QWidget.__init__(self, parent, name, f)
        self.setPaletteBackgroundColor(canvas_color)
        self.driver = PKAudio.Driver()
        
        # Get the modules
        self.mixer_widget = ModuleWidget(self.driver.getMixer(), self)
        self.mixer_widget.setPaletteBackgroundColor(mixer_color)
        QObject.connect(self.mixer_widget, PYSIGNAL("moved"), self.update)
        self.mod_widgets = [self.mixer_widget]
        self.conn_port_widgets = []
        self.slotDrawList()

        
    def slotDrawList(self):
        """ draw the modules in a list to the left side. """
        self.slotUpdateModules()
        for w in self.mod_widgets:
            w.hide()
        # draw the widgets
        last_y = 40
        for w in self.mod_widgets:
            w.move(10, last_y + 10)
            w.show()
            last_y = w.y() + w.height()
        
        
    def slotDrawGraph(self):
        """ Build a graph of modules based on the global mixer. """
        self.slotUpdateModules()
        mixer = self.driver.getMixer()
        for w in self.mod_widgets:
            w.hide()
                

    def slotUpdateModules(self):
        """ Creates new module widgets, hides old ones,
            connects, disconnects ports as needed.
        """
        
        # check for new modules
        engine = self.driver.getEngine()
        new_widgets = []
        for i in range(engine.numModules()):
            new_m = engine.getModule(i)
            new_id = new_m.id()
            name = new_m.name()
            found = 0
            for w in self.mod_widgets:
                if new_id == w.module.id():
                    found = 1
                    
            # Create the new widget
            if not found:
                w = ModuleWidget(new_m, self)
                self.setPaletteBackgroundColor(QColor("white"))
                QObject.connect(w, PYSIGNAL("moved"), self.update)
                w.show()
                self.mod_widgets.append(w)
                new_widgets.append(w)
                
        # check for stale modules
        for ow in self.mod_widgets:
            found = 0
            for i in range(engine.numModules()):
                m = engine.getModule(i)
                if ow.module.id() == m.id():
                    found = 1
                    break
            if not found:
                ow.hide()
                QObject.disconnect(ow, PYSIGNAL("moved"), self.update)
                self.mod_widgets.remove(ow)
                print "removing",ow.text().ascii()
                
    
        # position new widgets
        last_y = 40
        for w in new_widgets:
            w.move(10, last_y + 10)
            last_y = w.y() + w.height()
                    
        # track the connections
        self.conn_port_widgets = []
        for w in self.mod_widgets:
            for pw in w.port_widgets:
                conn = pw.port.connection()
                
                # Store the connection widgets if they exists
                if conn:
                    conn_pw = None                    
                    # find the connected port widget
                    
                    for w in self.mod_widgets: # each module
                        n_ports = w.numPorts()
                        for i in range(n_ports): # each port
                            new_pw = w.getPortWidget(i)
                            if conn.id() == new_pw.port.id():
                            
                                # found the widget
                                conn_pw = new_pw
                                break
    
                        if conn_pw:
                            # found it
                            break
                    
                    # Only registered modules have widgets, so...
                    if conn_pw:
                        self.conn_port_widgets.append([pw, conn_pw])
        
        if len(self.conn_port_widgets):
            self.update()
                    
                    
                    
    def paintEvent(self, e):
        p = QPainter(self)
        for c in self.conn_port_widgets:
            pw1 = c[0]
            pw2 = c[1]
            
            point_a = c[0].parentWidget().mapToParent(c[0].pos())
            point_b = c[1].parentWidget().mapToParent(c[1].pos())
            
            p.drawLine(point_a, point_b)
    
    
class PKCtl(PKCtlForm):

    def __init__(self, parent=None, name=None, f=0):
        PKCtlForm.__init__(self, parent, name, f)
        layout = QHBoxLayout(self.canvasFrame, 0, 0)

        self.scrollView = QScrollView(self.canvasFrame)
        self.canvas = Canvas(self.scrollView.viewport())
        self.canvas.resize(1024,768)
        self.canvas.setPaletteBackgroundPixmap(QPixmap('bg_tile.png'))
        
        self.scrollView.addChild(self.canvas)
        layout.addWidget(self.scrollView)
        
        self.mods = []
    
    def slotDrawGraph(self):
        self.canvas.slotDrawGraph()
        
    def slotDrawList(self):
        self.canvas.slotDrawList()


if __name__ == "__main__":
    import Modules
    a = QApplication(sys.argv)
    import PKAudio
    PKAudio.start_server()

    w = PKCtl()
    w.show()
    
    a.setMainWidget(w)
    a.exec_loop()
