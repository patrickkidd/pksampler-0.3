#!/bin/env python
""" The visual representation of a track.
    The parent (Track) contains either a disabled track or an enabled track.
    
    # in case we want to do clock stuff
    msecs = value
    posSecs = int(msecs) / 1000
    clockSecs = posSecs % 60
    clockMins = posSecs / 60
"""

import os.path
import fpformat
from qt import QObject, QTimer, SIGNAL, PYSIGNAL
import Globals
import pkaudio
pkaudio = Globals.getPKAudio()

# User vars
PITCH_RANGE = 8 # range of the slider
PITCH_RES = 75  # time res that the pitch buttons react to
PITCH_INC = 1   # bend delta increment
PITCH_MAX = 7   # percent deltas


cueMixer = None
mainMixer = None


class SampleControl(QObject):
    """ Manages a sample's port connections and emits signals when it has changed.
        SIGNALS:
            PYSIGNAL('loaded'), ()
            PYSIGNAL('unloaded'), ()
            PYSIGNAL('volumeChanged'), (vol,)
            PYSIGNAL('start'), ()
            PYSIGNAL('pause'), (pos,)
            PYSIGNAL('unpause'), (pos,)
            PYSIGNAL('cue'), ()
            PYSIGNAL('cueChanged'), (cue,)
            PYSIGNAL('positionChanged'), (pos,)
            PYSIGNAL('reverbChanged'), (rev,)
            PYSIGNAL('delayChanged'), (del,)
            PYSIGNAL('looping'), (bool,)
            PYSIGNAL('pitchChanged'), (pitch,)
            PYSIGNAL('midiPitchChanged'), (pitch, )
            PYSIGNAL('grouped'), (grouped,)
            PYSIGNAL('zoneChanged'), (zone, a0)
            # slotStart called, awaiting forceSlotStart()
            PYSIGNAL('waitingForStart'), ())
    """
    
    def __init__(self):
        """ sample -> splitter |-> volume -> pan -> muter -> mixers[0]
                               |-> volume -> pan -> muter -> mixers[1]
                               |                   ...
                               |-> volume -> pan -> mute from globals import *
        """
        QObject.__init__(self)
        
        self.sample = None
        self.currentCue = 0
        self.cues = []
        self.groupingEnabled = 0
        self.beatSynced = 0
        self.pitchRange = PITCH_RANGE
        self.savedPitchRange = 0
        
        self.driver = pkaudio.Driver()
        # Pitch : when real/temp pitch match, pitch is not bent
        self.pitchTimer = QTimer(self)
        QObject.connect(self.pitchTimer, SIGNAL("timeout()"),
                        self.slotDoPitchBend)
        self.pitchTemp = 0.0 # the bent pitch
        self.realPitch = 0.0 # the original pitch
        self.pitchDirection = "back"
        self.path = None
        
        self.splitter = pkaudio.Splitter()
        
        # Effect chains
        effectChain0 = {}
        effectChain1 = {}
        self.effectChains = [effectChain0, effectChain1]

        # connect eveything up
        for i, chain in enumerate(self.effectChains):

            chain['volume'] = pkaudio.Volume()
            chain['pan'] = pkaudio.Pan()
            chain['peak'] = pkaudio.PeakModule()
            chain['muter'] = pkaudio.Muter()
            chain['muter'].setOn(0)
            
            chain['volume'].outputPort().connect(chain['pan'].inputPort())
            chain['pan'].outputPort().connect(chain['peak'].inputPort())
            chain['peak'].outputPort().connect(chain['muter'].inputPort())
            if i != 1:
                self.splitter.outputPort(i).connect(chain['volume'].inputPort())
            else:
                self.splitter.outputPort(i).connect(chain['pan'].inputPort())
        
        self.effectChains[0]['volume'].setProperty('volume', 75)
        self.slotConnectMixers()
        
    def __del__(self):
        for chain in self.effectChains:
            if chain['muter'].outputPort() != None:
                chain['muter'].outputPort().disconnect()
            self.unload()

        
    def load(self, path):
        """ Load the file and persistent data at 'path'. """
        try:
            self.sample = pkaudio.Sample(path)
        except pkaudio.FileError:
            Globals.Print('Could not open '+path)
            self.sample = None
            return
            
        self.path = path
        conf = Globals.ConfFile()
        conf.readSampleData(self)
        
        # set cue points
        if len(self.cues):
            self.sample.setProperty('start', self.cues[self.currentCue][0])
            self.sample.setProperty('end', self.cues[self.currentCue][1])
        else:
            self.sample.setProperty('start', 0)
            self.sample.setProperty('end', self.sample.length())
            
        # Set looping on samples < 300 secs (5 min)
        if self.sample.length() < 13230000:
            self.slotLooping(1)
        self.sample.outputPort().connect(self.splitter.inputPort())
        self.emit(PYSIGNAL('loaded'), ())
    
    def isLoaded(self):
        """ Returns true if the sample is loaded and can be played. """
        return self.sample and True or False
        
    def unload(self):
        """ Delete the sample, saves persistent data. """
        if self.isLoaded():
            conf = Globals.ConfFile()
            conf.writeSampleData(self)
            conf.save()
            conf = None
            self.sample = None
            self.emit(PYSIGNAL('unloaded'), ())
            self.path = None

    def getShortName(self):
        bn = os.path.basename(self.path)
        return bn[:bn.rfind('.')]
            
    def getPeak(self):
        chain = self.effectChains[0]
        return (chain['peak'].right() + chain['peak'].left()) / 1.5
            
    def sampleId(self):
        """ Return he id of the sample, or -1 if no sampfrom Globals import * """
        if self.sample:
            return self.sample.id()
        else:
            return -1
            
    def isPlaying(self):
        if self.sample:
            return self.sample.isPlaying()
        else:
            return False
        
    def pos(self):
        if self.sample:
            return self.sample.pos()
        else:
            return 0
            
    def getLength(self):
        if self.sample:
            return self.sample.length()
        else:
            return 0

    def getVolume(self, zone=0):
        """ Return the volume for the passed zone. """
        if not zone in self.effectChains:
            zone = 0
        return self.effectChains[zone]['volume'].getProperty('volume')
        
    def setVolume(self, vol, zone=0):
        """ Just set the volume, don't emit the signal. """
        if not zone in self.effectChains:
            zone = 0
        self.effectChains[0]['volume'].setProperty('volume', vol)
        
    def slotVolume(self, a0):
        """ Called by the slider. 0 <= a0 <= 127. """
        a0 = 127 - a0
        volume = int((a0 * 100) / 127)
        self.setVolume(volume)
        self.emit(PYSIGNAL('volumeChanged'), (volume,))

    def setGrouped(self, a0):
        """ Set whether the sample should be consdered part of a group.
            This value can be used for anything.
        """
        self.emit(PYSIGNAL('grouped'), (a0,))
        self.groupingEnabled = a0
        return self.groupingEnabled
        
    def grouped(self):
        return self.groupingEnabled

    def setDeepGroup(self, id):
        """ Tell the C++ code that it manages this sample's grouping. """
        if self.sample:
            self.sample.setGroup(int(id))
        
    def slotStart(self):
        """ Starts playing the sample from the cue point. """
        if self.sample:
            # the delay
            if self.sample.getGroup() > 0:
                self.startDeepSync()
            else:
                self.forceStart()
                                
    def startDeepSync(self):
        """ Start using the more accurate C++ group.   """
        if self.sample and self.sample.getGroup() > 0:
            self.sample.startWithGroup()

    def notifyYouStarted(self):
        """ Get all the widgets rolling a/i the sample started.
            This will usually get called as a callback from startDeepSync().
            """
        self.emitStarted()
    
    def forceStart(self):
        """ Just start now. """
        if self.sample:
            self.slotCue()
            self.sample.play()
            self.emitStarted()
            
    def emitStarted(self):
        """ Just emit the signal w/o starting the stream. """
        if self.sample:
            self.emit(PYSIGNAL('start'), ())
                
    def slotPause(self):
        """ Pauses/UnPauses the sample. """
        if self.sample:
            if self.sample.isPlaying():
                self.sample.stop()
                self.emit(PYSIGNAL('pause'), (self.sample.pos(), ))
            else:
                self.sample.play()
                self.emit(PYSIGNAL('unpause'), (self.sample.pos(), ))
                
    def slotUnpause(self):
        """ Pauses/UnPauses the sample. """
        if self.sample:
            if not self.sample.isPlaying():
                self.sample.play()
                self.emit(PYSIGNAL('unpause'), (self.sample.pos(), ))
        
    def slotCue(self):
        """ Plays or stops the play object """
        if self.sample:
            self.sample.stop()
            self.sample.reset()
            self.emit(PYSIGNAL('cue'), ())
            
    def slotSearch(self, pos):
        """ Set the location of the sample. """
        if self.sample:
            self.sample.pos(pos)
            self.emit(PYSIGNAL('positionChanged'), (pos,))
            
    def slotCuePoint(self, index):
        """ Sets the current cue point. """
        if index < 0:
            index = 0
        elif index >= Globals.n_cues:
            index = Globals.n_cues-1
        if index != self.currentCue and self.sample:
            self.currentCue = index
            self.sample.setProperty('start', self.cues[self.currentCue][0])
            self.sample.setProperty('end', self.cues[self.currentCue][1])
            self.emit(PYSIGNAL('cueChanged'), (self.currentCue,))
            
    def slotReverb(self, v):
        #if self.reverb.numControls():
        #    self.reverb.control(0).tick(v)
        self.emit(PYSIGNAL('reverbChanged'), (v,))
        
    def slotDelay(self, v):
        #if self.delay.numControls():
        #    self.delay.control(1).tick((v/127.0) * 5)
        self.emit(PYSIGNAL('delayChanged'), (v,))
        
    def slotLooping(self, a0):
        """ Set looping to a0. """
        if self.sample:
            self.sample.setLooping(a0)
            self.emit(PYSIGNAL('looping'), (a0,))
        
    def slotPitchUp(self):
        """ Starts bending the pitch up. """
        if self.sample:
            self.pitchDirection = "up"
            self.pitchTemp = self.sample.getPitch()
            self.pitchTimer.stop()
            self.pitchTimer.start(PITCH_RES)

    def slotPitchDown(self):
        """ Starts bending the pitch down. """
        if self.sample:
            self.pitchDirection = "down"
            self.pitchTemp = self.sample.getPitch()
            self.pitchTimer.stop()
            self.pitchTimer.start(PITCH_RES)
            
    def slotPitchStop(self):
        """ Starts bending the pitch back to normal. """
        self.pitchDirection = "back"
            
    def slotDoPitchBend(self):
        """ Does the pitch bend, called by the pitch timer. """
        if self.sample:
            if self.pitchDirection == "up":
                if self.pitchTemp < self.realPitch + PITCH_MAX:
                    self.pitchTemp += PITCH_INC
            
            elif self.pitchDirection == "down":
                if self.pitchTemp > self.realPitch - PITCH_MAX:
                    self.pitchTemp -= PITCH_INC
                
            elif self.pitchDirection == "back":
                if self.pitchTemp == self.realPitch:
                    self.pitchTimer.stop()
                # adjust it
                else:
                    # done
                    if abs(self.pitchTemp - self.realPitch) < PITCH_INC:
                        self.pitchTemp = self.realPitch
                        self.pitchTimer.stop()
                    # rolling up
                    elif self.pitchTemp < self.realPitch:
                        self.pitchTemp += PITCH_INC
                    #rolling down
                    elif self.pitchTemp > self.realPitch:
                        self.pitchTemp -= PITCH_INC
            
            self.sample.setPitch(self.pitchTemp)
            self.emit(PYSIGNAL('pitch'), ())        

    def slotNudgeUp(self):
        """ Nudges the pitch setting up. """
        if self.sample:
            if self.pitchTemp != self.realPitch:
                # then the pitch is being bent,
                # just set the real pitch
                self.realPitch += .02
                self.emit(PYSIGNAL('pitchChanged'), (self.realPitch,))
            else:
                self.slotPitch(self.sample.getPitch() + .02)

    def slotNudgeDown(self):
        """ Nudges the pitch setting down. """
        if self.sample:
            if self.pitchTemp != self.realPitch:
                # then the pitch is being bent,
                # just set the real pitch
                self.realPitch -= .02
                self.emit(PYSIGNAL('pitchChanged'), (self.realPitch,))
            else:
                self.slotPitch(self.sample.getPitch() - .02)
        
    def slotPitch(self, pitch):
        """ Pass a floating point value.
            pitch should be in PK::DJEngine range.
        """
        # self.pitchLabel.setText(str(fpformat.fix(pitch, 2)) + "%")
        if self.sample:
            self.sample.setPitch(pitch)
            self.realPitch = self.sample.getPitch()
            self.emit(PYSIGNAL('pitchChanged'), (self.sample.getPitch(),))
        
    def slotMidiPitch(self, a0):
        """ Pass a midi value. """
        self.emit(PYSIGNAL('midiPitchChanged'), (a0,))
        a0 = 127 - a0
        if a0 >= 64:
            a0 -= 1
            pitch = self.pitchRange - (a0 / 63.0) * self.pitchRange
        elif a0 < 63:
            pitch = (self.pitchRange - (1 - ((a0 - 63) / 63.0)) * self.pitchRange) * -1
        else:
            pitch = 0.0
            
        self.slotPitch(pitch)
        
    def slotSetZone(self, zone, a0):
        """ Toggles the mute on a mixer. """
        if zone < len(self.effectChains):
            self.effectChains[zone]['muter'].setOn(a0)
            self.emit(PYSIGNAL('zoneChanged'), (zone, a0,))
        else:
            Globals.PrintErr('SampleControl.setZone: no such zone: '+str(zone))

    def getZone(self, zone):
        if zone < len(self.effectChains):
            return self.effectChains[zone]['muter'].isOn()
        else:
            Globals.PrintErr('SampleControl.setZone: no such zone: '+str(zone))
        
    def getPitch(self):
        """ Return a floating point value. """
        if self.sample:
            return self.sample.getPitch()
        else:
            return 0.0

    def looping(self):
        if self.sample and self.sample.getLooping():
            return True
        else:
            return False
            
    def atEnd(self):
        if self.sample:
            return self.sample.atEnd()
        else:
            return True
            
    def setPitchRange(self, r):
        """ set the pitch range of the sample. """
        self.savedPitchRange = 1
        self.pitchRange = r
        
    def slotConnectMixers(self):
        """ Connect the effect chains to the mixers. 
            Initialize mainMixer, cueMixer if necessary.
        """
        global mainMixer, cueMixer
        for i, chain in enumerate(self.effectChains):
            if self.driver.numMixers() > i:
                if i == 0:
                    if mainMixer == None:
                        mainMixer = self.driver.getMixer(0)
                    mainMixer.connect(self.effectChains[0]['muter'].outputPort())
                elif i == 1:
                    if cueMixer == None:
                        cueMixer = self.driver.getMixer(1)
                    cueMixer.connect(self.effectChains[1]['muter'].outputPort())
                else:
                    self.driver.getMixer(i).connect(self.effectChains[i]['muter'].outputPort())
    


class Listener:
    """ Responds to events form a SampleControl. """
    def __init__(self, sample):
        self.sample = sample

        QObject.connect(self.sample, PYSIGNAL('volumeChanged'),
                        self.slotVolume)
        QObject.connect(self.sample, PYSIGNAL('start'),
                        self.slotStart)
        QObject.connect(self.sample, PYSIGNAL('pause'),
                        self.slotPause)
        QObject.connect(self.sample, PYSIGNAL('unpause'),
                        self.slotUnpause)
        QObject.connect(self.sample, PYSIGNAL('cue'),
                        self.slotCue)
        QObject.connect(self.sample, PYSIGNAL('cueChanged'),
                        self.slotCueChanged)
        QObject.connect(self.sample, PYSIGNAL('positionChanged'),
                        self.slotPositionChanged)
        QObject.connect(self.sample, PYSIGNAL('reverbChanged'),
                        self.slotReverbChanged)
        QObject.connect(self.sample, PYSIGNAL('delayChanged'),
                        self.slotDelayChanged)
        QObject.connect(self.sample, PYSIGNAL('looping'),
                        self.slotLooping)
        QObject.connect(self.sample, PYSIGNAL('pitchChanged'),
                        self.slotPitchChanged)
        QObject.connect(self.sample, PYSIGNAL('midiPitchChanged'),
                        self.slotMidiPitchChanged)
        QObject.connect(self.sample, PYSIGNAL('grouped'), 
                        self.slotGrouped)
        QObject.connect(self.sample, PYSIGNAL('zoneChanged'),
                        self.slotZoneChanged)
        QObject.connect(self.sample, PYSIGNAL('waitingForStart'),
                        self.slotWaitingForStart)

    def unload(self):
        QObject.disconnect(self.sample, PYSIGNAL('volumeChanged'),
                           self.slotVolume)
        QObject.disconnect(self.sample, PYSIGNAL('start'),
                           self.slotStart)
        QObject.disconnect(self.sample, PYSIGNAL('pause'),
                           self.slotPause)
        QObject.disconnect(self.sample, PYSIGNAL('unpause'),
                           self.slotUnpause)
        QObject.disconnect(self.sample, PYSIGNAL('cue'),
                           self.slotCue)
        QObject.disconnect(self.sample, PYSIGNAL('cueChanged'),
                           self.slotCueChanged)
        QObject.disconnect(self.sample, PYSIGNAL('positionChanged'),
                           self.slotPositionChanged)
        QObject.disconnect(self.sample, PYSIGNAL('reverbChanged'),
                           self.slotReverbChanged)
        QObject.disconnect(self.sample, PYSIGNAL('delayChanged'),
                           self.slotDelayChanged)
        QObject.disconnect(self.sample, PYSIGNAL('looping'),
                           self.slotLooping)
        QObject.disconnect(self.sample, PYSIGNAL('pitchChanged'),
                           self.slotPitchChanged)
        QObject.disconnect(self.sample, PYSIGNAL('midiPitchChanged'),
                           self.slotMidiPitchChanged)
        QObject.disconnect(self.sample, PYSIGNAL('grouped'), 
                           self.slotGrouped)
        QObject.disconnect(self.sample, PYSIGNAL('zoneChanged'),
                           self.slotZoneChanged)
        QObject.disconnect(self.sample, PYSIGNAL('waitingForStart'),
                           self.slotWaitingForStart)
        self.sample = None

    def getSample(self):
        return self.sample

    def slotVolume(self, v):
        pass
        
    def slotStart(self):
        pass
              
    def slotPause(self, pos):
        pass
    
    def slotUnpause(self, pos):
        pass

    def slotCue(self):
        pass

    def slotCueChanged(self, cue):
        pass

    def slotPositionChanged(self, pos):
        pass

    def slotReverbChanged(self, rev):
        pass

    def slotDelayChanged(self, v):
        pass

    def slotLooping(self, on):
        pass

    def slotPitchChanged(self, pitch):
        pass

    def slotMidiPitchChanged(self, pitch):
        pass

    def slotGrouped(self, grouped):
        pass

    def slotZoneChanged(self, zone, on):
        pass

    def slotWaitingForStart(self):
        pass


    
def main():
    import time
    pkaudio.connect_to_host()
    
    l = []
    for i in range(4):
        w = SampleControl()
        w.load('/home/ajole/wav/Patrick Kidd - Birdman.wav')
        l.append(w)
    print 'exitting'


_list = []
def test():
    from qt import QWidget
    class W(QWidget):
        def __init__(self):

            QWidget.__init__(self)
    
    def create():
        global _list
        s = SampleControl()
        s.load('/home/ajole/wav/trance.wav')
        s.slotStart()
        s.slotSetZone(0, True)
        _list.append(s)
    
    import pkaudio
    from qt import QApplication, QPushButton, QObject, SIGNAL
    pkaudio.connect_to_host(startserver=0)
    a = QApplication([])

    w1 = SampleControl()
    w1.load('/home/ajole/wav/track.wav')
    w1.slotStart()
    w1.slotSetZone(0, True)

    b = QPushButton('create', None)
    QObject.connect(b,
                    SIGNAL('clicked()'),
                    create)
    b.show()
    a.setMainWidget(b)
    a.exec_loop()

def test_tearDown():
    """ test the deletion of a SampleControl """
    import pkaudio
    import time
    #pkaudio.DEBUG = True
    pkaudio.start_server()
    s = SampleControl()
    s.load('/home/ajole/wav/track.wav')
    time.sleep(4)

    

if __name__ == "__main__":
    test_tearDown()
