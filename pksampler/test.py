import time
#from qt import *
from Globals import *
from SampleWidget import *


##~ e = AppEngine()
##~ PK.setDriver('alsa')
##~ s = SampleControl()
##~ s.load('/home/ajole/wav/Patrick Kidd - Birdman.wav')
##~ s.slotSetZone(1,1)
##~ s.slotStart()
##~ time.sleep(1000)

paths = ['/home/ajole/wav/PS-28/WAV drumloops/WAV livezone/28n-drm01-125.wav',
         '/home/ajole/wav/PS-28/WAV instrumentloops/WAV guitarlicks/28a-gte27-125c.wav',
         '/home/ajole/wav/PS-28/WAV instrumentloops/WAV rhodeslicks/28-rho03-125e.wav',
         '/home/ajole/wav/PS-28/WAV instrumentloops/WAV pianoloops/28b-pne01-125c.wav',
         '/home/ajole/wav/PS-28/WAV drumloops/WAV livezone/28n-drm01-125.wav',
         '/home/ajole/wav/PS-28/WAV instrumentloops/WAV guitarlicks/28a-gte27-125c.wav',
         '/home/ajole/wav/PS-28/WAV instrumentloops/WAV rhodeslicks/28-rho03-125e.wav',
         '/home/ajole/wav/PS-28/WAV instrumentloops/WAV pianoloops/28b-pne01-125c.wav'
         ]
samples = []
volumes = []
sampleControls = []
PK.setDriver('alsa')
for p in paths:
    s = SampleControl()
    sampleControls.append(s)
    s.load(p)
    s.slotLooping(1)
    s.slotVolume(100)
    s.slotSetZone(1,1)
    s.slotStart()
    
    #s = PK.Sample(p)
    #v = PK.VolumeEffect()
    #v.control(0).tick(30)
    #s.outputPort().connect(v.inputPort())
    #v.outputPort().connect(PK.getMixer().createInput())
    #s.setLooping(1)
    #s.play()
    #volumes.append(v)
    #samples.append(s)

e = AppEngine()
time.sleep(2)

#a = QApplication([])
#QObject.connect(a, SIGNAL('lastWindowClosed()'), a.quit)
#a.exec_loop()

