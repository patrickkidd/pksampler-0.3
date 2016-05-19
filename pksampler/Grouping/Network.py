#!/bin/env python
""" Classes for reliable communication between application hosts. 
    The Remote host class stores information about remote hosts locally,
    and is kept updated by the remote hosts via network events.

    TODO:
    - Change 'Dispatch' to something else.
    - move PKAudioServer to pkaudio.py, pkaudiocore.py
"""

from qt import *
import socket
import Globals
import atexit

pkaudio = Globals.getPKAudio()

ENABLE_HOSTCACHE = True


def _atexit():
    if HostCacheServer in Singleton.instances:
        hcs = Singleton.instances[HostCacheServer]
    Singleton.instances[HostCacheServer] = None
atexit.register(_atexit)


class SingletonException(Exception):
    pass
class Singleton:
    instances = {}
    
    def __init__(self):
        if self.__class__ in Singleton.instances:
            raise SingletonException('an instance of this class already exists')
        else:
            Singleton.instances[self.__class__] = self
            

class ServerThread(QThread, Singleton):
    """ Base class for threaded servers that block and emit qt events. """
    
    def __init__(self, parent=None):
        QThread.__init__(self)
        Singleton.__init__(self)
        self.parent = parent
        
    def _postEvent(self, data):
        if self.parent:
            e = QCustomEvent(QEvent.User)
            e.setData(data)
            QApplication.postEvent(self.parent, e)
        
        
class PKAudioServer(ServerThread):
    """ Receives events from pkaudiod. Events are passed as QCustomEvents.
        This should be moved somewhere else...
    """
                
    def __init__(self, parent=None):
        """ Events are posted to parent using postEvent. """
        Globals.PrintErr("class PKAudioServer must be moved to the pkaudio package")
        ServerThread.__init__(self, parent)
        self.up = True
        if not pkaudio.connected():
           pkaudio.start_server()
        self.driver = pkaudio.Driver()
        self.driver.addHost(socket.gethostname())
        
    def run(self):
        sock = socket.socket(socket.AF_INET, 
                             socket.SOCK_DGRAM, 0)
        
        try:
            sock.bind((socket.gethostname(), pkaudio.PK_UP_PORT))
        except socket.error, e:
            Globals.PrintErr("Couldn't open pkaudio port: "+str(e))
            return
        
        sock.setblocking(True)
        while self.up:
            value, address = sock.recvfrom(1024)
            self._postEvent(value)
        Globals.Print('PKAudioServer: thread exitting.')
        
        
class HostCacheServer(ServerThread):
    """ Keeps track of similar objects on other hosts. """
    
    def __init__(self, parent=None):
        ServerThread.__init__(self, parent)
        self.error = False # if broadcast didn't work
        self.stopped = False
        # broadcast socket
        self.broadcastSocket = socket.socket(socket.AF_INET, 
                                             socket.SOCK_DGRAM, 0)
        self.broadcastSocket.setsockopt(socket.SOL_SOCKET, 
                                        socket.SO_BROADCAST, 1)
        self._acquireHosts()
        #self.start()
        
    def __del__(self):
        self.stop()
        self.broadcastSocket.close()
        
    def _addHost(self, host):
        self._postEvent('host up '+host)
        
    def _removeHost(self, host):
        self._postEvent('host down '+host)
      
    def _acquireHosts(self):
        """ broadcast, Request all hosts to send back a special ack. """
        # the tcp socket that receives the ACK
        ackSocket = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM, 0)
        ackSocket.bind(('', Globals.ACK_PORT))
        ackSocket.settimeout(1)
        ackSocket.listen(5)
        
        # UDP BROADCAST
        Globals.Print('Broadcasting for other hosts...')
        self.broadcast('host up')
        
        # WAIT: RESPONSES, TIMEOUT
        self.hosts = []
        while 1:
            try:
                # TCP ACK
                clientsocket, (host, port) = ackSocket.accept()
                value = clientsocket.recv(256)
                if value == 'host up ack':
                    self.addHost(host)
                clientsocket.close()
                clientsocket = None
            except:
                break
                
        ackSocket.close()
        
    def broadcast(self, data):
        """ Do a network broadcast """
        if not self.error:
            try:
                self.broadcastSocket.sendto(data,('<broadcast>',
                                            Globals.BROADCAST_PORT))
            except socket.error, (errno, text):
                if errno == 101:
                    self.error = True
                    Globals.PrintErr("You don't have any network interfaces!")
                else:
                    raise
        
    def stop(self):
        """ tell all the hosts that this one is dieing. """
        self.stopped = True
        self.broadcast('host down')
        
    def run(self):
        """ Listen for broadcasts from new or dieing hosts. """
        self.stopped = False
        # receives incoming 'host up' requests
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        serverSocket.bind(('255.255.255.255', Globals.BROADCAST_PORT))
        
        # wait for UDP broadcast, send TCP ACK
        while 1:
            
            # open a socket and listen for a message
            value,address = serverSocket.recvfrom(256)
            host,port = address
            
            # this actually prevents a seg fault ;( for some reason
            if self.stopped:
                return
    
            if value == 'host up':
            
                sendSocket = socket.socket(socket.AF_INET, 
                                           socket.SOCK_STREAM, 0)
                sendSocket.connect((host, Globals.ACK_PORT))
                sendSocket.send('host up ack')
                sendSocket.close()
                sendSocket = None
                self._addHost(host)
                
            elif value.find('host down') == 0:
                self._removeHost(host)
                    
            elif value.find('add group') == 0:
                self._postEvent(value)
                
            elif value.find('remove group') == 0:
                self._postEvent(value)
                
            elif value.find('group beat') == 0:
                self._postEvent(value)
        
        serverSocket.close()

        
class Dispatch(QObject):
    """ Performs all network communication and emits known events as signals.
        Really just acts as a QObject container proxy for the server threads.
        SINGALS:
            PYSIGNAL('host_up'), (host_ip,)
            PYSIGNAL('host_down), (host_down,)
            PYSIGNAL('add_group'), (group_id,)
            PYSIGNAL('remove_group'), (group_id,)
            PYSIGNAL('group_beat'), (group_id,)
            PYSIGNAL('local_sample_starting'), (sample_id,)
            PYSIGNAL('midi'), ([int,int,int,float],)
    """

    def __init__(self):
        QObject.__init__(self)
        self.hosts = []
        
        self.hostCacheServer = HostCacheServer(self)
        if ENABLE_HOSTCACHE:
            Globals.Print('Starting host listener...')
            self.hostCacheServer.start()
        self.pkaudioServer = PKAudioServer(self)
        self.pkaudioServer.start()

    def __del__(self):
        self.close()
    
    def close(self):
        self.hostCacheServer.stop()
    
    def customEvent(self, e):
        """ Receive events from the threads. """
        data = e.data()
        
        ## HOST INFO
        
        if data.find('host up') == 0:
            self.emit(PYSIGNAL('host_up'), (data.split(' ')[2],))

        elif data.find('host down') == 0:
            self.emit(PYSIGNAL('host_down'), (data.split(' ')[2],))

        elif data.find('add group') == 0:
            self.emit(PYSIGNAL('add_group'), (int(data.split(' ')[2]),))

        elif data.find('remove group') == 0:
            self.emit(PYSIGNAL('remove_group'), (int(data.split(' ')[2]),))

        elif data.find('group beat') == 0:
            self.emit(PYSIGNAL('group_beat'), (data[11:],))
        
       ## PKAUDIOD
       
        elif data.find('midi') == 0:
            l = data.split(' ')[1:]
            data = [int(l[0]),int(l[1]),int(l[2]),float(l[3])]
            self.emit(PYSIGNAL('midi'), (data,))
            
        elif data.find('sample:starting') == 0:
            l = data.split(' ')
            self.emit(PYSIGNAL('local_sample_starting'), (int(l[1]),))
            
    def notifyAddGroup(self, group_id):
        self.hostCacheServer.broadcast('new group '+str(group_id))
        
    def notifyRemoveGroup(self, group_id):
        self.hostCacheServer.broadcast('remove group '+str(group_id))
        
    def notifyGroupBeat(self, group_id):
        self.hostCacheServer.broadcast('group beat '+str(group_id))
    

def test_HostCacheServer():
    import time
    hcs = HostCacheServer()

def test_PKAudioServer():
    import pkaudio
    pkaudio.start_server()
    s = PKAudioServer()
    s.start()
    s.wait()

def test_Dispatch():
    a = QApplication([])
    b = QPushButton('quit', None)
    b.show()
    d = Dispatch()
    QObject.connect(b, SIGNAL('clicked()'), a.quit)
    a.setMainWidget(b)
    a.exec_loop()
    
if __name__ == '__main__':
    import time
    #import pkaudio
    #pkaudio.start_server()
    #test_sample()
    a = QApplication([])
    w = W()
    comm = Dispatch()
    w.show()
    a.setMainWidget(w)
    a.exec_loop()
    
