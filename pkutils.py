import sys
import os, os.path
import imp
import compiler
import compileall

# the list of pkaudio modules
PKAUDIO_MODULES = ['pkaudiocore',
                   'pkaudio',
                   ]


def PK_ACTION(s):
    print
    print ">>",s
    print


def PK_CERR(*s):
    print ' **',
    for i in s:
        print '',i,
    print
    print
    
def runSudo(cmd, use_sudo):
    if use_sudo:
        cmd = "sudo " + cmd
    ret = os.system(cmd)
    if ret:
        sys.exit(1)

def makeSudoDirs(name, mode=0755):
    """ Sort of like os.makedirs, but use sudo. 
        This is derived from 'os.makedirs'.
    """
    head, tail = os.path.split(name)
    if not tail:
        head, tail = os.path.split(head)
    if head and tail and not os.path.exists(head):
        makeSudoDirs(head, mode)
    runSudo("mkdir %s" % name, True)
    runSudo("chmod %s %s" % (str(mode), name), True)


def copyToFile(name, text):
    """Copy a string to a file.

    name is the name of the file.
    text is the contents to copy to the file.
    """
    f = open(name,"w")
    f.write(text)
    f.close()


def execCmd(cmd):
    """ Runs a cmd and returns its (status, stdout).
    The trailing newline is removed from the output for convenience.
    NOTE: This function runs a loop calling poll(), which does not block,
    so it should only be used for short-running programs, like `gcc -v`,
    or `echo 'hey'`.
    """
    import popen2
    buf = ''
    proc = popen2.Popen4(cmd)
    status = proc.poll()
    while status == -1:
        status = proc.poll()
    buf += proc.fromchild.read()
    if buf[-1] == '\n':
        buf = buf[:-1]
    return (status, buf)


def installFile(fp, targetdir, use_sudo=True):
    print "Copying %s" % fp+'c'
    dest = os.path.join(targetdir, fp)
    fp = fp+'c'
    dest = dest + 'c'
    cmd = "cp %s %s" % (fp, dest)
    runSudo(cmd, use_sudo)


def compileFile(fp):
    print "Compiling %s" % fp+'c'
    if 'embedded_pixmaps' in fp:
        print "(this one may take a while)"
    compiler.compileFile(fp)



def checkForQt():

    PK_ACTION("Checking for Qt ...")
    
    try:
        from qt import qVersion, PYQT_VERSION_STR
    except ImportError:
        PK_CERR("Could not find python Qt module")
        print 
        return False
    print "Found Qt version %s, PyQt version %s" % (qVersion(), PYQT_VERSION_STR)
    return True
    
    
def checkForPKAudio(versions, append_paths=[]):
    """ Returns True if the installed peices of pkaudio match the versions
    passed as a list of strings, i.e. ['0.3', '0.4']
    """
    global pkaudiod_version, proc

    PK_ACTION("Checking for pkaudio ...")
    
    # find the pkaudiod executable
    ver_cmd = 'pkaudiod -v'
    status, pkaudio_path = execCmd('which pkaudiod')
    if not os.path.isfile(pkaudio_path):
        if os.path.isfile('/usr/local/bin/pkaudiod'):
            ver_cmd = '/usr/local/bin/'+ver_cmd
        else:
            print "Could not find pkaudiod executable."
            return False
        
    # check the version
    status, output = execCmd(ver_cmd)
    try:
        pkaudiod_version = output.replace('pkaudiod-', '')
    except IndexError:
        PK_CERR("Got wierd output for 'pkaudiod -v': %s" % output)
        return False

    if pkaudiod_version in versions:
        print "Found pkaudiod version %s" % pkaudiod_version
    else:
        msg = "PKSampler requires pkaudiod-%s (found pkaudiod-%s)"
        PK_CERR(msg % (versions, pkaudiod_version))
        return False
        
    # find the python modules
    for name in PKAUDIO_MODULES:
        try:
            f, path, misc = imp.find_module(name)
        except ImportError:
            PK_CERR("cannot find \"%s\" python module" % name)
            return False
    # check the version
    import pkaudiocore
    if not pkaudiocore.VERSION in versions:
        PK_CERR("PKSampler requires pkaudio version %s, found %s" % (versions, pkaudiocore.VERSION))
        return False
    else:
        print "Found pkaudio python module version %s" % pkaudiocore.VERSION

    os_paths = os.environ['PATH'].split(':')+append_paths
    for dir in os_paths:
        fp = os.path.join(dir, 'pkaudiod')
        if os.path.isfile(fp):
            if os.access(fp, os.X_OK):
                break
            else:
                fp = None
        else:
            fp = None
    if fp:
        pass
        #getPKAudioVersion()
        #if not proc.normalExit():
        #    PK_CERR("Error executing %s " % fp)
        #    print
        #    return False
        #if pkaudiod_version.startswith('pkaudiod-'+VERSION):        #    print "Found %s @ %s" % (pkaudio_version, fp)
        #else:
        #    PK_CERR("Found %s @ %s, but pkaudio-%s is required" % (pkaudiod_version, fp, VERSION))
        #    print
        #    return False
    else:
        PK_CERR("Could not find pkaudiod executable")
        print
        return False
    
    return True



def doWrappers(bin_scripts, mod_dir, bin_dir):
    """ Generates wrapper shell-scripts for a list of python scripts, and
        installs them in bin_dir.
        'bin_scripts' is a list of tuples containing an executable python
        module name and description. 'target_dir' is the directory location
        of the python script that the shell script should execute.
    """
    PK_ACTION("Generating executable scripts ... ")

    # create/install the wrapper scripts
    for script, desc in bin_scripts:
        target = os.path.join(bin_dir, script)
        tmp = os.path.join('.', script+'.sh')
        fn = os.path.join(mod_dir, script)
        script = os.path.join('pksampler', script)
        print target
        wrapper = \
    """#!/bin/sh

    exec %s %s.pyc $*
    """ % (sys.executable, fn)
    
        copyToFile(tmp, wrapper)
        os.system("chmod 0755 %s" % tmp)
        cmd = "mv %s %s" % (tmp, target)
        runSudo(cmd, True)
