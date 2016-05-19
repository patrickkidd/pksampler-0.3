""" Config.py: Application configuration. """


import os, os.path
import atexit


_file = None
CONF_DPATH = os.path.join(os.environ["HOME"], '.pk')
CONF_FPATH = os.path.join(CONF_DPATH, 'pksampler_black.conf')
OPTIONS = {}

def _open(mode):
    if not os.path.isdir(CONF_DPATH):
	os.makedirs(CONF_DPATH)
    return open(CONF_FPATH, mode)
    
def write():
    _file = _open('w')
    for key, value in OPTIONS.items():
        _file.write(key+"="+value+'\n')
    _file.close()
    
def read():
    try:
        _file = _open('r')
    except IOError:
        _file = _open('w')
        _file = _open('r')
    for line in _file.readlines():
        line = line.replace('\n', '')
        if line:
            key, value = line.split('=')
            OPTIONS[key] = value
    
    
def get(key):
    if key in OPTIONS:
        return OPTIONS[key]
    else:
        return ''
    
def set(key, value):
    global OPTIONS
    OPTIONS[key] = value
    
def _atexit():
    write()
atexit.register(_atexit)
read()


if __name__ == '__main__':
    print "OPTIONS:"
    for key, value in OPTIONS.items():
        print key+'='+value
