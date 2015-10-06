__author__ = 'root'

import socket
import threading
bind_ip = "0.0.0.0"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))

server.listen(5)

print "Listening on %s:%d" %(bind_ip,bind_port)

#this is our clinet-handling thread

def handle_client(client_socket):
    #print out what hte client sends
    request = client_socket.recv(1024)

    print "[*] REceived: %s" % request

#does not include a loop to consistently receive data
    #send back packet
    client_socket.send("ACK!")

    client_socket.close()

while True:
    client, addr = server.accept()

    print "[*] Accepted connection from %s:%d" % (addr[0],addr[1])

    #run client thread
    client_handler = threading.Thread(target=handle_client,args=(client,))
    client_handler.start()