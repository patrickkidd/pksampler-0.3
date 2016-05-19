""" Grouping.py: All graphical and logical classes related to sample grouping.
    TODO:
    - At current, SampleGroup.slotGroupPitch does nothing.
"""


from qt import *
import GroupDialogForm
from CategoryForm import CategoryForm
import PovWidgets
import Group
import SampleWidget
import Globals
from Small.Animation import Animation

GROUP_PREFIX = 'Group '
BACKGROUND_COLOR = QColor(109, 109, 109)
FRAME_STYLE = QFrame.TabWidgetPanel | QFrame.Raised
PALETTE = None



class GroupDialog(GroupDialogForm.GroupDialogForm):
    """ Can add, remove, and select groups. """

    def __init__(self, parent):
        GroupDialogForm.GroupDialogForm.__init__(self, parent)
        self.GROUP_PREFIX = GROUP_PREFIX
        QObject.connect(Group.Sequencer(), PYSIGNAL('groupsUpdated'), self.slotUpdateGroups)
        QObject.connect(Group.Sequencer(), PYSIGNAL('hostsUpdated'), self.slotUpdateHosts)
        self.slotUpdateGroups()
        self.slotUpdateHosts()
        self.group_id = None
        
    def slotUpdateGroups(self):
        self.groupListBox.clear()
        for group in Group.Sequencer().getGlobalGroups():
            item = QListBoxText(self.groupListBox, group)
            
    def slotUpdateHosts(self):
        self.hostListBox.clear()
        for host in Group.Sequencer().getHosts():
            item = QListBoxText(self.hostListBox, host)
            
    def slotSelectionChanged(self, item):
        if item == None:
            self.deleteButton.setEnabled(0)
        else:
            self.deleteButton.setEnabled(1)
            
    def slotNoGroup(self):
        """ No Group button """
        self.group_id = None
        self.accept()
        
    def slotOk(self):
        """ OK button """
        item = self.groupListBox.item(self.groupListBox.currentItem())
        if item != None:
            self.group_id = item.text().ascii()
        else:
            self.group_id = None
        self.accept()
            
    def slotAdd(self):
        """ Eventually kicks of the big global group add. """
        seq = Group.Sequencer()
        groups = seq.getGlobalGroups()
        i = 1
        while i != -1:
            if not GROUP_PREFIX+str(i) in groups:
                seq.slotAddGlobalGroup(GROUP_PREFIX+str(i))
                i = -1
            else:
                i += 1
        
    def slotDelete(self):
        """ Eventually kicks off the global group removal. """
        item = self.groupListBox.item((self.groupListBox.currentItem()))
        group = item.text().ascii()
        Group.Sequencer().slotRemoveGlobalGroup(group)
        

class TrackFrame(QFrame):
    """ Holds a track in a colorable frame.         
        SIGNALS:
            PYSIGNAL('selected'), (self,)
            PYSIGNAL('loaded'), (self,)
            PYSIGNAL('unloaded'), (self,)
            PYSIGNAL('collapsed'), (self,)
            PYSIGNAL('expanded'), (self,)
    """
    
    def __init__(self, track=None, margin=5, parent=None, name=None, f=0):
        """ Insert the track into a frame with margin 'margin'. """
        QFrame.__init__(self, parent, name, f)
        self.setFrameStyle(FRAME_STYLE)
        if PALETTE:
            self.setPalette(PALETTE)
        self.margin = margin
        if track != None:
            self.track = track
        else:
            self.track = SampleWidget.SampleWidget()
        self.resize(self.track.width() + margin * 2, self.track.height() + margin * 2)
        self.track.reparent(self, QPoint(margin, margin))
        self.connect(self.track, PYSIGNAL('loaded'), self.slotLoaded)
        self.connect(self.track, PYSIGNAL('unload'), self.slotUnload)
        self.connect(self.track, PYSIGNAL('collapsed'), self.slotCollapsed)
        self.connect(self.track, PYSIGNAL('expanded'), self.slotExpanded)
        self.mousePressed = 0
    
    def slotLoaded(self):
        self.emit(PYSIGNAL('loaded'), (self,))
    
    def slotUnload(self):
        self.hide()
        self.emit(PYSIGNAL('unloaded'), (self,))
        self.close(1)
        
    def slotCollapsed(self):
        self.resize(self.track.width() + self.margin*2, self.track.height() + self.margin*2)
        self.emit(PYSIGNAL('collapsed'), (self,))
        
    def slotExpanded(self):
        self.resize(self.track.width() + self.margin*2, self.track.height() + self.margin*2)
        self.emit(PYSIGNAL('expanded'), (self,))
        
    def mousePressEvent(self, e):
        self.mousePressed = 1
        return QFrame.mousePressEvent(self, e)
        
    def mouseReleaseEvent(self, e):
        self.mousePressed = 0
        self.emit(PYSIGNAL('selected'), (self,))
        e.accept()
        
    def mouseMoveEvent(self, e):
        """ Drag a pointer to 'self' """
        if self.mousePressed:
            Globals.dragObject = QTextDrag('PKSampler: dragging a track', self)
            Globals.dragObject.trackFrame = self
            Globals.dragObject.dragCopy()
        
        
class TrackFramePool(QFrame):
    """ Arranges track widgets with group and save controls.
        SIGNALS:
            PYSIGNAL('dropped'), (trackFrame, self, oldParent
            PYSIGNAL('saved'), (self,)
            PYSIGNAL('groupChanged'), (self,)
    """
    
    def __init__(self, parent=None, name=None, f=0):
        """ Insert the track into a frame with margin 'margin'. """
        QFrame.__init__(self, parent, name, f)
        
        self.setAcceptDrops(1)
        self.Layout = QHBoxLayout(self,0,0,"poolLayout")
        
        self.backplate = QFrame(self, 'backplate')
        self.backplate.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.Layout.addWidget(self.backplate)
        
        self.trackFrames = []

    def Add(self, trackFrame):
        if not trackFrame in self.trackFrames:
            # just a little hack to remove it from a previous TrackFramePool
            p = trackFrame.parentWidget()
            if p and p.parentWidget() and \
                   isinstance(p.parentWidget(), TrackFramePool):
                p.parentWidget().Remove(trackFrame)
            trackFrame.reparent(self.backplate, 0, QPoint(-2000, -2000))
        # just reposition it on the end
        else:
            self.trackFrames.remove(trackFrame)
        self.trackFrames.append(trackFrame)
        trackFrame.show()
        self.rearrange()
        
    def Remove(self, trackFrame):
        trackFrame.reparent(None, 0, QPoint(-2000,-2000))
        self.trackFrames.remove(trackFrame)
        self.rearrange()
        
    def GetNewTrackX(self):
        """ Return the width of all the tracks in their current states. 
            This will be depreicated by implicit animation.
        """
        x = 0
        for i in range(len(self.trackFrames)):
            #self.trackFrames[i].move(x, 0)
            x += self.trackFrames[i].width()
        return x
        
    def rearrange(self):
        """ Arrange the tracks. """
        x = 0
        for i, w in enumerate(self.trackFrames):
            w.move(x, 0)
            x += w.width()
        
    def setBackplateColor(self, color):
        self.backplate.setPaletteBackgroundColor(color)
        
    def setBackplatePixmap(self, pixmap):
        self.backplate.setErasePixmap(pixmap)
        
    # Drag and drop
    
    def dragEnterEvent(self, dee):
        """ Whether or not the drag icon will appear to accept it. """
        dee.accept(hasattr(Globals.dragObject, 'trackFrame'))
    
    def dropEvent(self, de):
        """ Add TrackFrame objects, and remove from the previous parent. """
        # dragging a track
        if hasattr(Globals.dragObject, "trackFrame"):
            de.accept()
            trackFrame = Globals.dragObject.trackFrame
            oldParent = trackFrame.parentWidget()
            if oldParent:
                args = (trackFrame, self, oldParent.parentWidget())
            else:
                args = (trackFrame, self, None)
            self.emit(PYSIGNAL('dropped'), (args))
            # not yet used
            #Animation.animate(trackFrame, self, doneFunc=self.slotAnimationDone)
            
    def slotAnimationDone(self, animation, widget):
        """ Not yet used. """
        self.Add(widget)


class SampleGroup(TrackFramePool):
    """ A TrackFramePool that also has grouping controls and functions. """

    class CategoryDialog(CategoryForm):
        """ For selecting the groove category to save to. """
        def __init__(self, parent=None, name=None, modal=False, f=0):
            CategoryForm.__init__(self, parent, name, modal, f)
            
        def slotAccept(self, id):
            """ Called when a category button is clicked. """
            self.category = self.buttonGroup.find(id).text().ascii()
            self.accept()
            
    def __init__(self, parent=None, name='', f=0):
        TrackFramePool.__init__(self, parent, name, f)
        self.sampleGroup = Group.Group()
        QObject.connect(self.sampleGroup, PYSIGNAL('start'),
                        self.slotGroupStart)
        QObject.connect(self.sampleGroup, PYSIGNAL('cue'),
                        self.slotGroupCue)
        QObject.connect(self.sampleGroup, PYSIGNAL('pause'),
                        self.slotGroupPause)
        QObject.connect(self.sampleGroup, PYSIGNAL('unpause'),
                        self.slotGroupPause)
        QObject.connect(self.sampleGroup, PYSIGNAL('pitch'),
                        self.slotGroupPitch)
        QObject.connect(self.sampleGroup, PYSIGNAL('volume'),
                        self.slotGroupVolume)
        
        # the control widget
        self.controlWidget = QFrame(self)
        self.controlWidget.setPaletteBackgroundColor(BACKGROUND_COLOR)
        self.controlWidget.setFrameStyle(FRAME_STYLE)
        self.controlWidget.setSizePolicy(QSizePolicy.Fixed,
                                         QSizePolicy.Expanding)
        self.controlWidget.setMinimumWidth(55)
        
        self.saveButton = PovWidgets.PushButton('save_button', 'red',
                                                self.controlWidget)
        self.saveButton.move(3, 3)
        QToolTip.add(self.saveButton, 'Save this group to a file.')
        QObject.connect(self.saveButton, SIGNAL('clicked()'), self.slotSave)
        
        self.groupButton = PovWidgets.PushButton('auto_group_button',
                                                 'blue', self.controlWidget)
        self.groupButton.move(3,48)
        self.groupButton.setToggleButton(True)
        QToolTip.add(self.groupButton,
                     'Start samples in the group with the next loop.')
        QObject.connect(self.groupButton,SIGNAL('toggled(bool)'),
                        self.setDeepGrouped)
        
        self.groupEditButton = PovWidgets.PushButton('group_edit_button',
                                                     'green',
                                                     self.controlWidget)
        self.groupEditButton.move(3,88)
        QObject.connect(self.groupEditButton, SIGNAL('clicked()'),
                        self.slotGroupEdit)
        
        self.groupLabel = QLabel(self.controlWidget)
        self.groupLabel.setText('Not\nGrouped')
        self.groupLabel.move(3,125)
        self.groupLabel.resize(49, 30)
        self.groupLabel.setAlignment(Qt.AlignCenter)
        
        self.volumeSlider = PovWidgets.MixerSlider('outer_mixerslider', self.controlWidget)
        self.volumeSlider.move(13, 170)
        QToolTip.add(self.volumeSlider, 'Adjust the volume for a group.')
        QObject.connect(self.volumeSlider, SIGNAL('valueChanged(int)'), self.slotVolume)
        self.Layout.addWidget(self.controlWidget)
        
        self.categoryDialog = SampleGroup.CategoryDialog(self)        
        self.volumeSlider.setValue(27)
        
    def Add(self, trackFrame):
        """ Add a TrackFrame to the pool, and its SampleControl to the group. """
        TrackFramePool.Add(self, trackFrame)
        sampleControl = trackFrame.track.sampleControl
        if sampleControl.looping():
            self.sampleGroup.syncWithGroup(sampleControl)
        self.sampleGroup.add(trackFrame.track.sampleControl)
        
    def Remove(self, trackFrame):
        """ Remove a track frame from the pool and its SampleControl from hte group. """
        TrackFramePool.Remove(self, trackFrame)
        self.sampleGroup.remove(trackFrame.track.sampleControl)

    def setDeepGrouped(self, a0):
        """ Enable synchronizing the controls on all samples. """
        self.groupButton.setOn(a0)
        self.sampleGroup.setDeepGrouped(a0)
        
    def getGlobalGroup(self):
        return self.sampleGroup.getGlobalGroup()

    def slotVolume(self, a0):
        """ Called when the volume slider is moved. """
        self.sampleGroup.action('volume', value=a0)
            
    def slotSave(self):
        """ Pop category widget, save the samples in a Globals.GrooveFile """
        if self.categoryDialog.exec_loop() == QDialog.Accepted:
            category = self.categoryDialog.category
            id = str(time.time())
            grooveFile = Globals.GrooveFile(id, category)
            grooveFile.setPitch(self.sampleGroup.groupPitch)
            for frame in self.trackFrames:
                path = frame.track.sampleControl.path
                volume = frame.track.controllerWidget.volumeSlider.value()
                grooveFile.addSample(path, volume)
            grooveFile.save()
            self.emit(PYSIGNAL('saved'), (self,))
        else:
            pass
            
    def slotGroupEdit(self):
        """ pop the group dialog. """
        dialog = GroupDialog(self)
        if dialog.exec_loop() == QDialog.Accepted:
            if dialog.group_id != None:
                # set group
                self.sampleGroup.globalGroupId = dialog.group_id
                self.groupLabel.setText(dialog.group_id)
            else:
                # ungroup
                self.sampleGroup.globalGroupId = None
                self.groupLabel.setText('Not\nGrouped')
            self.emit(PYSIGNAL('groupChanged'), (self,))
    
    # Group slots
    
    def slotGroupStart(self, sampleControl):
        for frame in self.trackFrames:
            track = frame.track
            if track.sampleControl != sampleControl and track.sampleControl.grouped():
                track.controllerWidget.startButton.AnimateClick()
                track.collapsedWidget.startButton.AnimateClick()

    def slotGroupCue(self, sampleControl):
        for frame in self.trackFrames:
            track = frame.track
            if track.sampleControl != sampleControl and track.sampleControl.grouped():
                track.controllerWidget.cueButton.AnimateClick()

    def slotGroupPause(self, sampleControl):
        for frame in self.trackFrames:
            track = frame.track
            if track.sampleControl != sampleControl and track.sampleControl.grouped():
                track.controllerWidget.pauseButton.AnimateClick()
                track.collapsedWidget.pauseButton.AnimateClick()
        
    def slotGroupPitch(self, sampleControl, pitch):
        for frame in self.trackFrames:
            track = frame.track
            if track.sampleControl != sampleControl and track.sampleControl.grouped():
                #track.controllerWidget.pitchSlider.setPixmap(pitch)
                pass
        
    def slotGroupVolume(self, sampleControl, volume):
        for frame in self.trackFrames:
            track = frame.track
            if track.sampleControl != sampleControl and track.sampleControl.grouped():
                track.controllerWidget.volumeSlider.setPixmap(volume)
                track.collapsedWidget.volumeSlider.setPixmap(volume)
            
        

class GroupWidgetStack(PovWidgets.WidgetStack):
    """ A widget stack that gets notified about TrackFramePool group changes. """
    def __init__(self, parent=None, name=None, f=0):
        PovWidgets.WidgetStack.__init__(self, parent, name, f)
        
    def addWidget(self, w, id=-1, button=None):
        PovWidgets.WidgetStack.addWidget(self, w, id, button)
        if w.__class__ == TrackFramePool:
            QObject.connect(w, PYSIGNAL('groupChanged'), 
                            self.slotGroupChange)
        
    def removeWidget(self, w):
        PovWidgets.WidgetStack.removeWidget(self, w)
        if w.__class__ == TrackFramePool:
            del self.trackFramePools[self.find(w)]
            QObject.disconnect(w, PYSIGNAL('groupChanged'),
                               self.slotGroupChange)
        
    def slotGroupChange(self, trackFramePool):
        """ Called when a child' sampleGroup's group gets changed. 
            Change the color of the button to match the 
        """
        id = self.id(trackFramePool)
        button = self.findButton(trackFramePool)
        group_id = trackFramePool.getGlobalGroup()
        color = Globals.group_colors[group_id]
        if button.__class__ == PovWidgets.PushButton:
            button.setColor(color)
        else:
            button.setPaletteBackgroundColor(QColor(color).light(125))
            
            
def test_SampleGroup():
    import pkaudio
    pkaudio.start_server()
    a = QApplication([])
    QObject.connect(a, SIGNAL('lastWindowClosed()'), a.quit)
    t1 = TrackFramePool()
    t1.setBackplateColor(QColor("red"))
    t2 = TrackFramePool()
    t1.show()
    t2.show()
    s1 = TrackFrame()
    s2 = TrackFrame()
    s1.show()
    s2.show()
    a.setMainWidget(t1)
    a.exec_loop()
    
def test_GroupWidgetStack():
    a = QApplication([])
    w = GroupWidgetStack()
    for i in range(5):
        w.addWidget(TrackFramePool())
    w.show()
    a.setMainWidget(w)
    a.exec_loop()

def test_SampleGroup():
    import pkaudio
    pkaudio.start_server()
    a = QApplication([])
    w = SampleGroup()
    s1 = TrackFrame()
    s2 = TrackFrame()
    s1.track.slotLoad('/home/patrick/wav/loops/bd_137.wav')
    s2.track.slotLoad('/home/patrick/wav/loops/hi_drums_137.wav')
    w.Add(s1)
    w.Add(s2)
    w.show()
    w.resize(450,450)
    a.setMainWidget(w)
    a.exec_loop()
    

def test_TrackFramePool():
    import pkaudio
    print 'BLEH'
    from Selector import Selector
    def dropped(frame, pool):
        pool.Add(frame)
    pkaudio.start_server()
    a = QApplication([])
    QObject.connect(a, SIGNAL('lastWindowClosed()'), a.quit)
    t1 = TrackFramePool()
    t2 = TrackFramePool()
    t1.setBackplateColor(QColor("red"))
    QObject.connect(t1, PYSIGNAL('dropped'), dropped)
    QObject.connect(t2, PYSIGNAL('dropped'), dropped)
    t1.resize(400,400)
    t2.resize(400,400)
    t1.show()
    t2.show()
    s1 = TrackFrame()
    s2 = TrackFrame()
    s1.track.slotLoad('/home/patrick/wav/loops/bd_137.wav')
    s2.track.slotLoad('/home/patrick/wav/loops/hi_drums_137.wav')
    s1.show()
    s2.show()
    a.setMainWidget(t1)
    a.exec_loop()


def run_test():
    import sys
    testname = sys.argv[1]
    if testname == 'TrackFramePool':
        test_TrackFramePool()
    elif testname == 'SampleGroup':
        test_SampleGroup()
    elif testname == 'GroupWidgetStack':
        test_GroupWidgetStack()
    else:
        print 'test not found'
        
