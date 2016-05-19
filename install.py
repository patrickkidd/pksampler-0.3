""" install.py: Instalation script for pksampler. 

"""


import sys
import os, os.path
import distutils.sysconfig
import getopt
from pksampler.Globals import VERSION


## CONFIGURATION (internal)

USE_SUDO = True

# versions  of pkaudio to look for.
USE_PKAUDIO_VERSIONS = ['0.3', '0.4']

# where the package is going
MODDIR = distutils.sysconfig.get_python_lib()

# where wrapper scripts are installed
BINDIR = '/usr/local/bin'

# package dir in MODDIR
PKSAMPLERDIR = os.path.join(MODDIR, 'pksampler')

# (shell script, description)
BIN_SCRIPTS = [('pksampler', "PKSampler executable"),
               
               ('pkpatchtool',
                "A Tool for creating PKSequencer patches"),
               ]
PKUTILS_MODULES = [('pkutils.py', 'The main pkutils package'),
           ]
               
# path from pksampler package
PIXMAP_FILE = "pov/embedded_pixmaps.py"

# paths to misc files, relative to the pksampler dir, to be copied
MISC_FILES = ['splash.png',
              'icon.png',
              ]


##################################################
## INTERNAL STORAGE
##################################################

# install information storage
CONFIG_TEXT = \
"""# -*- coding: utf-8 -*-
#
# This module contains the configuration of the pksampler installation
#

_install_config = {
    'PKSAMPLERDIR'    : '%s',
    'BINDIR'          : '%s',
}
"""

ERRMSG = """An internal error occured.  Please report all the output of the program,
including the following traceback, to patrickkidd@gci.net.
"""

ERRORS = 0


PROGNAME = sys.argv[0]


USAGE = """
Usage:
    %s [-b] [-s] [-u | --pkutils] [-h | --help]
       [--uninstall]
where:
       -b dir       where the binaries will be installed
                    (default: %s)
       -s           Don't use sudo to install (default: sudo enabled)
       -u --pkutils Only install pkutils
       -h --help    Display this help.

       --uninstall  Uninstall a previous installation.
"""


# these are used for the informative output at the end of execution
INSTALLED_MODULES = []
INSTALLED_PACKAGES = []
INSTALLED_BINS = []

def usage(rcode):
    """Display a usage message and exit.
       rcode is the return code passed back to the calling process.
    """
    global PROGNAME, BINDIR
    print USAGE % (PROGNAME, BINDIR)

    sys.exit(rcode)


def compilePixmaps():    
    cmd = 'cd pksampler && pyuic -embed pixmaps `find . -name "*.bmp"` `find . -name "*.xpm"` `find . -name "*.png"` > %s'
    cmd = cmd % PIXMAP_FILE
    os.system(cmd)


def installPKUtils():
    global PKUTILS_MODULES, INSTALLED_MODULES
    import pkutils
    pkutils.PK_ACTION("Installing pkutils ...")
    pkutils.PK_ACTION("Compiling pkutils modules ...")
    for fp, desc in PKUTILS_MODULES:
        pkutils.compileFile(fp)
    pkutils.PK_ACTION("Installing pkutils modules ...")
    for fp, desc in PKUTILS_MODULES:
        pkutils.installFile(fp, MODDIR, USE_SUDO)
        INSTALLED_MODULES.append((fp,desc))

def uninstallPKUtils():
    global ERRORS, PKUTILS_MODULES
    print 
    print "Uninstalling pkutils ..."

    for m, desc in PKUTILS_MODULES:
        fp = os.path.join(MODDIR, m)+'c'
        print "Deleting module %s ..." % fp
        if os.path.isfile(fp):
            cmd = "rm -rf %s" % fp
            runSudo(cmd, USE_SUDO)
        else:
            print " ** %s not found in %s" % (m, MODDIR)
            ERRORS += 1
    if ERRORS == 0:
        print "Done"

def installPKSampler():
    from pkutils import checkForPKAudio, checkForQt, PK_ACTION, runSudo
    from pkutils import compileFile, installFile, makeSudoDirs, doWrappers
    from pkutils import copyToFile
    
    if not checkForQt():
        sys.exit(1)

    if not checkForPKAudio(USE_PKAUDIO_VERSIONS, [BINDIR]):
        sys.exit(1)
    
    #PK_ACTION("Compiling pixamp data")
    #compilePixmaps()
    #print "Done"

    PK_ACTION("Installing python package to %s ..." % PKSAMPLERDIR)

    PK_ACTION("Deleting old installation")
    # delete existing installation
    if os.path.isdir(PKSAMPLERDIR):
        runSudo("rm -rf %s" % PKSAMPLERDIR, USE_SUDO)
        
    packages = []
    modules = []
    
    # find all packages
    for line in os.walk('pksampler'):
        package = line[0]
        if os.path.isfile(os.path.join(package, '__init__.py')):
            packages.append(package)
            # each module in package
            for fn in line[2]:
                if fn.endswith('.py'):
                    modules.append(os.path.join(package, fn))
    
    packages.sort()
    modules.sort()
    
    PK_ACTION("Compiling python modules ...")

    for m in modules:
        compileFile(m)

    PK_ACTION("Installing python modules ...")
    
    # create the packages
    for p in packages:
        package = os.path.join(MODDIR,p)
        print 'Creating %s' % package
        makeSudoDirs(package, '0755')
    INSTALLED_PACKAGES.append((PKSAMPLERDIR, 'pksampler applcation package'))
        
    # copy the compiled modules
    for m in modules:
        installFile(m, MODDIR, USE_SUDO)
        
    # copy misc files
    for fn in MISC_FILES:
        runSudo("cp %s %s" % (os.path.join('pksampler', fn), PKSAMPLERDIR),
                USE_SUDO)

    doWrappers(BIN_SCRIPTS, PKSAMPLERDIR, BINDIR)
    global INSTLLED_BINS
    for i in BIN_SCRIPTS:
        INSTALLED_BINS.append(i)

    PK_ACTION("Generating uninstall config ...")

    # write config for uninstall
    text = CONFIG_TEXT % (PKSAMPLERDIR, BINDIR)
    copyToFile('pksamplerconfig.py', text)
    print "Created pksamplerconfig.py"



def uninstallPKSampler():

    try:
        from pksamplerconfig import _install_config
    except ImportError:
        print
        print " ** Cannot find install config. You must install before you can uninstall."
        print
        return 1

    from pkutils import PK_ACTION, runSudo

    global BIN_SCRIPTS, ERRORS
    PKSAMPLERDIR = _install_config['PKSAMPLERDIR']
    BINDIR = _install_config['BINDIR']

    
    print 
    print "Uninstalling pksampler ..."

    PK_ACTION("Deleting package in %s ..." % PKSAMPLERDIR)
    if os.path.isdir(PKSAMPLERDIR):
        cmd = "rm -rf %s" % PKSAMPLERDIR
        runSudo(cmd, USE_SUDO)
        print "Done"
    else:
        print " ** PKSampler package not found in " + PKSAMPLERDIR
        ERRORS += 1


    PK_ACTION("Removing executable scripts ...")

    for name, desc in BIN_SCRIPTS:
        fp = os.path.join(BINDIR,name)
        if os.path.isfile(fp):
            print "Deleting %s" % fp
            cmd = 'rm %s' % fp
            runSudo(cmd, USE_SUDO)
        else:
            print " ** The file",fp,"does not exist (continuing)"
            ERRORS += 1

    os.system('rm -rf pksamplerconfig.py*')

    print
    print "*******************************************************************"
    print "*******************************************************************"
    print
    if ERRORS:
        print "Uninstall complete (%d errors)" % ERRORS
    else:
        print "PKSampler uninstalled"
    print
    print


def printCompletion():
    global INSTALLED_MODULES, INSTALLED_BINS, INSTALLED_PACKAGES
    print
    print "*******************************************************************"
    print "*******************************************************************"
    print
    print "Installation complete"
    print
    if len(INSTALLED_PACKAGES):
        print "Packages installed:"
        print 
        for name, desc in INSTALLED_PACKAGES:
            print "  %s\n    - %s\n" % (os.path.join(BINDIR, name), desc)
        print
    if len(INSTALLED_MODULES):
        print "Modules installed:"
        print
        for name, desc in INSTALLED_MODULES:
            print "  %s\n    - %s\n" % (os.path.join(MODDIR, name), desc)
        print
    if len(INSTALLED_BINS):
        print "Executables installed:"
        print 
        for name, desc in INSTALLED_BINS:
            print "  %s\n    - %s\n" % (os.path.join(BINDIR, name), desc)
        print
    print 'Please contact patrickkidd@gci.net with any problems/comments.'
    print
    print "*******************************************************************"
    print "*******************************************************************"
    print
    


def main():
    global BINDIR, BIN_SCRIPTS, USE_SUDO

    # get options
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "bhu", ['help',
                                                           'uninstall',
                                                            'pkutils',
                                                            ])
        for opt, arg in optlist:
            if opt == "-b":
                if os.path.isdir(arg):
                    BINDIR = arg
                else:
                    print 'Invalid binary directory:',arg
            elif opt == "-s":
                USE_SUDO = False
            elif opt == "-h" or opt == "--help":
                usage(0)
            elif opt == "-u" or opt == "--pkutils":
                installPKUtils()
                printCompletion()
                return
            elif opt == "--uninstall":
                uninstallPKUtils()
                return uninstallPKSampler()
    except getopt.GetoptError:
        usage(1)

    print 
    print "Installing pksampler-%s ..." % VERSION
    
    print "Looking for sudo: ",
    sys.stdout.flush()
    if os.system('which sudo') == 0:
        USE_SUDO = True
    else:
        print "Cannot find sudo, you must be root to install."
        USE_SUDO = False

    installPKUtils()

    # install
    try:
        installPKSampler()
    except KeyboardInterrupt:
        print "Installation aborted"
        raise
    except SystemExit:
        raise
    except:
        print ERRMSG
        raise
    printCompletion()
    
if __name__ == "__main__":
    main()
