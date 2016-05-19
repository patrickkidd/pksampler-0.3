
class Knob(QWidget):
    """ A 50 x 50 knob """
    def __init__(self, parent=None, minValue=0, maxValue=127, step=1, pageStep=10, initialPosition=0, size=50):
        QWidget.__init__(self, parent)
        self.step = step
        self.pageStep = pageStep
        self.lastPosition = initialPosition
        self.position = initialPosition
        self.buttonPressed = 0
        self.lastY = 0
        self.lastX = 0
        self.knobColour = QColor(0, 0, 0)

        QToolTip.add(self,
                 "Click and drag up and down or left and right to modify")
        self.resize(size, size)
        #self.setFixedSize(size, size)
    
        # set the initial position
        self.drawPosition()
        
    def setValue(self, value):
        self.position = value
        self.repaint()
        
    def setKnobColor(self, color):
        self.knobColour = color
        self.repaint()
        
    def mousePressEvent(self, e):
        #self.palette().color(QPalette.Active, QColorGroup.Dark)
        if e.button() == Qt.LeftButton:
        
            self.buttonPressed = 1
            self.lastY = e.y()
            self.lastX = e.x()
    
            # Reposition - we need to sum the relative positions up to the
            # topLevel or dialog to please move().
            par = self.parentWidget()
            totalPos = self.pos()
    
            if par:
                while par.parentWidget() and not par.isTopLevel() and par.isDialog():
                    totalPos = totalPos + par.pos()
                    par = par.parentWidget()
        
        # reset to center position
        elif e.button() == Qt.RightButton:
            self.position = (self.maxValue() + self.minValue()) / 2.0
            self.drawPosition()
            self.emit(PYSIGNAL("valueChanged"), (self.position, None))
            
    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.buttonPressed = 0
            self.lastY = 0
            self.lastX = 0
                
    def mouseMoveEvent(self, e):
        if self.buttonPressed:
            # Dragging by x or y axis when clicked modifies value
            newValue = self.position + (self.lastY - float(e.y()) + float(e.x()) - self.lastX) * self.step
    
            if newValue > self.maxValue():
                self.position = self.maxValue()
            else:
                if newValue < self.minValue():
                    self.position = self.minValue()
                else:
                    self.position = newValue
    
            # don't update if there's nothing to update
            if self.lastPosition == self.position: 
                return
    
            self.lastY = e.y()
            self.lastX = e.x()
    
            self.drawPosition()
    
            self.emit(PYSIGNAL("valueChanged"), (self.position, None))

    def wheelEvent(self, e):
        if e.delta() > 0:
            self.position -= self.pageStep
        else:
            self.position += self.pageStep
    
        if self.position > self.maxValue():
            self.position = self.maxValue()
    
        if self.position < self.minValue():
            self.position = self.minValue()
    
        self.drawPosition()
    
        # Reposition - we need to sum the relative positions up to the
        # topLevel or dialog to please move().
        par = self.parentWidget()
        totalPos = self.pos()
    
        while par.parentWidget() and not par.isTopLevel() and not par.isDialog():
            totalPos += par.pos()
            par = par.parentWidget()
    
        # set it to show for a timeout value
        self.emit(PYSIGNAL("valueChanged"), (self.position, None))
    
    def paintEvent(self, e):
        paint = QPainter(self)
        pen = QPen()
        paint.setClipRegion(e.region())
        paint.setClipRect(e.rect().normalize())
        
        paint.setPen(self.palette().color(QPalette.Active, QColorGroup.Dark))

        if self.knobColour != Qt.black:
            paint.setBrush(self.knobColour)
        else:
            paint.setBrush(self.palette().color(QPalette.Active, QColorGroup.Base))

        paint.drawEllipse(0,0,self.size().width(), self.size().height())
        self.drawPosition()
        
    def drawPosition(self):
        """ draws the current value based on self.position. """
        paint= QPainter(self)
        pen = QPen()
        pen.setWidth(4)
        hyp = float(self.size().width()) / 2.0

        #Undraw the previous line
        angle = (0.22 * math.pi) + \
                        (1.6 * math.pi * (float(self.lastPosition - self.minValue()) / \
                        (float(self.maxValue()) - float(self.minValue()))))
        x = float(hyp - 0.9 * hyp * math.sin(angle))
        y = float(hyp + 0.9 * hyp * math.cos(angle))

        if self.knobColour != Qt.black:
            pen.setColor(self.knobColour)
        else:
            pen.setColor(self.palette().color(QPalette.Active, QColorGroup.Base))
        paint.setPen(pen)
        paint.drawLine(int(hyp), int(hyp), int(x), int(y))

        # Draw the new position
        angle = (0.22 * math.pi) + \
                    (1.6 * math.pi * (float(self.position - self.minValue()) /
                    (float(self.maxValue()) - float(self.minValue()))))
        x = float(hyp - 0.9 * hyp * math.sin(angle))
        y = float(hyp + 0.9 * hyp * math.cos(angle))
    
        pen.setColor(self.palette().color(QPalette.Active, QColorGroup.Dark))
        paint.setPen(pen)
        paint.drawLine(int(hyp), int(hyp), int(x), int(y))

        self.drawTextValue()
        self.lastPosition = self.position
    
    def drawTextValue(self):
        paint = QPainter(self)
        pen = QPen()
        font = QFont()
        font.setPointSize(self.width() / 10)
        paint.setFont(font)
        
        # undraw previous value
        if self.knobColour != Qt.black:
            pen.setColor(self.knobColour)
        else:
            pen.setColor(self.palette().color(QPalette.Active, QColorGroup.Base))
        paint.setPen(pen)
        point = self.getTextPoint(self.lastPosition, font)
        paint.drawText(point, QString(str(int(self.lastPosition))))
    
        # draw text value
        pen.setColor(self.palette().color(QPalette.Active, QColorGroup.Text))
        paint.setPen(pen)
        point = self.getTextPoint(self.position, font)
        paint.drawText(point, QString(str(int(self.position))))
        
    def getTextPoint(self, value, font):
        """ Adjusts the text point according to the value. """
        if value > 99:
            x = self.width() / 2 - font.pointSize() * 2.5
        elif value < 10:
            x = self.width() / 2 
        else:
            x = self.width() / 2 - font.pointSize()
            
        y = (self.height() / 4) * 3.5
        return QPoint(x,y)
                
    def setPosition(self, position):
        self.position = position
        self.drawPosition()
        



class L33tSlider(QSlider):
    def __init__(self, orientation=Qt.Vertical, parent=None, name=None):
        QSlider.__init__(self, orientation, parent, name)
        self.pressed = 0
        
    def currentlyPressed(self):
        return self.pressed
        
    def setValue(self, v):
        if not self.pressed:
            QSlider.setValue(self, v)
        
    def mousePressEvent(self, e):
        if e.button() != Qt.RightButton:
            self.pressed = 1
            QSlider.mousePressEvent(self, e)
        
    def mouseReleaseEvent(self, e):
        self.pressed = 0
        QSlider.mouseMoveEvent(self, e)
        self.emit(PYSIGNAL('userChanged'), (self.value(), ))
        

class Slider(QSlider):
    
    def __init__(self, orientation=Qt.Vertical, parent=None, name=None, f=0):
        QSlider.__init__(self, orientation, parent, name)
        self.knob_width = 15
        self.orientation = orientation
        self.l33t = 0
        
    def setKnobWidth(self, w):
        self.knob_width = w

    def mouseMoveEvent(self, e):
        if not self.l33t:
            QSlider.mouseReleaseEvent(self, e)
            #self.emit(SIGNAL("valueChanged(int)"), (int(self.value())))
        
    def mouseReleaseEvent(self, e):
        self.pressed = 0
        if self.l33t:
            QSlider.mouseReleaseEvent(self, e)
            #self.emit(SIGNAL("valueChanged(int)"), (self.value())
    
    def setL33t(self, a0):
        """ If a0 is true, valueChanged is only emitted on mouse release. """
        self.l33t = a0
        
        
    def paintEvent(self, e):
        """ Paint a slider. """
        
        #if self.changed:
        if 1:
            self.erase(1,1,-1,-1)
    
            painter = QPainter(self)
        
            # GROOVE
            
            if self.orientation == Qt.Vertical:
                groove_args = ((self.width() * 3) / 11, 0, 3, self.height())
            else:
                groove_args = (0, (self.height() * 3) / 11, self.width(), 3)
            
            c = self.paletteBackgroundColor()
            painter.setPen(c.dark(150))
            painter.setBrush(c.dark(120))
            painter.drawRect(QRect(*groove_args))
            # set the brush to draw over the groove
            painter.setBrush(self.paletteBackgroundColor())
            painter.setPen(self.paletteForegroundColor())
            
            # KNOB
        
            range = abs(self.minValue() - self.maxValue())
            abs_value = abs(self.maxValue() - self.value())
            pixel_percent = (abs_value * 1.0) / range
            
            if self.orientation == Qt.Vertical:
                value_y = self.height() - self.height() * pixel_percent
                
                # keep it in the widget
                if value_y < self.knob_width / 2:
                    value_y = self.knob_width / 2
                elif value_y > (self.height() - self.knob_width / 2) - 1:
                    value_y = (self.height() - self.knob_width / 2) - 1
                    
                rect_args = (0, value_y - self.knob_width / 2, 
                        self.width(), self.knob_width)
                        
            else:
                value_x = self.width() - self.width() * pixel_percent
                
                # keep it in the widget
                if value_x < self.knob_width / 2:
                    value_x = self.knob_width / 2
                elif value_x > (self.width() - self.knob_width / 2) - 1:
                    value_x = (self.width() - self.knob_width / 2) - 1
                    
                rect_args = (value_x - self.knob_width / 2, 0, 
                        self.knob_width, self.height())
            
            
            mid_args = (rect_args[0]+1, rect_args[1]+1, rect_args[2]-2, rect_args[3]-2)
            inner_args = (mid_args[0]+1, mid_args[1]+1, mid_args[2]-2, mid_args[3]-2)

            knob_rect = QRect(*rect_args)
            mid_rect = QRect(*mid_args)
            inner_rect = QRect(*inner_args)
            
            painter.drawRoundRect(knob_rect)
            c = self.paletteBackgroundColor()
            c = c.dark(200)
            painter.setPen(c)
            painter.drawRoundRect(mid_rect)
            c = c.light(150)
            painter.setPen(c)
            painter.drawRoundRect(inner_rect) 


class CycleButton(QWidget):
    """ A button that cycles through pixmaps and has an index state. """
    def __init__(self, pixmaps=None, parent=None, name=None, f=0):
        QWidget.__init__(self, parent, name, f)
        self.pixmaps = []
        if pixmaps and len(pixmaps):
            self.setPixmaps(pixmaps)
        self.index = 0
        self.update()

    def SetIndex(self, index):
        """ Set the index. """
        if index <= len(self.pixmaps):
            return
        else:
            self.index = index
            self.drawButton()

    def GetIndex(self):
        return self.index

    def mouseReleaseEvent(self, me):
        self.index = self.index + 1
        if self.index == len(self.pixmaps):
            self.index = 0

        self.update()
        self.emit(PYSIGNAL("clicked"), ())
    
    def setPixmaps(self, pixmaps):
        """ Set the pixmaps to pixmaps, a tuple of file names. """
        self.pixmaps = []
        for i in pixmaps:
            p = Globals.load_pixmap(i)
            if p:
                self.pixmaps.append(p)
        self.index = 0
        self.update()

    def paintEvent(self, pe):
        """ Paint the pixmap. """
        if len(self.pixmaps):
            p = QPainter(self)
            p.drawPixmap(QPoint(0,0), self.pixmaps[self.index])
        PixmapButton.paintEvent(self, pe)    



class OldButton(QPushButton, PixmapWidget):
    """ Retains the QPushButton text label while drawing with pixmaps. 
        Not sure if I really want this any more.
    """
    
    def __init__(self, pixmap_paths, name, parent=None):
        """ Pass no image paths for a text button, or just the on image path for all images. """
        QPushButton.__init__(self, parent)
        PixmapWidget.__init__(self, pixmap_paths, name)
        
    def drawButton(self, painter):
        flags = QStyle.Style_Default
        if self.isEnabled():
            flags |= QStyle.Style_Enabled
        if self.hasFocus():
            flags |= QStyle.Style_HasFocus
        if self.isDown():
            flags |= QStyle.Style_Down
        if self.isOn():
            flags |= QStyle.Style_On
        if not self.isFlat() and not self.isDown():
            flags |= QStyle.Style_Raised
        if self.isDefault():
            flags |= QStyle.Style_ButtonDefault
        
        self.style().drawControl(QStyle.CE_PushButtonLabel, painter, self, 
                                 QRect(0,0,self.width() - 10, self.height() - 9),
                                 self.colorGroup(),
                                 flags)







class LED(QLabel):
    def __init__(self, parent=None, name=None, f=0):
        QLabel.__init__(self, parent, name, f)
        self.on = 0
        
        self.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.setScaledContents(1)
        self.annoying = 0
        self.color = QColor("red")
        
    def setColor(self, color=QColor("red")):
        self.color = color
        self.update()
        
    def setOn(self, a0=0):
        self.on = a0
        self.update()
        
    def startFlashing(self, msecs=750):
        self.stopFlashing()
        self.startTimer(msecs)
        self.setOn(1)
        
    def stopFlashing(self):
        self.killTimers()
        
    def SetAnnoying(self, a0):
        self.annoying = a0
        
    def Toggle(self):
        self.setOn(not self.on)
        
    def timerEvent(self, e):
        self.Toggle()
            
    def paintEvent(self, e):
        p = QPainter(self)
        
        outer_args = (1, 1, self.width() - 2, self.height() - 2)
        outer_rect = QRect(*outer_args)
        
        inner_args = (4, 4, self.width() - 7, self.height() - 8)
        inner_rect = QRect(*inner_args)
        
        if self.on:
        
            color = self.color
            p.setBrush(color)
            pen = QPen()
            
            # OUTER
            
            c = color.dark(200)
            pen.setColor(c)
            pen.setWidth(1)
            p.setBrush(c)
            p.setPen(pen)
            p.drawRoundRect(outer_rect)
            
            # INNER
            
            pen.setWidth(1)
            c = color.light(140)
            pen.setColor(c)
            p.setBrush(color)
            p.setPen(pen)
            p.drawRoundRect(inner_rect)

            
        else:

            # INNER: OFF
            
            c = self.paletteBackgroundColor().dark(250)
            pen = QPen()
            pen.setColor(c)
            pen.setWidth(1)
            p.setPen(pen)
            off_args = (3, 3, self.width() - 7, self.height() - 8)
            p.drawRoundRect(inner_rect)
        
        if not self.annoying or (self.annoying and self.on):
                # font (for resize events?)
                f = QFont()
                f.setItalic(1)
                f.setBold(1)
                if self.height() < self.width():\
                    ps = self.height() / 5
                else:
                    ps = self.width() / 5
                f.setPointSize(ps)
                self.setFont(f)
            
                QLabel.paintEvent(self, e)
                





class CollapsableBuddy(QWidget):
    """ A widget that a Collapsable widget can dock to. """
    def __init__(self, parent=None, name=None, f=0):
        QWidget.__init__(self, parent, name, f)
    
    def resizeEvent(self, re):
        self.emit(PYSIGNAL('resized'), ())
    
    def moveEvent(self, me):
        self.emit(PYSIGNAL('moved'), ())
        

class Collapsable(QWidget):
    """ A floating collapsable widget that sticks to a buddy.
        Qt.AlignmentFlags is used to specifiy the behavior of the widget.
        Qt.AlignLeft will collapse the widget to the left side,
        Qt.AlignRight will collapse thewidget to the right seide, and so on.
        A collapse tab is added to the alignment side of thickness 
        'self.tabThickness'.
    """

    def __init__(self, buddy=None, alignment=Qt.AlignLeft):
        """ Construct a widget with Qt.AlignmentFlags.
            'buddy' is the CollapsableBuddy that this one can stick to.
            'name' will go in the title tab.
        """
        if buddy:
            parent = buddy.parentWidget()
        else:
            parent = None
        QWidget.__init__(self, None)
        self.buddy = buddy
        self.alignment  = alignment
        self.collapsed = 0
        self.tabThickness = 20
        self.uncollapsedSize = self.size()

        # THE TAB BUTTON
        self.tab = QPushButton(self)
        self.tab.setPaletteBackgroundColor(QColor("black"))
        self.tab.move(0,0)
        QObject.connect(self.tab, SIGNAL('clicked()'), self.ToggleCollapsed)
        
        # THE MAIN WidGET
        self.mainWidget = QWidget(self)
        self.mainWidget.setPaletteBackgroundColor(QColor("yellow"))

        self.SetBuddy(self.buddy)
        self.SetUncollapsedSize(self.size())
        self.SetCollapsed(0)
    
    def SetTabPixmap(self, pixmap):
        """ Set the pixmap on the collapse widget. """
        self.tab.setPixmaps([pixmap])
    
    def GetTabThickness(self):
        return self.tabThickness
        
    def SetTabThickness(self, thickness):
        """ Set the collapsed thickness. The default is 20. """
        self.tabThickness = thickness
        self.update()
        
    def ToggleCollapsed(self):
        self.SetCollapsed(not self.collapsed)
        
    def SetCollapsed(self, collapsed):
        """ Collapse or uncollapse the widget by adjusting the size.
        """
        self.collapsed = collapsed
        
        if collapsed:

            if self.alignment == Qt.AlignBottom:
                new_height = self.tabThickness
                new_width = self.size().width()
            elif self.alignment == Qt.AlignTop:
                new_height = self.tabThickness
                new_width = self.size().width()
            elif self.alignment == Qt.AlignLeft:
                new_height = self.size().height()
                new_width = self.tabThickness
            elif self.alignment == Qt.AlignRight:
                new_height = self.size().height()
                new_width = self.tabThickness

            # Do the update
            self.resize(new_width, new_height)           
            self.tab.resize(self.size())
            self.tab.raiseW()
            self.tab.show()
            
        else:
        
            self.resize(self.uncollapsedSize)
            
        self.update()
 
    def SetUncollapsedSize(self, size_or_w, h=None):
        """ Set the uncollapsed size. 
            The collapse tab will be added inside the new size.
        """
        old = self.uncollapsedSize
        if h:
            self.uncollapsedSize = QSize(size_or_w, h)
        else:
            self.uncollapsedSize = size_or_w
        if (not self.collapsed) and  \
            (self.uncollapsedSize.width() != old.width() or \
            self.uncollapsedSize.height() != old.height()):
            self.SetCollapsed(1)
            self.SetCollapsed(0)

    def UncollapsedSize(self):
        """ Returns the uncollapsed size as a QSize. 
            Can be used to compensate for the collapse tab.
        """
        return self.uncollapsedSize
            
    def SetBuddy(self, buddy):
        """ Change the buddy widget to 'buddy'. """
        if self.buddy:
            QObject.disconnect(self.buddy, PYSIGNAL("resized"), self.update)
            QObject.disconnect(self.buddy, PYSIGNAL("moved"), self.update)
        self.buddy = buddy
        QObject.connect(self.buddy, PYSIGNAL("resized"), self.update)
        QObject.connect(self.buddy, PYSIGNAL("moved"), self.update)
        self.update()
    
    def SetTabColor(self, color):
        """ Set the background color of the tab. """
        self.tab.setPaletteBackgroundColor(color)
        
    
    def update(self):
        """ Update the location according to the buddy. """

        # Move the widget
        if self.alignment == Qt.AlignBottom:
            if self.buddy:
                new_x = self.buddy.x()
                new_y = self.buddy.y() - self.height()
            new_tab_p = QPoint(0,self.height() - self.tab.height())
            new_main_p = QPoint(0,0)
        elif self.alignment == Qt.AlignTop:
            if self.buddy:
                new_x = self.buddy.x()
                new_y = self.buddy.y() + self.buddy.size().height()
            new_tab_p = QPoint(0,0)
            new_main_p = QPoint(0, self.tab.height())
        elif self.alignment == Qt.AlignLeft:
            if self.buddy:
                new_x = self.buddy.x() + self.buddy.size().width() + 1
                new_y = self.buddy.y()
            new_tab_p = QPoint(0,0)
            new_main_p = QPoint(self.tab.width(), 0)
        elif self.alignment == Qt.AlignRight:
            if self.buddy:
                new_x = self.buddy.x() - self.size().width() - 1
                new_y = self.buddy.y()
            new_tab_p = QPoint(self.size().width() - self.tab.size().width(), 0)
            new_main_p = QPoint(0,0)
        
        if self.buddy:
            self.move(new_x, new_y)
        self.tab.move(new_tab_p)
        self.mainWidget.move(new_main_p)

        QWidget.update(self)
    
    def resizeEvent(self, e):
        """ Resize the tab accordingly. """
        if self.alignment == Qt.AlignTop or self.alignment == Qt.AlignBottom:
            self.tab.resize(self.size().width(), self.tabThickness)    
            self.mainWidget.resize(self.width(), self.height() - self.tab.height())
        elif self.alignment == Qt.AlignRight or self.alignment == Qt.AlignLeft:
            self.tab.resize(self.tabThickness, self.size().height())
            self.mainWidget.resize(self.width() - self.tab.width(), self.height())
        QWidget.resizeEvent(self, e)
        
