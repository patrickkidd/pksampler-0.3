""" """

import socket

BC_PORT = 20000
ACK_PORT = BC_PORT + 1

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
serverSocket.bind(('255.255.255.255', BC_PORT))
    
# wait for UDP broadcast, send TCP ACK
while 1:
    
    # open a socket and listen for a message
    value,address = serverSocket.recvfrom(256)
    print '[[[[[',value,address,']]]]]]]'
    host,port = address

    sendSocket = socket.socket(socket.AF_INET, 
                               socket.SOCK_STREAM, 0)
    sendSocket.connect((host, ACK_PORT))
    sendSocket.send('host up ack')
    sendSocket.close()
    sendSocket = None
