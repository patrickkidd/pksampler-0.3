from socket import *
import select
import sys

sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
sock.bind( ("<broadcast>", 2000) )

while 1:
    (rs,ws,es)=select.select([sock],[],[],1)
    if sock in rs:
        (data, addr) = sock.recvfrom(9999)
        print "Got data: {%s}" % data
        print "from:",addr
    else:
        print ".",
        sys.stdout.flush()
        
