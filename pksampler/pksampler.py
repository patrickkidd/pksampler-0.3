#!/bin/env python
""" Usage: %s [options] [normal args]
    options:
        -f --fullscreen             Fullscreen mode (xrandr extension required)
        
        -H [host]  --host=[host]    Connect to host (default: localhost)
        
        --rack -r                   Run pkstudio rack only

"""

import os, os.path
import sys
import thread
import getopt
from qt import *

psyco = False
try:
    import psyco
except ImportError:
    pass


USAGE = __doc__ % (sys.argv[0])


PKSAMPLERDIR = os.path.dirname(sys.argv[0])

try:
    pass
    #import psyco
    #print 'Imported psyco'
    #psyco.full()
except Exception, e:
    print 'Couldn\'t find psyco:', e
    
USE_KDE = False
##~ try:
##~     from kdecore import *
##~     USE_KDE = True
##~     print "PKSampler: Found PyKDE, creating kde application."
##~ except ImportError:
##~     pass

def _splash(splash, text):
    if splash:
        splash.message(text)
        app.processEvents()

USE_XRANDR = False
SCREEN_GEOMETRY = ()
def initScreenRes():
    """ Set the screen res to that of the pksampler. """
    global USE_XRANDR, SCREEN_GEOMETRY
    import Globals
    dw = QDesktopWidget()
    rect = dw.screenGeometry()
    SCREEN_GEOMETRY = (rect.width(), rect.height())
    w, h = SCREEN_GEOMETRY
    if w > 1024 and h > 768:
        Globals.Print("Looking for xrandr ...", )
        if os.system('which xrandr >> /dev/null') == 0:
            USE_XRANDR = True
            if os.system('xrandr -s 1024x768'):
                Globals.PrintErr("Error setting screen resolution to 1024x768")
        else:
            USE_XRANDR = False
            Globals.Print("Install xrandr to automatically adjust screen res")
if psyco:
    psyco.bind(initScreenRes)

def revertScreenRes():
    """ Reset the screen res to that of before initScreenRes() """
    global SCREEN_GEOMETRY, USE_XRANDR
    import Globals
    if USE_XRANDR:
        w, h = SCREEN_GEOMETRY
        cmd = "xrandr -s %dx%d" % (w, h)
        if os.system(cmd):
            Globals.PrintErr("Error setting screen res back to %dx%d" % (w,h))

    
app = None
def main():
    global app
    if USE_KDE:
        about = KAboutData('pksampler', 'myabout', '0.1')
        KCmdLineArgs.init(sys.argv, about)
        app = KApplication()
    else:
        app = QApplication(sys.argv)


    # Command line arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'fhH:', ['fullscreen', 'help', 'host='])
    except Exception, e:
        print 'PKSAMPLER: ',e
        print
        print USAGE
        sys.exit(1)

    host = None
    FULLSCREEN = False
    use_null_pkaudio = False
    for o, a in opts:
        if o in ('--fullscreen', '-f'):
            FULLSCREEN = True
        elif o in ('-H', '--host'):
            host = a
        elif o in ('-n', '--null'):
            use_null_pkaudio = True
        #elif o in ('-h', '--host'):
        #    print USAGE
        #    sys.exit(0)

    import Globals
    
    p = QPixmap(os.path.join(PKSAMPLERDIR, 'splash.png'))
    if not p.isNull():
        splash = QSplashScreen(p, Qt.WDestructiveClose)
        splash.show()
    else:
        print " ** PKSampler: couldn't load splash.png"
        splash = None

    # Sound System
    _splash(splash, "Loading sound system...")
    if use_null_pkaudio:
        Globals.useNullPKAudio(True)
    else:
        Globals.useNullPKAudio(False)
    pkaudio = Globals.getPKAudio()
    if host:
        startserver = False
    else:
        startserver = True
        host = 'localhost'    
    _splash(splash, 'Connecting to audio server...')
    if startserver:
        pkaudio.start_server(realtime=True)
    else:
        pkaudio.connect_to_host(host=host)
    if not pkaudio.connected():
        QMessageBox.critical(None,
                             'Network error',
                             'Could not connect to '+host,
                             QMessageBox.Ok)
        sys.exit(1)
    conf = Globals.ConfFile()
    pitchRange = conf.getPitchRange()

    driver = pkaudio.Driver()
    if driver.numMixers() == None:
        Globals.Print("No audio devices detected")

    # Network stuff
    _splash(splash, "Starting network sequencer...")
    from Grouping import Group
    sequencer = Group.Sequencer()

    # Bringing up window
    _splash(splash, "Building Components ...")
    from MainWindow import MainWindow
    import SampleWidget
    SampleWidget.PITCH_RANGE = conf.getPitchRange()
    conf.save()
    conf = None

    if FULLSCREEN:
        pksampler = MainWindow(None,
                               'PKSampler',
                               Qt.WStyle_Customize | Qt.WStyle_NoBorder)
        pksampler.move(0,0)
    else:
        pksampler = MainWindow()

    # motivated by the exceptions thrown in SampleControl.__del__
    import atexit
    def _atexit():
        pksampler.unloadAllSamples()
    atexit.register(_atexit)

    _splash(splash, "Caching samples...")
    pksampler.fillWidgetCache()

    _splash(splash, "Bringing up main window...")
    app.setMainWidget(pksampler)
    if splash:
        splash.finish(pksampler)
        del splash
            
    if FULLSCREEN:
        initScreenRes()
        
   # Do the rest in a try block so we can still reset the screen res.
    try:
        
        pksampler.show()
        app.exec_loop()
        Globals.Print("shutting down")
        #Globals.PK.setRedirectStdout(0)

    except:
        revertScreenRes()
        raise
    
    revertScreenRes()

if psyco:
    psyco.bind(main)
    
def rack():
    from pkstudio import PKStudio
    
    # this is here so that all extension directories can access this module
    # as easily.
    sys.path.append(os.getcwd())
    
    a = QApplication(sys.argv)
    mainwindow = PKStudio.MainWindow()
    mainwindow.show()
    a.setMainWidget(mainwindow)
    a.exec_loop()

if __name__ == "__main__":
    #import profile
    #profile.run('main()', 'profile_out')
    if '-r' in sys.argv or '--rack' in sys.argv:
        rack()
    main()
    
