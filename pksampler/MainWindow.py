#!/bin/env python
""" MainWindow and other high-level classes.
    TODO:
    - MainWindow.closeEvent breaks encapsulation for breaking down samples.
"""


import sys
import os
from qt import *
from Queue import Queue
import Globals
from Globals import loadPixmap
import SampleWidget
import Selector
import Widgets
import PovWidgets
import ControlPanel
import time
from Grouping.Widgets import TrackFrame, SampleGroup
from Grouping.Widgets import GroupWidgetStack, GroupDialog

try:
    from pkstudio import Rack
    from pksequencer import PKSequencer
    from pksequencer import patchtool
    from pksequencer.patchtool import NewPatchDialog
    USE_PKSTUDIO = True
    Globals.Print("Using pkstudio rack")
except ImportError, e:
    USE_PKSTUDIO = False

PKAudio = Globals.getPKAudio()


selected_color = QColor(248, 139, 0)
backgroundColor = QColor(109, 109, 109)
num_tracks = 4
channel_offset = 0
num_auxTrackPools = 8
palette = None
trackDropFrames = 20
MARGIN = 10
ANIM_INTERVAL_MS = 7
FRAME_STYLE = QFrame.TabWidgetPanel | QFrame.Raised
MIDDLE_MARGIN = 28

WIDGET_CACHE_SIZE = 10
WIDGET_READ_AHEAD = 3


class ControlFrame(QFrame):
    """ The frame to the right that controls the application and slide-over panels. """
    
    FixedWidth = 70
    
    def __init__(self, parent=None, name=None, f=0):
        QFrame.__init__(self, parent, name, f)
        self.setFixedWidth(ControlFrame.FixedWidth)
        self.setFrameStyle(FRAME_STYLE)
        self.setAcceptDrops(1)
        
        self.exitButton = PovWidgets.PushButton('exit_button', 
                                                'red',
                                                self,
                                                'exitButton')
        #self.exitButton.SetMask(108,78,51,45)
        self.exitButton.setFixedSize(51, 45)
        self.exitButton.move(self.width() / 2 - 25,2)
        
        self.controlPanel = ControlPanel.ControlPanel(self)
        
        self.controlButton = PovWidgets.PushButton('config_button',
                                                   'red',
                                                   self,
                                                   'controlButton')
        self.controlButton.move(self.width() / 2 - 25, 50)
        QObject.connect(self.controlButton, SIGNAL('clicked()'), self.controlPanel.exec_loop)
        
        # Real-time stuff
        self.realtimeLED = PovWidgets.LED('outer_led', 'green', self)
        self.realtimeLED.move(self.width() / 2 - 15, 110)
        self.driver = PKAudio.Driver()
        if self.driver.runningRealtime():
            self.realtimeLED.setOn(1)
        self.realtimeLabel = QLabel(self)
        pixmap = loadPixmap('realtime_label.bmp')
        self.realtimeLabel.setPixmap(pixmap)
        self.realtimeLabel.resize(pixmap.size())
        self.realtimeLabel.move(2, 85)
        
        # Sample trash
        self.sampleTrash = QLabel(self)
        self.sampleTrash.setText('Sample\nTrash')
        font = QFont()
        font.setPointSize(9)
        self.sampleTrash.setFont(font)
        self.sampleTrash.move(2, 150)
        self.sampleTrash.resize(self.width()- 4, 50)
        self.sampleTrash.setAlignment(Qt.AlignCenter)

        self.cpuLabel = QLabel(self)
        self.cpuLabel.setGeometry(20, 200, self.width()-4, self.cpuLabel.height())
        Globals.displayTimer.register(self)

        # Peaks
##~         peak = Globals.PK.getPeakModule(0)
##~         self.leftPeakModule = PovWidgets.PeakModule('outer_peak_module', peak.left, self)
##~         self.leftPeakModule.start()
##~         self.leftPeakModule.move(17, self.height() - self.leftPeakModule.height() - 5)
##~         
##~         self.rightPeakModule = PovWidgets.PeakModule('outer_peak_module', peak.right, self)
##~         self.rightPeakModule.start()
##~         self.rightPeakModule.move(39, self.height() - self.rightPeakModule.height() - 5)
        
    # drag and drop

    def updateDisplay(self):
        usage = self.driver.cpuLoad()
        s = ' CPU:\n%.2f%%' % usage
        self.cpuLabel.setText(s)
    
    def takeTrackFrame(self, trackFrame):
        trackFrame.reparent(None, QPoint(0,0), 0)
        trackFrame.track.slotUnload()
        
    def dragEnterEvent(self, dee):
        """ Whether or not the drag icon will appear to accept it. """
        dee.accept('trackFrame' in Globals.dragObject.__dict__)
    
    def dropEvent(self, de):
        """ Add TrackFrame objects, and remove from the previous parent. """
        # dragging a track
        if hasattr(Globals.dragObject, 'trackFrame'):
            de.accept()
            trackFrame = Globals.dragObject.trackFrame
            oldParent = trackFrame.parentWidget()
            if oldParent and oldParent.parentWidget() and \
                oldParent.parentWidget().__class__ == SampleGroup:
                trackFrame.track.sampleControl.unload()
                self.emit(PYSIGNAL('dropped'), (trackFrame, self, oldParent.parentWidget(), 0))
        
        
class SelectorFrame(QFrame):
    def __init__(self, parent=None, name=None, f=0):
        QFrame.__init__(self, parent, name)
        
        layout = QVBoxLayout(self, 4, 4)
        
        # the control widget
        self.controlWidget = QFrame(self)
        self.controlWidget.setFrameStyle(FRAME_STYLE)
        self.controlWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.controlWidget.setMinimumHeight(37)
        self.collapseButton = PovWidgets.PushButton('collapse_button', 'blue', self.controlWidget)
        self.collapseButton.move(3,3)
        layout.addWidget(self.controlWidget)
        
        self.selector = Selector.Selector(self)
        self.selector.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.selector)
        self.selector.openAll()
        
        
class RackPanel(QFrame):
    def __init__(self, parent=None, name='', f=0):
        QFrame.__init__(self, parent, name)
        self.setFrameStyle(FRAME_STYLE)
        self.setPaletteBackgroundColor(Globals.BACKGROUND_COLOR)
        
        # layout
        RackPanelLayout = QHBoxLayout(self,0,6,"RackPanelLayout")
        
        self.scrollView = QScrollView(self)
        self.scrollView.setVScrollBarMode(QScrollView.AlwaysOn)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum,
                                 QSizePolicy.Expanding,
                                 0,
                                 0,
                                 self.scrollView.sizePolicy().hasHeightForWidth())
        self.scrollView.setSizePolicy(sizePolicy)
        self.scrollView.setMinimumSize(QSize(Rack.Rack.WIDTH + 80,0))
        RackPanelLayout.addWidget(self.scrollView)
        
        spacer = QSpacerItem(111, 61,
                             QSizePolicy.Expanding, 
                             QSizePolicy.Minimum)
        RackPanelLayout.addItem(spacer)
        
        self.rack = Rack.Rack(self.scrollView.viewport())
        self.rack.resize(self.rack.width(), 500)
        self.scrollView.addChild(self.rack)
        
        # control frame
        
        self.addButton = PovWidgets.PushButton('sequencer_button',
                                               color='red', parent=self)
        self.addButton.move(self.scrollView.width() + 5, 5)
        QObject.connect(self.addButton, SIGNAL('clicked()'), self.slotAdd)
        
        self.newPatchDialog = NewPatchDialog(self)
        self.newPatchButton = PovWidgets.PushButton('tool_button',
                                                    color='red', parent=self)
        self.newPatchButton.move(self.addButton.x(),
                                 self.addButton.y()+5+self.addButton.height())
        QObject.connect(self.newPatchButton, SIGNAL('clicked()'),
                        self.newPatchDialog.exec_loop)
        
        self.pitchWheel = PovWidgets.VerticalJogWheel('pitch_wheel', self)
        self.pitchWheel.move(self.addButton.x()+ 60, self.newPatchButton.y())
        QObject.connect(self.pitchWheel, PYSIGNAL('moved'), self.slotTempo)

        xo = self.scrollView.width()+5
        yo = 135
        button_defs = (
                # attrname, ctor, pos, color, slotfunc, tooltip
                ('pitchCenterButton', PovWidgets.PushButton, (xo+60, 5), 'pitch_center_button', 'red', self.slotPitchCenter, 'Zeros the pitch'),
                ('nudgeUpButton', PovWidgets.PushButton,     (xo,    yo+55), 'nudge_up_button', 'red', self.slotNudgeUp, 'Nudges the pitch up'),
                ('nudgeDownButton', PovWidgets.PushButton,   (xo+50, yo+55), 'nudge_down_button', 'red', self.slotNudgeDown, 'Nudges the pitch down'),
                ('pitchUpButton', PovWidgets.PushButton,     (xo,    yo+91), 'pitch_up_button', 'red', None, 'Bends the pitch up'),
                ('pitchDownButton', PovWidgets.PushButton,   (xo+50, yo+91), 'pitch_down_button', 'red', None, 'Bends the pitch down'),
                ('pauseButton', PovWidgets.PushButton,       (xo,    yo+134), 'pause_button', 'blue', self.slotPause, 'Pauses/Starts the sequencer'),
                ('cueButton', PovWidgets.TapButton,          (xo,    yo+177), 'cue_button', 'red', self.slotCue, 'Stops and resets all tracks'),
                ('startButton', PovWidgets.TapButton,        (xo+50, yo+177), 'start_button', 'green', self.slotStart, 'Resets and starts the sequencer'),
                )
        for attrname, ctor, pos, pov_dir, color, slotfunc, tooltip in button_defs:
            if color:
                button = ctor(pov_dir, color, self, attrname)
            else:
                button = ctor(pov_dir, self, attrname)
            self.__dict__[attrname] = button
            button.move(*pos)
            if slotfunc:
                self.connect(button, SIGNAL("clicked()"), slotfunc)
            QToolTip.add(button, tooltip)
        self.pitchCenterButton.setFixedSize(40,32)
        
    def slotAdd(self):
        """ Add a sequencer """
        seq = PKSequencer.PKSequencer()
        seq.hide()
        self.rack.addModule(seq)
        
    def slotTempo(self, delta):
        seq = pksequencer.getSequencerModule()
        if seq:
            seq.setTempo(seq.getTempo() + delta * .05)
            
    def slotPitchCenter(self):
        pass
        
    def slotNudgeUp(self):
        pass
        
    def slotNudgeDown(self):
        pass
        
    def slotPause(self):
        pass
        
    def slotCue(self):
        pass
        
    def slotStart(self):
        pass
        
seqdoneonce = False
def seqwarning():
    global seqdoneonce
    if not seqdoneonce:
        QMessageBox.warning(None,
                            'pksequencer warning',
                            'pksequencer is hardly finished, and may not work at all.',
                            QMessageBox.Ok)
        seqdoneonce = True
        
        
class SampleWidgetCache(Queue):
    """ Caches sample widgets in a queue. """

    def get(self):
        # if empty, read ahead
        if self.qsize() == 0:
            self._readAhead()
        return Queue.get(self)

    def put(self, o):
        Queue.put(self, o)

    def _readAhead(self):
        """ fill to the read ahread limit, instead of the size limit. """
        w = QLabel("Caching widgets...\n\nplease wait...", None)
        w.show()
        global WIDGET_READ_AHEAD
        for i in range(WIDGET_READ_AHEAD):
            self.put(SampleWidget.SampleWidget())

    def fill(self):
        global WIDGET_CACHE_SIZE
        while self.qsize() < WIDGET_CACHE_SIZE:
            self.put(SampleWidget.SampleWidget())
        

        
class MainWindow(QWidget):

    def __init__(self, parent=None, name=None, f=0):
        global palette
        QWidget.__init__(self, parent, name, f)
        self.setPalette(QPalette(backgroundColor, backgroundColor))
        self.setCaption('PKSampler: Main Window')
        self.setIcon(loadPixmap('icon.png'))
        self.setFixedSize(1024,768)
        self.resize(1024,768)
        palette = self.palette()
        
        #conf = Globals.ConfFile()
        self.selectedTrack = None
        
        self.trackFrames = []
        self.trackFramePools = [] # for convenience
        
        ##
        ## TOP PANEL
        ##
        
        # Main Panel
        self.mainWidgetStack = PovWidgets.WidgetStack(self)
        self.mainWidgetStack.setMinimumSize(self.width() - ControlFrame.FixedWidth-2, 
                                            SampleWidget.TRACK_HEIGHT + 10)
        
        self.mainTrackPool = SampleGroup(self.mainWidgetStack)
        self.mainTrackPool.setBackplateColor(Globals.BACKGROUND_COLOR)
        self.mainTrackPool.setBackplatePixmap(loadPixmap('background.png'))
        #self.mainTrackPool.setDeepGrouped(True)
        self.mainWidgetStack.addWidget(self.mainTrackPool)
        self.trackFramePools.append(self.mainTrackPool)
        QObject.connect(self.mainTrackPool, PYSIGNAL('dropped'),
                        self.slotTrackDropped)
        QObject.connect(self.mainTrackPool, PYSIGNAL('saved'),
                        self.slotSaved)
        
        if USE_PKSTUDIO:
            self.rack = RackPanel(self.mainWidgetStack)
            b = PovWidgets.PushButton('sequencer_button', 'red')
            self.mainWidgetStack.addWidget(self.rack, -1, b)
            QObject.connect(b, SIGNAL('clicked()'), seqwarning)
        
        # Control Frame
        self.controlFrame = ControlFrame(self)
        self.controlFrame.move(self.mainWidgetStack.width(), 0)
        self.controlFrame.resize(self.controlFrame.width(), 
                                 self.mainWidgetStack.height())
        self.controlFrame.setPaletteBackgroundColor(backgroundColor)
        self.controlFrame.setSizePolicy(QSizePolicy.Preferred,
                                        QSizePolicy.Expanding)
        QObject.connect(self.controlFrame, PYSIGNAL('dropped'),
                        self.slotTrackUnloaded)
        QObject.connect(self.controlFrame.exitButton, SIGNAL('clicked()'),
                        self.close)
        QObject.connect(self.controlFrame.controlPanel,
                        PYSIGNAL('pathAdded'),
                        self.slotPathAdded)
        QObject.connect(self.controlFrame.controlPanel,
                        PYSIGNAL('pathRemoved'),
                        self.slotPathRemoved)
        QObject.connect(self.controlFrame.controlPanel,
                        PYSIGNAL('useGradients'),
                        self.slotUseGradients)
        QObject.connect(self.controlFrame.controlPanel,
                        PYSIGNAL('mixersChanged'),
                        self.slotMixersChanged)
        
        
        ##
        ## BOTTOM PLATE
        ##

        class ButtonPlate(QPushButton):
            def __init__(self, parent):
                QFrame.__init__(self, parent)
                self.setPaletteBackgroundColor(Globals.BACKGROUND_COLOR)
        self.bottomPlate = QPushButton("Collapse", self)
        self.bottomPlate.resize(self.width()-2, MIDDLE_MARGIN)
        self.bottomPlate.move(1, self.mainWidgetStack.height())
        
        QObject.connect(self.bottomPlate,
                        SIGNAL('clicked()'),
                        self.slotBottomCollapse)
        self.bottomAnimTimer = QTimer(self)
        QObject.connect(self.bottomAnimTimer,
                        SIGNAL('timeout()'),
                        self.slotBottomCollapseEvent)
        self.bottom_collapsed = False
        
        
        ##
        ## BOTTOM PANEL
        ##
        
        # Bottom widget stack
        self.widgetStack = GroupWidgetStack(self)
        self.widgetStack.setPaletteBackgroundColor(Globals.BACKGROUND_COLOR)
        #self.widgetStack.setMaximumWidth((self.width() / 3)*2)
        self.widgetStack.resize(700, self.height() - (self.mainWidgetStack.height() + MIDDLE_MARGIN))
        bottom_y = self.bottomPlate.y() + self.bottomPlate.height()
        self.widgetStack.move(0, bottom_y)
        
        # Output window
        global num_auxTrackPools
        conf = Globals.ConfFile()
        if conf.getUseOutputWindow():
            num_auxTrackPools -= 1
        
        # Auxillary track frame pools
        for i in range(num_auxTrackPools):
            trackPool = SampleGroup(self.widgetStack)
            self.__dict__['auxTrackPool_'+str(i)] = trackPool
            trackPool.setFrameStyle(QFrame.Panel | QFrame.Sunken)
            trackPool.backplate.setPaletteBackgroundPixmap(loadPixmap('background.png'))
            trackPool.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
            trackPool.setMinimumWidth(self.widgetStack.width() - 55)
            trackPool.setName('Collapsed Tracks')
            #trackPool.setBeatSynced(1)
            self.widgetStack.addWidget(trackPool)
            self.trackFramePools.append(trackPool)
            QObject.connect(trackPool, PYSIGNAL('dropped'), self.slotTrackDropped)
            QObject.connect(trackPool, PYSIGNAL('saved'), self.slotSaved)
            
##~         self.ctl = PKCtl.PKCtl(self)
##~         self.ctl.canvas.setPaletteBackgroundPixmap(QPixmap('bg_tile.png'))
##~         button = PovWidgets.PushButton('pk_button', 'blue')
##~         self.widgetStack.addWidget(self.ctl, -1, button)

        if conf.getUseOutputWindow():
            self.outputWidget = Widgets.OutputWidget(self)
            button = PovWidgets.PushButton('pk_button', 'green')
            self.widgetStack.addWidget(self.outputWidget, -1, button)
            
        # TrackFrame Drag n' Drop Animations
        self.trackDropFrame = None
        self.destDropWidget = None
        self.trackDropIndex = None
        self.trackDropSeq = []
        self.dropSizeSeq = []
        self.trackDropTimer = QTimer(self)
        QObject.connect(self.trackDropTimer, SIGNAL('timeout()'), self.slotTrackDropTimer)
  
        # Track editor stack
        self.trackEditors = []
        self.trackEditorStack = QWidgetStack(self.widgetStack, 'Track Editors')
        self.trackEditorStack.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
##~         for i in range(num_tracks):
##~             editor = TrackEditor.TrackEditor(self.trackFrames[i].track.sampleControl, self)
##~             editor.resize(self.width() / 2, bottom_height)
##~             editor.move(3, bottom_y)
##~             editor.show()
##~             self.trackEditors.append(editor)
        self.widgetStack.addWidget(self.trackEditorStack)
        
        # Selector
        self.selectorFrame = SelectorFrame(self)
        self.selectorFrame.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.selectorFrame.setPaletteBackgroundColor(Globals.BACKGROUND_COLOR)
        self.selectorFrame.setLineWidth(2)
        self.selectorFrame.resize(self.width() - self.widgetStack.width() - MARGIN, 
                                  self.height() - self.mainWidgetStack.height())
        self.selectorFrame.move(self.width() - self.selectorFrame.width(), bottom_y)
        self.selectorFrame.selector.updateGrooveCategories()
        
        self.connect(self.selectorFrame.selector, PYSIGNAL('selected'),
                     self.slotLoad)
        self.connect(self.selectorFrame.collapseButton, SIGNAL('clicked()'),
                     self.slotSelectorCollapse)
        
        # collapsed selector
        self.selectorPlate = QFrame(self)
        self.selectorPlate.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.selectorPlate.setPaletteBackgroundColor(Globals.BACKGROUND_COLOR)
        self.selectorPlate.resize(ControlFrame.FixedWidth - MARGIN, self.widgetStack.height())
        self.selectorPlate.move(self.width()-self.selectorPlate.width(), 
                                self.height()-self.selectorPlate.height())
        self.selectorPlate.setMinimumWidth(ControlFrame.FixedWidth - MARGIN)
        self.selectorExpandButton = PovWidgets.PushButton('collapse_button', 'blue', self.selectorPlate)
        self.selectorExpandButton.move(3,3)
        self.selectorPlate.hide()
        QObject.connect(self.selectorExpandButton, SIGNAL('clicked()'),
                        self.slotSelectorCollapse)
        
        # selector animation
        self.selectorAnimTimer = QTimer(self)
        QObject.connect(self.selectorAnimTimer, SIGNAL('timeout()'),
                        self.slotSelectorCollapseEvent)
        self.selector_collapsed = 0
        self.selectorOrigX = self.selectorFrame.x()
            
        # Midi
        #self.midi_map = {}
        #for i in range(num_tracks):
        #    self.midi_map[i + channel_offset] = self.trackFrames[i].track.controllerWidget.slotVolume
        
        # Misc Init
        #self.selectorFrame.selector.openAll()
        self.mainWidgetStack.raiseWidget(0)
        self.widgetStack.raiseWidget(self.trackFramePools[1])
        self.controlFrame.controlPanel.matchUpValues()
        self.controlFrame.controlPanel.slotApply()
        
        # Pre-cached samplewidgets
        self.sampleWidgetCache = SampleWidgetCache()
        
        
    def closeEvent(self, e):
        self.unloadAllSamples()
        QWidget.closeEvent(self, e)

    def unloadAllSamples(self):
        """ Manually destruct all Samples. """
        for t in self.trackFrames:
            t.track.slotUnload()
        
    def fillWidgetCache(self):
        """ This is here for tighter external control (splashscreen). """
        self.sampleWidgetCache.fill()

    def keyPressEvent(self, e):
        # events should be passed to child widgets.
        #if e.isAutoRepeat():
        #    e.ignore()
            
        # select track
        if e.key() == Qt.Key_AsciiTilde:
            if self.selectedTrack:
                index = self.trackFrames.index(self.selectedTrack)
                # last track
                if index == len(self.trackFrames) - 1:
                    index = -1
            else:
                index = -1
            self.SelectTrack(self.trackFrames[index+1])
            e.accept()
        
        elif e.key() == Qt.Key_Space and self.selectedTrack:
            self.selectedTrack.track.sampleControl.slotStart()
            e.accept()
            
        elif e.key() == Qt.Key_Return and self.selectedTrack:
            self.selectedTrack.track.sampleControl.slotCue()
            
        elif e.key() == Qt.Key_Left and self.selectedTrack:
            self.selectedTrack.track.sampleControl.slotPitchUp()
            
        elif e.key() == Qt.Key_Right and self.selectedTrack:
            self.selectedTrack.track.sampleControl.slotPitchDown()            
    
    def keyReleaseEvent(self, e):
        if e.key() == Qt.Key_Left or e.key() == Qt.Key_Right:
            if not self.selectedTrack == None:
                self.selectedTrack.track.sampleControl.slotPitchStop()
            
    def slotLoad(self, path):
        """ Load a file or groove. Called when self.selector emits 'selected'. 
            Pass 'groove: category,id' for a groove; a valid path for a file.
        """
        if path.find('groove:') == 0:
            l = path.replace('groove:','').split(',')
            category = l[0].strip(' ')
            id = l[1].strip(' ')
            self.loadGroove(category, id)
        else:
            self.loadFile(path)
            
    def createTrackFrame(self, path):
        """ Load a sample and return a TrackFrame if it's valid. """
        sample = self.sampleWidgetCache.get()
        sample.slotLoad(path)
        if not sample.isLoaded():
            sample.slotUnload()
            #QMessageBox.information(self,
            #                        "Couldn't open file.",
            #                        "Couldn't open \'"+path+"\'",
            #                        QMessageBox.Ok)
            return None
            
        sample.setPaletteBackgroundColor(self.paletteBackgroundColor().light(115))
        frame = TrackFrame(sample, 5, self)
        frame.setPaletteBackgroundColor(Globals.BACKGROUND_COLOR)
        self.connect(frame, PYSIGNAL('selected'), self.slotTrackSelected)
        self.connect(frame, PYSIGNAL('collapsed'), self.slotTrackCollapsed)
        self.connect(frame, PYSIGNAL('expanded'), self.slotTrackExpanded)
        self.connect(frame, PYSIGNAL('unloaded'), self.slotTrackUnloaded)
        self.trackFrames.append(frame)
        return frame
        
    def loadGroove(self, category, id):
        """ Load a groove's samples into the first open frame and bring it to the front. """
        groove = Globals.GrooveFile(id, category)
        if groove.load() == None:
            return
            
        # Find an open track pool.
        i = 0
        widget = 1
        trackFramePool = None
        for i in range(self.widgetStack.numWidgets()):
            widget = self.widgetStack.widget(i)
            if widget and \
               widget.__class__ == SampleGroup and \
               len(widget.trackFrames) == 0:
               trackFramePool = widget
               break
        
        if trackFramePool:
            samples = groove.getSamples()
            for path in samples:
                volume = samples[path]['volume']
                frame = self.createTrackFrame(path)
                if frame:
                    frame.track.sampleControl.slotVolume(volume)
                    trackFramePool.Add(frame)
                    frame.show()
            self.widgetStack.raiseWidget(trackFramePool)
                    
        # no free SampleGroup
        else:
            QMessageBox.information(self,
                                    "No room for groove!",
                                    "Free up a window in the sample stack before loading a groove.",
                                    QMessageBox.Ok)
            
    def loadFile(self, path):
        """ Create a new track widget and load the sample.
            Called when a file is selected on the selector. 
        """
        frame = self.createTrackFrame(path)
        if frame:
            self.mainTrackPool.Add(frame)
            frame.show()

    def slotTrackCollapsed(self, trackFrame):
        trackFrame.parentWidget().parentWidget().rearrange()
            
    def slotTrackExpanded(self, trackFrame):
        trackFrame.parentWidget().parentWidget().rearrange()

    def slotTrackSelected(self, frame):
        """ Select or deselect a track. """
        if frame != self.selectedTrack:
            self.SelectTrack(frame)
        else:
            self.SelectTrack(None)
            
    def slotTrackUnloaded(self, trackFrame):
        """ Delete the track widget. """
        self.trackFrames.remove(trackFrame)
        self.sampleWidgetCache.put(trackFrame.track)
        try:
            pool = trackFrame.parentWidget().parentWidget()
            if pool.__class__ == SampleGroup:
                pool.Remove(trackFrame)
        except:
            pass
        
    def slotTrackDropped(self, trackFrame, destDropWidget, oldTrackParent=None, sizeAdjust=0):
        """ Called when a TrackFrame is dropped in a SampleGroup. """
        if destDropWidget == oldTrackParent:
            return
        
        # store vars
        self.destDropWidget = destDropWidget
        self.trackDropFrame = trackFrame
        
        # calculate points, anim data
        if trackFrame.parentWidget():
            self.trackOrigPoint = trackFrame.parentWidget().mapTo(self, trackFrame.pos())
        else:
            self.trackOrigPoint = QPoint(0,0) # animate from origin if wierd parent
            
        # find the destination point on the drop widget
        if destDropWidget.__class__ == SampleGroup:
            self.trackDestPoint = destDropWidget.mapTo(self, QPoint(destDropWidget.GetNewTrackX(), 0))
        else:
            self.trackDestPoint = destDropWidget.mapTo(self, QPoint(0, 0))

        # find the height, width diff and divide into segments
        self.trackDropSeq = []
        
        x = self.trackOrigPoint.x()
        y = self.trackOrigPoint.y()
        x_seg = abs(self.trackOrigPoint.x() - self.trackDestPoint.x()) / trackDropFrames
        y_seg = abs(self.trackOrigPoint.y() - self.trackDestPoint.y()) / trackDropFrames
        for i in range(trackDropFrames):
            if self.trackOrigPoint.x() > self.trackDestPoint.x():
                x = x - x_seg
            else:
                x = x + x_seg
            if self.trackOrigPoint.y() > self.trackDestPoint.y():
                y = y - y_seg
            else:
                y = y + y_seg
            self.trackDropSeq.append(QPoint(x,y))
            if sizeAdjust:
                factor = (1.0 * i) / trackDropFrames
                x = factor * self.trackDropFrame.width()
                y = factor * self.trackDropFrame.height()
                self.dropSizeSeq.append([x,y])
        self.dropSizeSeq.reverse()
            
        # reparent to self
        if oldTrackParent:
            oldTrackParent.Remove(trackFrame)
        trackFrame.reparent(self, self.trackOrigPoint)
        trackFrame.show()
        trackFrame.raiseW()
        self.trackDropIndex = 0
        self.slotTrackDropTimer()
        self.trackDropTimer.start(ANIM_INTERVAL_MS)
    Globals.psyco_bind(slotTrackDropped)
        
    def slotTrackDropTimer(self):
        """ Animate the track dropped into a SampleGroup. """
        # animate
        if self.trackDropIndex < len(self.trackDropSeq):
            i = self.trackDropIndex
            self.trackDropFrame.move(self.trackDropSeq[i])
            if len(self.dropSizeSeq) > i:
                self.trackDropFrame.resize(self.dropSizeSeq[i][0], self.dropSizeSeq[i][1])
            self.trackDropIndex += 1
        else:
            self.trackDropTimer.stop()
            self.trackDropIndex = 0
            self.trackDropSeq = []
            self.dropSizeSeq = []
            if self.destDropWidget.__class__ == SampleGroup:
                self.destDropWidget.Add(self.trackDropFrame)
            else:
                self.destDropWidget.takeTrackFrame(self.trackDropFrame)
    
    def slotSaved(self, trackFramePool):
        """ Called when a SampleGroup saves a file. """
        self.selectorFrame.selector.updateGrooveCategories()
        
    def slotPathAdded(self, path):
        """ Called when the ControlPanel adds a selector path. """
        self.selectorFrame.selector.addPath(path)

    def slotPathRemoved(self, path):
        """ Called when the ControlPanel removes a selector path. """
        self.selectorFrame.selector.remove(path)
        
    def slotUseGradients(self, a0):
        """ Called when the use gradients variable is changed in the contol panel. """
        # repaint all the widgets that use gradients.
        self.selectorFrame.selector.repaint()
        
    def slotSelectorCollapse(self):
        """ Called when the collapseButton on the selector frame is clicked. """
        if not self.selector_collapsed:
            self.selectorAnimDirection = 'collapse'
            self.selectorOrigX = self.selectorFrame.x()
            self.slotSelectorCollapseEvent()
            self.selectorAnimTimer.start(ANIM_INTERVAL_MS)
        else:
            self.selectorAnimDirection = 'uncollapse'
            self.slotSelectorCollapseEvent()
            self.selectorAnimTimer.start(ANIM_INTERVAL_MS)
            
    def slotSelectorCollapseEvent(self):
        """ Animate the selector collapse. """
        
        # collapsing
        if self.selectorAnimDirection == 'collapse':
            target_x = self.width() - ControlFrame.FixedWidth - MARGIN
            # done collapsing
            if self.selectorFrame.x() >= target_x:
                self.selectorAnimTimer.stop()
                self.selector_collapsed = 1
                self.widgetStack.resize(target_x+MARGIN,
                                        self.widgetStack.height())
                self.selectorFrame.hide()
                self.selectorPlate.show()
                return
            x = Globals.animInterval+self.selectorFrame.x()
            if x > target_x:
                x = target_x
            self.selectorFrame.move(x,
                                    self.selectorFrame.y())
            self.widgetStack.resize(x,
                                    self.widgetStack.height())
                                    
        # uncollapsing
        else:
            target_x = self.selectorOrigX
            self.selectorFrame.show()
            self.selectorPlate.hide()
            if self.selectorFrame.x() <= target_x:
                self.selector_collapsed = 0
                self.selectorAnimTimer.stop()
                self.widgetStack.resize(target_x - MARGIN,
                                        self.widgetStack.height())
                return
            x = self.selectorFrame.x()-Globals.animInterval
            if x < target_x:
                x = target_x
            self.selectorFrame.move(x, 
                                    self.selectorFrame.y())
            self.widgetStack.resize(x-MARGIN,
                                    self.widgetStack.height())
    Globals.psyco_bind(slotSelectorCollapseEvent)
    
    def slotBottomCollapse(self):
        """ Called when the collapseButton on the control frame is clicked. """
        if not self.bottom_collapsed:
            self.bottomAnimDirection = 'collapse'
            self.bottomOrigY = self.widgetStack.y()
            self.slotBottomCollapseEvent()
            self.bottomAnimTimer.start(ANIM_INTERVAL_MS)
        else:
            self.bottomAnimDirection = 'uncollapse'
            self.slotBottomCollapseEvent()
            self.bottomAnimTimer.start(ANIM_INTERVAL_MS)
            
    def moveBottomFrame(self, y):
        """ move the bottom frame to a y value for the widget
            stack and selector. """
        y1 = self.widgetStack.y() - self.bottomPlate.y()
        self.widgetStack.move(self.widgetStack.x(), y)
        self.selectorFrame.move(self.selectorFrame.x(), y)
        self.selectorPlate.move(self.selectorPlate.x(), y)
        self.bottomPlate.move(self.bottomPlate.x(), self.widgetStack.y()-y1)
        self.mainWidgetStack.resize(self.mainWidgetStack.width(),
                                    self.bottomPlate.y())
        self.controlFrame.resize(self.controlFrame.width(),
                                 self.mainWidgetStack.height())
        if USE_PKSTUDIO:
            self.rack.rack.slotRearrange()
        
    def slotBottomCollapseEvent(self):
        """ Animate the bottom frame collapse. """
        
        # collapsing
        if self.bottomAnimDirection == 'collapse':
            target_y = self.height() - self.bottomPlate.height() + MIDDLE_MARGIN
            # done collapsing
            if self.widgetStack.y() >= target_y:
                self.bottomAnimTimer.stop()
                self.bottom_collapsed = 1
                self.moveBottomFrame(target_y)
                return
            # keep collapsing
            else:
                y = Globals.animInterval+self.widgetStack.y()
                if y > target_y:
                    y = target_y
                self.moveBottomFrame(y)
                                    
        # expanding
        else:
            target_y = self.bottomOrigY
            # done expanding
            if self.widgetStack.y() <= target_y:
                self.bottom_collapsed = 0
                self.bottomAnimTimer.stop()
                y = self.bottomOrigY
                self.moveBottomFrame(y)
            # keep expanding
            else:
                y = self.widgetStack.y() - Globals.animInterval
                if y < target_y:
                    y = target_y
                self.moveBottomFrame(y)
    Globals.psyco_bind(slotBottomCollapseEvent)
    
    def slotMixersChanged(self):
        for pool in self.trackFramePools:
            for s in pool.sampleGroup.getSamples():
                s.slotConnectMixers()
            
    def slotPitchRangeChanged(self):
        """ Called when the pitch range is cahnged on the control panel. """
        for pool in self.trackFramePools:
            for s in pool.getSamples():
                if not s.savedPitchRange:
                    s.pitchRange = SampleWidget.pitchRange
        
    def SelectTrack(self, frame):
        """ Select a track, None deselects """
        # deselect
        if frame == None:
            if self.selectedTrack != None:
                self.selectedTrack.setPaletteBackgroundColor(Globals.BACKGROUND_COLOR)
            self.selectedTrack = None
        
        # select
        else:
            if self.selectedTrack != None:
                self.selectedTrack.setPaletteBackgroundColor(Globals.BACKGROUND_COLOR)
            self.selectedTrack = frame
            self.selectedTrack.setPaletteBackgroundColor(selected_color)
            #self.trackEditors[self.selectedTrack].raiseW()
        
        
class TestWindow(QWidget):
    def __init__(self, parent=None, name=None, f=0):
        QWidget.__init__(self, parent, name, f)
        
        self.setPalette(QPalette(backgroundColor, backgroundColor))
        self.setCaption('PKSampler: Main Window')
        self.setIcon(loadPixmap('icon.png'))
        self.setFixedSize(1024,768)
        self.resize(1024,768)
        palette = self.palette()
        
        #conf = Globals.ConfFile()
        self.selectedTrack = None

        # Tracks
        self.trackFrames = []
        self.mainScrollView = QScrollView(self)
        self.mainScrollView.setVScrollBarMode(QScrollView.AlwaysOff)
        self.mainScrollView.setHScrollBarMode(QScrollView.AlwaysOn)
        self.mainScrollView.resize(self.width() - ControlFrame.FixedWidth, SampleWidget.TRACK_HEIGHT + 30)
        
##~         self.trackFramePools = [] # for convenience
        self.mainTrackPool = SampleGroup(self.mainScrollView.viewport())
##~         self.trackFramePools.append(self.mainTrackPool)
##~         self.mainTrackPool.backplate.setPaletteBackgroundColor(Globals.BACKGROUND_COLOR)
##~         self.mainTrackPool.backplate.setErasePixmap(QPixmap('background.png'))
        self.mainTrackPool.setFixedSize(self.width() - ControlFrame.FixedWidth-2,SampleWidget.TRACK_HEIGHT + 10)
##~         self.mainTrackPool.setBeatSynced(0)
        self.mainScrollView.addChild(self.mainTrackPool)
##~         QObject.connect(self.mainTrackPool, PYSIGNAL('dropped'), self.slotTrackDropped)
##~         QObject.connect(self.mainTrackPool, PYSIGNAL('saved'), self.slotSaved)

        

def runTest(self):
    import PKAudio
    import SampleWidget
    from Grouping import Group
    PKAudio.start_server()
    a = QApplication([])
    Group.Sequencer()
    #w = TestWindow()
    w = SampleGroup()
    for p in range(1):
        s = SampleWidget()
        s.slotLoad('/home/ajole/wav/Patrick Kidd - Birdman.wav')
        frame = TrackFrame(s)
        w.Add(frame)
    
    a.setMainWidget(w)
    w.show()
    a.exec_loop()    

if __name__ == "__main__":
    a = QApplication([])
    w = PovWidgets.WidgetStack()
    w.addWidget(SampleGroup())
    w.addWidget(Rack.Rack())
    a.setMainWidget(w)
    w.show()
    a.exec_loop() 
