""" Null Interface to PKAudio. """

import os.path
from qt import *

class Static:
    def __init__(self, anycallable):
        self.__call__ = anycallable

class Tracked:
    last_id = 0
    objects = {}
    def __init__(self):
        PK.Tracked.last_id += 1
        self.id = PK.Tracked.last_id
        PK.Tracked.objects[self.id] = self
    def id(self):
        return self.id
    def GetObject(self, i):
        return PK.Tracked.objects[i]
    
class Port(Tracked):
    Input = 0
    Output = 1
    def __init__(self, parent, type, name='null port'):
        PK.Tracked.__init__(self)
        self.parent = parent
        self.type = type
        self.conn = None
    def name(self):
        return ""
    def disconnect(self):
        self.conn = None
    def connect(self, port):
        self.conn = port
    def connection(self):
        return self.conn
    def longName(self):
        return self.parent.name()+"[null port]"
    def write(self, seg):
        pass
    def type(self):
        return self.type
        
class PassivePort(Port):
    def __init__(self, parent, name):
        PK.Port.__init__(self, parent, PK.Port.input, name)
        self.new_data = 1
        self.seg = None
    def write(self, seg):
        self.new_data = 1
        self.seg = seg
    def newData(self):
        tmp = self.new_data
        self.new_data = 0
        return tmp
    def buffer(self):
        return self.seg
        
class Module(Tracked):
    def __init__(self, name):
        PK.Tracked.__init__(self)
        self.name = name
        self.inputs = []
        self.outputs = []
    def name(self):
        return self.name
    def addInput(self, name='input'):
        if name.__class__ == PK.Port:
            self.inputs.append(name)
        else:
            self.inputs.append(PK.Port(self, PK.Port.Input, 'input'))
    def addOutput(self, name='output'):
        if name.__class__ == PK.Port:
            self.outputs.append(name)
        else:
            self.outputs.append(PK.Port(self, PK.Port.Output, 'output'))
    def inputPort(self, i=0):
        return self.inputs[i]
    def outputPort(self, i=0):
        return self.outputs[i]
    def input(self):
        return self.inputs[0]
    def output(self):
        return self.outputs[0]
    def numOutputs(self):
        return len(self.outputs)
    def numInputs(self):
        return len(self.inputs)
        
class Sample(Module):
    def __init__(self, path):
        PK.Module.__init__(self, os.path.basename(path))
        self.pitch = 0.0
        self.addOutput()
        PK._engine.AddModule(self)
    def __del__(self):
        PK._engine.RemoveModule(self)
    def timerEvent(self, te):
        pass
    def play(self):
        print 'PKAudioNull.Sample.Play()'
    def stop(self):
        print 'PKAudioNull.Sample.Stop()'
        pass
    def playAt(self, bpms):
        pass
    def playTimed(self, beats):
        pass
    def isPlaying(self):
        return 0
    def length(self):
        return 1000
    def lengthMS(self):
        return 1000
    def looping(self, looping=None):
        return 0
    def pos(self, pos=None):
        return 0
    def reset(self):
        print 'PKAudioNull.Sample.Reset()'
        pass
    def pitch(self, pitch=None):
        if pitch != None:
            self.pitch = pitch * 1.0
        return self.pitch
    def tempPitch(self, pitch):
        return 0
    def tempo(self, tempo=None):
        return 0
    def mediaTempo(self, tempo=None):
        return 0
    def setStart(self, sample):
        pass
    def setEnd(self, sample):
        pass
    def getStart(self):
        pass        
    def getEnd(self):
        return 0
        
class EffectControl:
    def name(self):
        return 'control'
    def tick(self, v):
        pass
        
class Effect(Module):
    def __init__(self, name):
        PK.Module.__init__(self, name)
        self.addInput('input')
        self.addOutput('output')
        PK._engine.AddModule(self)
    def __del__(self):
        PK._engine.RemoveModule(self)
    def control(self, value):
        return PK.EffectControl()
        
class VolumeEffect(Effect):
    def __init__(self):
        PK.Effect.__init__(self,'volume')
        
class PanEffect(Effect):
    def __init__(self):
        PK.Effect.__init__(self,'pan')
        
class DelayEffect(Effect):
    def __init__(self):
        PK.Effect.__init__(self,'delay')
        
class ReverbEffect(Effect):
    def __init__(self):
        PK.Effect.__init__(self,'reverb')
        
class Mixer(Module):
    def __init__(self, name='Mixer'):
        PK.Module.__init__(self, name)
        self.addOutput('output')
        PK._engine.AddModule(self)
    def __del__(self):
        PK._engine.RemoveModule(self)
    def CcreateInput(self):
        port = PK.PassivePort(self, 'input')
        self.addInput(port)
        return port
        
class PeakModule(Module):
    def __init__(self, name='PeakModule'):
        PK.Module.__init__(self, name)
        self.addOutput('output')
        self.addInput('input')
        
class Engine:
    def __init__(self):
        self.modules = []
        self.driver = PK.Module('RtAudioDriver')
        self.driver.addInput('input')
        self.addModule(self.driver)
        self.mixer = PK.Mixer('Main Mixer')
        self.addModule(self.mixer)
        self.peakModule = PK.PeakModule()
        self.mixer.output().connect(self.driver.input())
    def addModule(self, m):
        self.modules.append(m)
    def removeModule(self, m):
        self.modules.remove(m)
    def numModules(self):
        return len(self.modules)
    def getModule(self, i):
        return self.modules[i]
    def getMixer(self):
        return self.mixer
    def getPeakModule(self, int=0):
        return self.peakModule
    def writeToSocket(self, data, len):
        pass
            
    _engine = Engine()
            
PK._engine = PK.Engine()
def GetMixer():
    return PK._engine.GetMixer()
def getEngine():
    return PK._engine
PK.GetMixer = GetMixer
PK.getEngine = getEngine          
            

class AppEngine:
    pass
    
    
mixer = PK.Mixer('Main Mixer')
mod = PK.Module('module')
mod.addOutput()
mod.output().Connect(mixer.createInput())
print mixer.numInputs()
