#!/usr/local/bin/python


import os
import os.path
import sys
import getopt
import fpformat
import mask
import signal
import time

width = 266
height = 200

child_pid = None

#the value is the index of the last image

USAGE = """make.py --all --pretend"""

try:
    opts, args = getopt.getopt(sys.argv[1:], 'ap', ['all', 'pretend'])
except Exception, e:
    print 'PKSAMPLER: ',e
    print
    print USAGE
    sys.exit(1)

render_all = False
pretend = False
for o, a in opts:
    if o in ('--all', '-a'):
        render_all = True
    elif o in ('--pretend', '-p'):
        pretend = True

# default
if len(sys.argv) == 1:
    render_all = True
        
class KeyboardKill(KeyboardInterrupt):
    def __init__(self, pid, path):
        KeyboardInterrupt.__init__(self)
        self.pid = pid
        self.path = path

def make(name, sr, er, sc, ec, clock=0.0):
    global child_pid
    fname = os.path.join(name, name+str(clock) + '.png')
    args = (os.P_NOWAIT,
            'povray',
            'povray',
            os.path.join(name,name+'.pov'),
            'Clock='+str(clock),
            '+O'+fname,
            '-D0 +Q11 +R2 +AM2 +A0.3 +R2',
            '+W'+str(width),
            '+H'+str(height),
            #'+SR'+str(sr),
            #'+ER'+str(er),
            #'+SC'+str(sc),
            #'+EC'+str(ec),
            )
    child_pid = os.spawnlp(*args)
    try:
        (pid, status) = os.waitpid(child_pid, 0)
        if status != 0:
            print 'POVRAY RETURNED ERROR'
            return False
    except KeyboardInterrupt:
        raise KeyboardKill(child_pid, fname)
    return True

    
def make_iterative(name, indecies, sr=0, er=0, sc=0, ec=0):
    """ build <name>.pov with 'range' clock iterations """
    m, frames = mask.masks[name]
    if isinstance(frames, float):
        clock = 0.0
    else:
        clock = 0
    time_string = ''
    job_times = [] # keep track for averaging
    while len(indecies):
        clock = indecies[0]
        s = str(len(indecies)).rjust(3)
        s = s.replace(' ', '0')
        s = '>> FRAMES LEFT: '+s+time_string
        print s,
        sys.stdout.flush()
        
        job_time = time.time()
        if not make(name, sr, er, sc, ec, clock):
            sys.exit(1)
        indecies.remove(indecies[0])
        
        job_time = int(time.time() - job_time)
        job_times.append(job_time)
        avg_time = 0
        for jt in job_times:
            avg_time += jt
        avg_time = avg_time / len(job_times)
        min_rem = (avg_time*len(indecies)) / 60
        sec_rem = (avg_time*len(indecies)) % 60
        sec_rem = str(sec_rem).rjust(2)
        sec_rem = sec_rem.replace(' ', '0')
        time_string = ', %d:%s minutes remaining.' % (min_rem, sec_rem)
    
##~         # spool back
##~         for i in s:
##~             sys.stdout.write('\b')
##~         sys.stdout.flush()
    print 'Done'


usage = """Usage: make.py [--pretend] <dir> [dir ...] 
Example for slider.pov: make.py slider
"""


# FILE/ITERATIONS
def isolder(path1, path2):
    return os.path.getmtime(path1) < os.path.getmtime(path2)
    
def getOldImages(dir):
    """ Returns a list of indecies of images that need updating. """
    import mask
    pov_path = os.path.join(dir,dir+'.pov')
    inc_path = dir+'.inc'
    if os.path.exists(dir) and os.path.isdir(dir):
            
        m, frames = mask.masks[dir]
        use_int = False
        if isinstance(frames, int):
            use_int = True
        elif isinstance(frames, float):
            use_int = False
            
        checked_exts = []
        ext = 'png'
        good_ext = None
        index_digits = len(str(frames))
        # the validation algorithm:
        # use first of png or bmp, not both
        # an extension is good if one file is found.
        while True:
            ret = []
  
            if use_int:
                index = 0
            else:
                index = 0.0
                
            # check all the files
            while index <= frames:
                s_index = str(index).rjust(index_digits)
                s_index = s_index.replace(' ', '0')
                
                img_path = os.path.join(dir,dir+s_index+'.'+ext)
                # source exists?
                if os.path.exists(inc_path) and os.path.exists(pov_path):
                    # image exists?
                    if os.path.exists(img_path):
                        good_ext = ext
                        # stale images?
                        if isolder(img_path, pov_path) or isolder(img_path, inc_path):
                            ret.append(index)
                    else:
                        ret.append(index)
                if use_int:
                    index += 1
                else:
                    index += 0.1
                    
            # record the ext
            if not ext in checked_exts:
                checked_exts.append(ext)
                
            # see if we need to check another ext
            if not good_ext:
                if 'png' in checked_exts and not 'bmp' in checked_exts:
                    ext = 'bmp'
                elif 'bmp' in checked_exts and not 'png' in checked_exts:
                    ext = 'png'
                elif 'png' in checked_exts and 'bmp' in checked_exts:
                    break
            else:
                break
                
    return ret


def printPretend(dir, indecies):
    print 'IMAGE:',dir.ljust(20),'FRAMES:',
    if len(indecies):
        print indecies
    else:
        print 'None'
        
        
def isValidDir(dir):
    """ Returns True if the source tree exists for dir. """
    if os.path.isdir(dir):
        pov_path = os.path.join(dir, dir+'.pov')
        inc_path = dir+'.inc'
        if os.path.isfile(pov_path) and os.path.isfile(inc_path):
            return True
            
            
def makeDirs(check_dirs):
    """ Build the passed directories. """
    import mask
    render_jobs = {}
    # validate the dirs, queue the jobs
    for dir in check_dirs:
        m = mask.masks
        if dir == 'leddigit':
            pass
        if os.path.isdir(dir) and not dir in mask.masks:
            print '** \"%s\" has no mask entry in mask.py' % dir
        elif isValidDir(dir):
            old_images = getOldImages(dir)
            if old_images:
                render_jobs[dir] = old_images
            
    # process the jobs
    for dir, old_images in render_jobs.items():
        
        if not pretend:
            print 'Rendering \"'+dir+'\"',
            m, frames = mask.masks[dir]
            make_iterative(dir, old_images, frames)
        else:
            printPretend(dir, old_images)
        
    if len(render_jobs) == 0:
        print 'Nothing to do.'

    

def main():

    # take all dirs
    if render_all:
        makeDirs(os.listdir('.'))
    # take the passed names
    elif pretend:
        makeDirs(sys.argv[1:])
    else:
        makeDirs(sys.argv[1:])
    

if __name__ == '__main__':
    try:
        main()
    except KeyboardKill, e:
        os.kill(e.pid, signal.SIGKILL)
        os.system('rm '+e.path)
        sys.exit(1)

