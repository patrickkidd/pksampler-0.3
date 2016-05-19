#!/bin/env python
""" All application-global data. """

import sys
import qt
import os


VERSION = "0.3"
PKAUDIO_VERSIONS = ['0.3']

n_cues = 9
FILE_FORMATS = ['wav',
                'ogg',
                #'mp2',
                #'mp3',
                #'ac3',
                ]
default_driver_name = 'null'
default_buffersize = 1024
default_pitch_range = 8
groove_extension = 'pkgroove'
animInterval = 50 # in pixels
n_defaultGroups = 3
group_colors = {'Group 1' : 'red',
                'Group 2' : 'green',
                'Group 3' : 'blue',
                }

BROADCAST_PORT = 20000
ACK_PORT = BROADCAST_PORT + 1

BACKGROUND_COLOR = qt.QColor(136, 136, 136)


psyco = False
try:
    import psyco
except ImportError:
    pass
def psyco_bind(method):
    if psyco:
        psyco.bind(method)


def _mkdir(newdir):
    """works the way a good mkdir should :)
        - already exists, silently complete
        - regular file in the way, raise an exception
        - parent directory(ies) does not exist, make them as well
    """
    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        raise OSError("a file with the same name as the desired " \
                      "dir, '%s', already exists." % newdir)
    else:
        head, tail = os.path.split(newdir)
        if head and not os.path.isdir(head):
            _mkdir(head)
        #print "_mkdir %s" % repr(newdir)
        if tail:
            os.mkdir(newdir)
            Print('Created directory '+newdir)

            
def get_user_home_dir():
    """ Return the users home directory. """
    if 'HOMEPATH' in os.environ:
        return os.path.join(os.environ['HOMEPATH'])
    elif 'HOME' in os.environ:
        return os.path.join(os.environ['HOME'])
    else:
        return '.'
    return path
    
def get_home_dir():
    """ Return an application-specific, writable directory. 
        Create it if it doesn't exist.
    """
    path = get_user_home_dir()
    path = os.path.join(path, '.pk')
    if not os.path.isdir(path):
        _mkdir(path)
    return path
    
def setBackground(qwidget, color):
    """ BACKWARDS COMPATIBILITY """
    if qVersion() < 3:
        qwidget.setBackgroundColor(color)
    else:
        qwidget.setPaletteBackgroundColor(color)

def setBackgroundPixmap(qwidget, pixmap):
    """ BACKWARDS COMPATIBILITY """
    if qVersion() < 3:
        qwidget.setBackgroundPixmap(pixmap)
    else:
        qwidget.setErasePixmap(pixmap)
        
def qVersion():
    """ Returns the qt version in an integer. """
    return int(qt.qVersion()[0])
    
def _print_routine(msg, char):
    diff = 78 - len(msg)
    left = ""
    right = ""
    line = ""
    for i in range(diff / 2):
        left += char
        right += char
    while (len(left) + len(msg) + len(right)) < 78:
        right += char
    for i in range(80):
        line += char
        
    print line
    print left,msg,right
    print line
    print

def begin_routine(msg):
    _PrintRoutine(msg, "*")
    
def end_routine(msg):
    _PrintRoutine(msg + " complete", "+")
    
def Print(text):
    sys.stdout.write('PKSampler: '+text+'\n')
    
def PrintErr(text):
    t = 'PKSampler: *** '+text+'\n'
    sys.stderr.write(t)    
    
def file_supported(path):
    fi = qt.QFileInfo(path)
    ext = fi.extension().ascii().lower()
    return ext in FILE_FORMATS
    
    
    
# engine wrapper stuff
use_null_pkaudio = False


def loadPixmap(path):
    from pov import embedded_pixmaps
    from qt import QPixmap
    return QPixmap(embedded_pixmaps.uic_findImage(path))

def useNullPKAudio(a0):
    global use_null_pkaudio
    use_null_pkaudio = a0

def getPKAudio():
    """ Return a real or null PKAudio module. """
    if use_null_pkaudio:
        import PKAudioNull
        return PKAudioNull
    else:
        try:
            p = PKAudio
        except NameError:
            import pkaudio
            v = pkaudio.version()
            if not v in PKAUDIO_VERSIONS:
                PrintErr('This version of pksampler does not support pkaudio version %s (supported_versions: %s)' % (v, PKAUDIO_VERSIONS))
                sys.exit(1)
        return pkaudio
    
class Singleton:
    """ An abstract singleton superclass. """
    __instance = {}
    def getClassName(self):
        self.__class__.__name__
        
    def hasInstance(self):
        (Singleton.__instance).has_key(self.getClassName())
        
    def __init__(self):
        classname = self.getClassName()
        if self.hasInstance():
            raise Singleton.__instance[self.getClassName()]
            Singeton.__instance[self.getClassName()] = self
        else:
            # this is the one
            print 'new'
            
    def __del__(self):
        if self.hasInstance():
            del Singleton.__instance[self.getClassName()]
            

class DisplayTimer:
    """ Handles calling functions to update all displays
        at once, instead of using lots of timers. 
        This follows the Borg pattern, right?
    """
    
    INSTANCE = None
    INTERVAL = 300
    
    def __init__(self):
        if DisplayTimer.INSTANCE:
            self.__dict__ = DisplayTimer.INSTANCE
        else:
            self.widgets = []
            self.timer = qt.QTimer()
            qt.QObject.connect(self.timer, qt.SIGNAL('timeout()'),
                               self.update)
            self.timer.start(DisplayTimer.INTERVAL)
            DisplayTimer.INSTANCE = self.__dict__
            
    def setInterval(self, ms):
        """  Set the update interval """
        DisplayTimer.INTERVAL = ms
        self.timer.stop()
        self.timer.start(DisplayTimer.INTERVAL)
        
    def getInterval(self):
        return DisplayTimer.INTERVAL
        
    def register(self, f):
        if not f in self.widgets:
            self.widgets.append(f)
            
    def deregister(self, f):
        if f in self.widgets:
            self.widgets.remove(f)
            
    def update(self):
        for w in self.widgets:
            w.updateDisplay()
    psyco_bind(update)
            
displayTimer = DisplayTimer()
            
        
# Groove stuff

        
def get_grooves():
    """ Return a list of [category,id] lists from the groove dir. """
    dir = get_home_dir()
    retval = []
    
    for category in os.listdir(dir):
        if os.path.isdir(os.path.join(dir,category)):
            # find the groove files
            for fname in os.listdir(os.path.join(dir,category)):
            
                if os.path.isfile(os.path.join(dir,category,fname)):
                    if not fname == '..' and not fname == '.':
                        i = fname.rfind('.')
                        ext = fname[i+1:]
                        
                        # for groove files
                        if ext == groove_extension:
                            retval.append([category,fname[:fname.rfind('.')]])
    
    return retval
psyco_bind(get_grooves)


class Persistent:
    """ Defines how persistent, host-independent objects are stored. 
        Subclass this class, fill the self.values dict, and call save().
        Subclasses should add methods to easily modify the self.values dict.
        Data Format: self.values = { 'key:value' : value } 
            -> this avoids key,subkey entries.
    """
    def __init__(self, id, type=None):
        self.id = id
        self.type = type
        self.values = {}
        self.ext = None
        
    def _openFile(self, mode, ext=None):
        """ Open the file with mode, return None on error """
        dir = get_home_dir()
        if self.type != None:
            # save the type as a directory if not None
            dir = os.path.join(dir, self.type)
            if not os.path.isdir(dir):
                if 'w' in mode:
                    _mkdir(dir)
                # read mode and no dir 
                else:
                    return None
                
        path = os.path.join(dir,self.id)
        if self.ext:
            path += '.'+self.ext
        if mode != 'w' and not os.path.isfile(path):
            return None
        return open(path, mode)
            
    def setExtension(self, ext):
        self.ext = ext
        
    def save(self):
        """ Write the file based on id and type.
            Return true on success, false on failure. 
        """
        file = self._openFile('w')
        if file:
            # each key (single-nested dictionary)
            lines = []
            for key in self.values:
                val = self.values[key]
                s = key+'='+str(val)+'\n'
                lines.append(s)
            file.writelines(lines)
            return 1
        else:
            if self.type == None: t = ''
            else: t = self.type
            Print('Could not write groove info for '+t+':'+self.id)
            return 0
    
    def load(self):
        """ Read the file based on the id and type.
            Returns true on success, false on failure.
        """
        file = self._openFile('r')
        if file:
            # read the values, try to find the type
            for line in file.readlines():
                if '=' in line:
                    
                    try:
                        key = line.split('=')[0]
                        value = line.split('=')[1]
                        tmp = value.replace('\n','')
                    except:
                        PrintErr('Error parsing line in config file: '+line)
                    
                    # check the values for numbers
                    try: 
                        tmp = int(tmp)
                    except: 
                        try: 
                            tmp = float(tmp)
                        except: 
                            pass
                        
                    self.values[key] = tmp
                
            return 1
        else:
            return 0

            

class ConfFile(Persistent):
    """ An instance of the configuration.
        The file is loaded upon instantiation.
    """
    def __init__(self):
        import Widgets
        Persistent.__init__(self, 'pksampler')
        self.setExtension('conf')
        self.values = {
            'selector_paths' : '',
            'driver' : default_driver_name,
            'buffersize' : default_buffersize,
            'use_gradients' : 1,
            'pitch_range' : default_pitch_range,
            'main_output' : "",
            'cue_output' : "",
            'DISPLAY_UPDATE_INTERVAL' : DisplayTimer.INTERVAL,
            'use_output_window' : 0,
            'animation_granularity' : Widgets.ANIMATION_COEF,
            }
        self.load()
        
    def addSelectorPath(self, path):
        paths = []
        found = 0
        # no dupes
        paths = self.values['selector_paths'].split(',')
        if path.endswith('/'):
            path = path[:len(path)-1]
        if not path in paths:
            self.values['selector_paths'] += ','+path
        paths_str = self.values['selector_paths']
        if paths_str.startswith(','):
            self.values['selector_paths'] = paths_str[1:]
        
    def removeSelectorPath(self, path):
        paths = self.values['selector_paths'].split(',')
        for p in paths:
            if p == path:
                paths.remove(p)
                break
        paths_str = ''
        for p in paths:
            paths_str += p+','
        paths_str = paths_str[:len(paths_str)-1]
        self.values['selector_paths'] = paths_str

    def getSelectorPaths(self):
        retval = self.values['selector_paths'].split(',')
        if len(retval[0]):
            return retval
        else:
            return []
        
    def setDriver(self, driver):
        self.values['driver'] = driver
        
    def getDriver(self):
        return self.values['driver']
        
    def setBufferSize(self, size):
        self.values['buffersize'] = size
        
    def getBufferSize(self):
        return self.values['buffersize']
        
    def readSampleData(self, sample):
        """ Recall persistent data for 'sample' """
        sample.cues = []
        entry = 'sample:' + sample.path
        
        # new sample
        if not entry in self.values:
            for i in range(n_cues):
                sample.cues.append([0,sample.sample.length()])
            return
            
        # read from file
        else:
            entries = self.values[entry].split(':')
            for e in entries:
                if e != '':
                    vals = e.split(',')
                    start = int(vals[0])
                    end = int(vals[1])
                    sample.cues.append([start,end])
            
    def writeSampleData(self, sample):
        """ Write persistent data in 'sample'. """
        entry = 'sample:' + sample.path
        entry_str = ''
        for i in range(n_cues):
            start = int(sample.cues[i][0])
            end = int(sample.cues[i][1])
            entry_str += str(start)+','+str(end)+':'
        self.values[entry] = entry_str
        
    def setUseGradients(self, a0):
        self.values['use_gradients'] = a0
        
    def getUseGradients(self):
        return self.values['use_gradients']
        
    def setPitchRange(self, range):
        self.values['pitch_range'] = range
    
    def getPitchRange(self):
        return self.values['pitch_range']
        
    def setMainOutput(self, name):
        self.values['main_output'] = name
        
    def getMainOutput(self):
        return self.values['main_output']
        
    def setCueOutput(self, name):
        self.values['cue_output'] = name
        
    def getCueOutput(self):
        return self.values['cue_output']
        
    def getDisplayUpdateInterval(self):
        return self.values['DISPLAY_UPDATE_INTERVAL']
        
    def setDisplayUpdateInterval(self, v):
        self.values['DISPLAY_UPDATE_INTERVAL'] = v
        
    def getUseOutputWindow(self):
        return self.values['use_output_window']
        
    def setUseOutputWindow(self, a0):
        self.values['use_output_window'] = a0

    def setAnimationGranularity(self, i):
        self.values['animation_granularity'] = i

    def getAnimationGranularity(self):
        return int(self.values['animation_granularity'])
        
        
class GrooveFile(Persistent):
    """ A persistent group of samples and their settings.
        Groove files don't really need to be edited, just created and added to.
    """
    
    def __init__(self, id, category):
        Persistent.__init__(self, id, category)
        self.setExtension(groove_extension)
        self.pitch = 64
        
    def setPitch(self, pitch):
        self.values['groove:pitch'] = pitch
        
    def addSample(self, path, volume):
        """ Duplicates are overwritten. """
        self.values[path+':volume'] = volume
    
    def getPitch(self):
        return self.pitch
        
    def getSamples(self):
        """ Returns a dict of samples in the form
                { 'path' : {'volume' : val, 'pitch' : val } } 
        """
        samples = {}
        for entry in self.values:
        
            key1 = entry.split(':')[0]
            key2 = entry.split(':')[1]
            value = self.values[entry]
            
            # groove entries
            if key1 == 'groove':
                self.__dict__[key2] = value
                
            # sample entries
            else:
                path = entry.split(':')[0]
                var = entry.split(':')[1]
                if not path in samples:
                    samples[path] = {}
                samples[path][var] = self.values[entry]
                
        return samples
        
    
    
# module init

dragObject = None

# a test    
if __name__ == '__main__':
    print 'herr'
    class MySing(Singleton):
        pass
    
    s1 = MySing()
    s2 = MySing()
    s1 = None
    s2 = None
    s1 = MySing()
    
    
    
##~ # PK.Sample UNIT TEST
##~ 
##~ from Globals import *
##~ import time
##~ 
##~ e = AppEngine()
##~ PK.setDriver('alsa')
##~ s = PK.Sample('/home/ajole/wav/Ear Cramps/bass_main.wav')
##~ s.outputPort().connect(PK.getMixer().createInput())
##~ s.play()
##~ ##~ # PK.Sample UNIT TEST
##~ 
##~ from Globals import *
##~ import time
##~ 
##~ e = AppEngine()
##~ PK.setDriver('alsa')
##~ s = PK.Sample('/home/ajole/wav/Ear Cramps/bass_main.wav')
##~ s.outputPort().connect(PK.getMixer().createInput())
##~ s.play()
##~ 
##~ time.sleep(100)


##~ # SampleWidget.SampleControl UNIT TEST
##~ 
##~ from Globals import *
##~ from Sample import *
##~ import time
##~ 
##~ s = SampleControl()
##~ s.load('/home/ajole/w3av/Ear Cramps/bass_main.wav')
##~ s.slotStart()
##~ 
##~ time.sleep(100)

