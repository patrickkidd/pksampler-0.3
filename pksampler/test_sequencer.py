""" test_sequencer.py """

import sys
from qt import *
from MainWindow import RackPanel
from pksequencer import pksequencer
import Globals
PKAudio = Globals.getPKAudio()

a = QApplication(sys.argv)
PKAudio.connect_to_host(startserver=1)
w = RackPanel()
seq = pksequencer.pksequencer()
w.rack.addModule(seq)
print pksequencer.getSequencerModule().getTempo()
seq.loadPatch('/home/ajole/140test.pkpatch')
w.show()
a.setMainWidget(w)
a.exec_loop()

print 'exitting'
