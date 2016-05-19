""" """

import socket

BC_PORT = 20000
ACK_PORT = BC_PORT + 1

# broadcast socket
broadcastSocket = socket.socket(socket.AF_INET, 
                           socket.SOCK_DGRAM, 0)
broadcastSocket.setsockopt(socket.SOL_SOCKET, 
                      socket.SO_BROADCAST, 1)

# the tcp socket that receives the ACK
ackSocket = socket.socket(socket.AF_INET,
                          socket.SOCK_STREAM, 0)
ackSocket.bind(('', ACK_PORT))
ackSocket.settimeout(1)
ackSocket.listen(5)

# UDP BROADCAST
broadcastSocket.sendto('host up',('<broadcast>', BC_PORT))

while 1:
    try:
        # TCP ACK
        clientsocket, (host, port) = ackSocket.accept()
        value = clientsocket.recv(256)
        print value, host, port 
        if value == 'host up ack':
            pass
        clientsocket.close()
        clientsocket = None
    except:
        break
