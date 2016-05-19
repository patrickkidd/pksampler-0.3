""" Group.py: Controls the automatic starting and stopping of samples,
    and responds to network events.
    
    THE WAY IT SHOULD BE (Phase 1):
        - Samples belong to groups.
        - GroupProxy: A sample listener that signals that knows
        - Look at Group and GroupManagers' methods,
          compare with SampleControl's respective [grouping] methods.
        - Make sure GroupManager should exist, instead of just this module.
    THE WAY IT SHOULD BE (Phase 2):
        - Groups have siblings on other hosts, and respond to each other with
          the accuracy of network latency.
"""

import socket
from qt import *
import Globals
from Queue import Queue
import atexit
from Network import Dispatch
from SampleControl import Listener as SampleListener


net_event_queue = Queue()
manager = None


def Sequencer():
    global manager
    if manager == None:
        manager = GroupManager()
    return manager

def _atexit():
    global manager
    if manager:
        manager.close()
        manager = None
atexit.register(_atexit)


class GroupProxy(SampleListener):
    """ Simply stores which sampleControl sent a signal in the parent pool. 
        One group proxy is created per SampleControl, but more could be
        created if for some reason the sample should be in more groups.

        This shouldn't really be used outside of this module.
    """
    
    def __init__(self, sampleControl, group):
        SampleListener.__init__(self, sampleControl)
        self.group = group
        
    def slotStart(self):
        if self.getSample().grouped():
            self.group.action('start', self.getSample())
        
    def slotCue(self):
        if self.getSample().grouped():
            self.group.action('cue', self.getSample())
        
    def slotPause(self):
        if self.getSample().grouped():
            self.group.action('pause', self.getSample())
        
    def slotUnpause(self):
        if self.getSample().grouped():
            self.group.action('unpause', self.getSample())
            
    def slotPitchChanged(self, pitch):
        if self.getSample().grouped():
            self.group.action('pitch', self.getSample(), pitch)
            
    def slotWaitingForStart(self):
        self.group.doSynchedStart(self.getSample())
            
    
class Group(QObject):
    """ The local realization of a global group of samples.
        These may be linked with global groups accross the network boundary.
        SIGNALS:
            # action == {start, cue, pause, pitch, volume}
            PYSIGNAL(action), (origSampleControl,value) 
    """
    
    last_id = 1
    
    def __init__(self):
        global manager
        Sequencer()
        QObject.__init__(self)
        self.group_id = Group.last_id
        self.globalGroupId = None
        Group.last_id += 1
        
        self.groupProxies = []
        self.groupPitch = 0.0 # used to init added tracks
        self.waitingSamples = []
        self.deepGrouped = 0
        self.originator = None
        
        # register the group
        manager.addGroup(self)
        
    def __del__(self):
        global manager
        if manager:
            manager.removeGroup(self)

    def groupId(self):
        """ Return a unique group identifier. """
        return self.group_id
        
    def setGlobalGroup(self, global_id):
        """ Set which global group this sample group belongs to. 
            None disassociates it with all global groups.
        """
        self.globalGroupId = None
        
    def getGlobalGroup(self):
        return self.globalGroupId

    def getSamples(self):
        """ Return a list of the group's sampleControls. """
        return [g.getSample() for g in self.groupProxies]
        
    def setDeepGrouped(self, a0):
        """ Set a boolean value for whether or not to sync the samples. """
        self.deepGrouped = a0
        for gp in self.groupProxies:
            if a0:
                gp.getSample().setDeepGroup(self.groupId())
            else:
                gp.getSample().setDeepGroup(0)
        
    def getDeepGrouped(self):
        """ Return the value set by setDeepGrouped(). default is false. """
        return self.deepGrouped
        
    def add(self, sampleControl):
        """ Add the sample to this group. """
        if self.deepGrouped:
            sampleControl.setDeepGroup(self.groupId())
        else:
            sampleControl.setDeepGroup(0)
        self.groupProxies.append(GroupProxy(sampleControl, self))
        self.syncWithGroup(sampleControl)
        
    def remove(self, sampleControl):
        """ Remove a sample from this group. """
        for g in self.groupProxies:
            if g.getSample() == sampleControl:
                self.groupProxies.remove(g)
                g.unload()
                break
        sampleControl.setDeepGroup(0)
        
    def syncWithGroup(self, sampleControl):
        """ Sync up the sampleControl's settings with those of this group. """
        # sync with the group
        if sampleControl.grouped():
            sampleControl.slotPitch(self.groupPitch)
        
    def onBeat(self):
        """ Tells the group that a sample has looped. """
        pass
#        if not self.getBeatSynced() or not len(self.waitingSamples):
#            return
#        for sample in self.waitingSamples:
#            sample.forceStart()
#            self.waitingSamples.remove(sample)
#                
    def doSynchedStart(self, sampleControl):
        pass
#        global manager
#        # start the sample if no sample is playing in the global/local group
#        if self.globalGroupId != None:
#            samples = manager.getSamplesForGroup(self.globalGroupId)
#        else:
#            samples = self.getSamples()
#        samples.remove(sampleControl)        
#        something_playing = 0
#        for sample in samples:
#            if sample.isPlaying():
#                something_playing = 1
#                break
#                
#        # testing
#        if not sampleControl in self.waitingSamples:
#            self.waitingSamples.append(sampleControl)
#        return
#        
#        # original code
#        if something_playing == 0:
#            sampleControl.forceStart()
#        else:
#            if not sampleControl in self.waitingSamples:
#                self.waitingSamples.append(sampleControl)

    def action(self, action, sampleControl=None, value=0):
        """ Perform an action on the group. """
        if self.originator != None: # prevent recursion
            return
            
        self.originator = sampleControl
        self.emit(PYSIGNAL(action), (self.originator,value,))
        
        samples = self.getSamples()
        if sampleControl != None:
            samples.remove(self.originator)
        for sample in samples:
            if sample.grouped():
                if action == 'start': 
                    sample.slotStart()
                elif action == 'cue': 
                    sample.slotCue()
                elif action == 'pause': 
                    sample.slotPause()
                elif action == 'unpause': 
                    sample.slotUnpause()
                elif action == 'volume': 
                    sample.slotVolume(value)
                elif action == 'pitch':
                    self.groupPitch = value
                    sample.slotPitch(value)
                
        self.originator = None


class GroupManager(QObject):
    """ Manages everything group related on this host.
        The manager is an event dispatcher and network monitor.
        
        Global groups are stored as identifiers in each SampleGroup, and
        in self.globalGroups for conveinience.
        SocketReader(Thread) -> networkEvent -> postEvent -> event() -> _process*Event
        SIGNALS:
            PYSIGNAL('groupsUpdated'), ()
            PYSIGNAL('hostsUpdated'), ()
    """
    
    def __init__(self):
        QObject.__init__(self)
        self.Groups = []
        self.globalGroups = []
        self.hosts = []
        self.midiCallbacks = []
        self.boundMidiChannels = {}
        self.comm = Dispatch()
        QObject.connect(self.comm, PYSIGNAL('host_up'),
                        self.slotAddHost)
        QObject.connect(self.comm, PYSIGNAL('host_down'),
                        self.slotRemoveHost)
        QObject.connect(self.comm, PYSIGNAL('add_group'),
                        self.slotAddGlobalGroup)
        QObject.connect(self.comm, PYSIGNAL('remove_group'),
                        self.slotRemoveGlobalGroup)
        QObject.connect(self.comm, PYSIGNAL('group_beat'),
                        self.slotGroupBeat)
        QObject.connect(self.comm, PYSIGNAL('local_sample_starting'),
                        self.slotStartEvent)
        QObject.connect(self.comm, PYSIGNAL('midi'),
                        self.slotMidiEvent)
        
        for group in Globals.group_colors:
            self.slotAddGlobalGroup(group)
    
    def close(self):
        """ Kills the local host. """
        self.comm.close()
        manager = None
        
    ## EVENT SLOTS
        
    def slotStartEvent(self, sample_id):
        """ Called by event() when a local sample loops. """
        # find the sample's local group.
        targetGroup = None
        for group in self.Groups:
            for sample in group.getSamples():
                if sample.sampleId() == sample_id:
                    sample.notifyYouStarted()
                    targetGroup = group
                    break
            if targetGroup: break
        
        # send the message to the remote hosts *first*
        if targetGroup != None:
            if targetGroup.globalGroupId != None:
                self.comm.notifyGroupBeat(targetGroup.globalGroupId)
            self.slotGroupBeat(targetGroup.globalGroupId)
        
    def slotMidiEvent(self, data):
        """ If the control is bound to a function, call it,
            then send to all listeners
        """
        for func in self.midiCallbacks:
            func(data)
            
        if not len(self.midiCallbacks) and data[0] in self.boundMidiChannels:
            self.boundMidiChannels[data[0]](data[2])
               
    def slotGroupBeat(self, group_id):
        """ Called when a beat is received for a group. """
        for group in self.Groups:
            if group.globalGroupId == group_id:
                group.onBeat()
                
    def slotAddHost(self, host):
        """ Called when the Dispatch finds a new host. """
        if not host in self.hosts:
            self.hosts.append(host)
        Globals.Print('added host: '+host)
        self.emit(PYSIGNAL('hostsUpdated'), ())

    def slotRemoveHost(self, host):
        """ Called when the Dispatch sees a host go down. """
        if host in self.hosts:
            self.hosts.remove(host)
        Globals.Print('removed host: '+host)
        self.emit(PYSIGNAL('hostsUpdated'), ())
        
    ## public methods
        
    def getHosts(self):
        return self.hosts
        
    def slotAddGlobalGroup(self, global_id):
        """ Top-level entry point for adding a group to all hosts. 
            Called when the Dispatch finds another global group.
        """
        self.comm.notifyAddGroup(global_id)
        if not global_id in self.globalGroups:
            self.globalGroups.append(global_id)
        self.emit(PYSIGNAL('groupsUpdated'), ())
    
    def slotRemoveGlobalGroup(self, global_id):
        """ Top-level entry point for removing a group from all hosts.
            Called by the Dispatch when it sees a group disappear.
            Removes all referencing SampleGroups from the group.
        """
        self.comm.notifyRemoveGroup(global_id)
        if global_id in self.globalGroups:
            self.globalGroups.remove(global_id)
        for group in self.Groups:
            if group.globalGroupId == global_id:
                group.globalGroupId = None
        self.emit(PYSIGNAL('groupsUpdated'), ())
        
    def getSamplesForGroup(self, group_id):
        samples = []
        for group in self.Groups:
            if group.globalGroupId == group_id:
                samples += group.getSamples()
        return samples
                
    def getGlobalGroups(self):
        return self.globalGroups
        
    def addGroup(self, sampleGroup):
        if not sampleGroup in self.Groups:
            self.Groups.append(sampleGroup)
    
    def removeGroup(self, sampleGroup):
        if sampleGroup in self.Groups:
            self.Groups.remove(sampleGroup)
            
    def addMidiListener(self, func, channel=-1):
        """ Call func with for messages with channel, or if channel == -1, 
            call func for all messages.
        """
        if channel != -1:
            self.boundMidiChannels[channel] = func
        elif not func in self.midiCallbacks:
            self.midiCallbacks.append(func)
        
    def removeMidiListener(self, func, channel=-1):
        """ Remove a binding made with addMidiListener. """
        if channel != -1:
            del self.boundMidiChannels[channel]
        elif func in self.midiCallbacks:
            self.midiCallbacks.remove(func)
            
    def removeAllForTrack(self, track):
        """ A track is about to be deleted, so deregister all respective bindings. """
        del_list = []
        for i in self.boundMidiChannels:
            if self.boundMidiChannels[i] == track.controllerWidget.slotVolume:
                del_list.append(i)
        for i in del_list:
            del self.boundMidiChannels[i]
            


def addMidiListener(func, channel=-1):
    global manager
    manager.addMidiListener(func, channel)
    
def removeMidiListener(func, channel=-1):
    global manager
    manager.removeMidiListener(func, channel)

def removeAllForTrack(t):
    global manager
    if manager:
        manager.removeAllForTrack(t)


# module init
#Sequencer()

    
def test_Group():
    import time
    import pkaudio
    from SampleControl import SampleControl
    pkaudio.start_server()
    s1 = SampleControl()
    s2 = SampleControl()
    s1.load("/home/ajole/wav/PS-28/WAV drumloops/WAV basic/28x-drm01-125.wav")
    s2.load("/home/ajole/wav/PS-28/WAV drumloops/WAV basic/28x-drm03-125.wav")
    g = Group()
    g.add(s1)
    g.add(s2)
    s1.setGrouped(True)
    s2.setGrouped(False)
    s1.slotSetZone(0, True)
    s2.slotSetZone(0, True)
    s1.slotLooping(True)
    s2.slotLooping(True)
    
    s1.slotStart()
    time.sleep(2)
    
    for i in range(5):
        s1.slotStart()
        time.sleep(.1)
        
    time.sleep(4)

    
def test_HostCacheServer():
    import time
    server = HostCacheServer()
    time.sleep(1000)


    
    
if __name__ == '__main__':
    test_Grouping()
