
""" PKSequencer.py: the GUI behind pksequencer.
    Created: Fri Dec  3 13:59:32 2004
    Author: Patrick Kidd patrickkidd@gci.net
    
    In this file you should:
      - Define the graphical representation of your C++ module.
      - Import your C++ module.
"""


import os, os.path
import sys
from qt import *
import Globals
PKAudio = Globals.getPKAudio()
from PKAudio import *
from pkstudio import Rack
from pksequencerform import PKSequencerForm
from Patch import PatchFile

sequencer = None
def getSequencerModule():
    global sequencer
    return sequencer

MAX_TRACKS = 9

# The expanded front view of your module.
class PKSequencerFrontExpandedView(QWidget):
    def __init__(self, parent=None, name=None, f=0):
        QWidget.__init__(self, parent, name, f)
        self.form = PKSequencerForm(self)
        self.resize(700,200)
        
        
# The expanded back view of your module.
class PKSequencerBackExpandedView(QWidget):
    def __init__(self, parent=None, name=None, f=0):
        QWidget.__init__(self, parent, name, f)
        self.label = QLabel('PKSequencer: back expanded', self)
        self.label.move(3,3)
        self.label.resize(400,20)
        
        
# The collapsed front view of your module.
class PKSequencerFrontCollapsedView(QWidget):
    def __init__(self, parent=None, name=None, f=0):
        QWidget.__init__(self, parent, name, f)
        self.label = QLabel('PKSequencer: front collapsed', self)
        self.label.move(3,3)
        self.label.resize(400,20)
        

# The collapsed back view of your module.
class PKSequencerBackCollapsedView(QWidget):
    def __init__(self, parent=None, name=None, f=0):
        QWidget.__init__(self, parent, name, f)
        self.label = QLabel('PKSequencer: back collapsed', self)
        self.label.move(3,3)
        self.label.resize(400,20)
        

# Your rack module has four views.       
class PKSequencer(Rack.ProducerModule):

    def __init__(self, name=None):
        global sequencer
        if sequencer == None:
            sequencer = PKAudio.SequencerModule()
        Rack.ProducerModule.__init__(self, name)
        
        self.collapsedWidget = PKSequencerFrontCollapsedView(self)
        self.expandedWidget = PKSequencerFrontExpandedView(self)
        self.backExpandedWidget = PKSequencerBackExpandedView(self)
        self.backCollapsedWidget = PKSequencerBackCollapsedView(self)
        self.updateView()
        
        self.expandedWidget.resize(700,200)
        self.collapsedWidget.resize(700,200)
        self.backExpandedWidget.resize(700,50)
        self.backCollapsedWidget.resize(700,50)
        
        self.frontForm = self.expandedWidget.form
        QObject.connect(self.frontForm.openButton, SIGNAL('clicked()'), self.slotOpen)
        QObject.connect(self.frontForm.sampleButtonGroup, SIGNAL('toggled(bool)'), self.slotSampleButton)
        
        self.volumeSliders = []
        for i in range(MAX_TRACKS):
            slider = getattr(self.frontForm, 'volumeSlider'+str(i))
            QObject.connect(slider, SIGNAL('valueChanged(int)'), self.slotVolume)
            self.volumeSliders.append(slider)
            
            QObject.connect(self.frontForm.sampleButtonGroup.find(i),
                            SIGNAL('toggled(bool)'),
                            self.slotSampleButton)
        
        # PKAudio module stuff
        self.tracks = []
        self.volumes = []
        self.splitters = []
        driver = Driver()
        for i in range(MAX_TRACKS):
            self.tracks.append(None)
            s = Splitter('splitter '+str(i))
            s.setOutputs(driver.numMixers())
            self.splitters.append(s)
            volumes = []
            for j in range(driver.numMixers()):
                m = driver.getMixer(j)
                v = Volume('volume '+str(i))
                m.connect(v.outputPort())
                s.outputPort(j).connect(v.inputPort())
                volumes.append(v)
            self.volumes.append(volumes)
            
            
    def slotOpen(self):
        fname = QFileDialog.getOpenFileName(
           os.environ['HOME'],
           "Sequencer Patches (*.pkpatch)",
           self,
           "open file dialog",
           "Pick a patch to open")
        if not fname.isNull():
            self.saveFileName = fname.ascii()
        self.loadPatch(fname)
        
    def slotSampleButton(self, on):
        id = self.frontForm.sampleButtonGroup.id(self.sender())
        if on:
            self.tracks[id].play()
        else:
            self.tracks[id].stop()
        
    def loadPatch(self, fname):
        self.patchFile = PatchFile(str(fname))
        self.unloadTracks()
            
        # load new tracks
        track_index = -1
        driver = Driver() # TESTING
        for path in self.patchFile.getFileNames():
            # load a file
            size_mb = os.path.getsize(path) / 1000000
            if size_mb > 10:
                ret = QMessageBox.question(
                        self,
                        'Load big file?',
                        'The file \"'+path+'\" is '+str(size_mb)+'MB\n'+
                        'Do you still want to load it?',
                        QMessageBox.Yes,
                        QMessageBox.No)
                if ret == QMessageBox.No:
                    continue
            # load the track
            track = SequencerTrack(sequencer, path)
            track_index += 1
            # set the tempo
            track.setTempo(self.patchFile.tempo)
            # set the button
            button = self.frontForm.sampleButtonGroup.find(track_index)
            button.setEnabled(1)
            # connect the port
            num = track.numOutputs()
            main_mixer = driver.getMixer(0)
            #if main_mixer:
            #    main_mixer.connect(track.outputPort()) # TESING
            track.outputPort().connect(self.splitters[track_index].inputPort())
            # set the track name
            fname = os.path.basename(path)
            trackname = fname[:fname.rfind('.')]
            QToolTip.add(button, trackname)
            self.tracks[track_index] = track
            
        self.setTempo(self.patchFile.tempo)
        self.expandedWidget.form.nameLabel.setText(self.patchFile.name)
        
    def setTempo(self, tempo):
        self.tempo = tempo
        
    def unloadTracks(self):
        for i, track in enumerate(self.tracks):
            if self.tracks[i]:
                self.tracks[i].outputPort().disconnect()
                self.tracks[i] = None
            self.frontForm.sampleButtonGroup.find(i).setEnabled(0)
    
    def slotVolume(self, val):
        val = 127 - val
        index = self.volumeSliders.index(self.sender())
        for v in self.volumes[index]:
            v.setVolume(val)


widgets = {'PKSequencer': {'outputs': 1, 'properties': [], 'stereotype': 'Producer', 'inputs': 0}}

if __name__ == '__main__':
    a = QApplication(sys.argv)
    PKAudio.connect_to_host(startserver=1)
    w = PKSequencer()
    w.show()
    a.setMainWidget(w)
    a.exec_loop()
