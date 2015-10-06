__author__ = 'root'

import sys
import socket
import getopt
import threading
import subprocess

# #define global variables
# listen = False
# command = False
# upload = False
# execute = ""
# target = ""
# #target = ""
# upload_destination =""
# port =0

def usage():
    print "From BHP net tool"
    print
    print " set up optparse"


    sys.exit(0)

def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        #connect to the target
        client.connect((target,port))
        if len(buffer):
            client.send(buffer)

        while True:
            #wait for data
            recv_len = 1
            response = ""

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break

            print response,

            #wait for more input
            buffer = raw_input("")
            buffer += "\n"

            #send it off
            cliend.send(buffer)

    except:
        print "{*} Exception! Exiting"

        client.close


def server_loop():
    global target

    # if no target is defnined, listen on all interfaces
    if not len(target):
        target = "0.0.0.0"
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((target,port))
        server.listen(5)

    while True:
        client_socket, addr = server.accept()

        #start thread
        client_thread = threading.Thread(target=client_handler, args =(client_socket,))
        client_thread.start()

def run_command(command):

    #trim new line
    command = command.strip()

    #run the command get get output

    try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=TRUE)
    except:
        output = "Failed to execute command"

    return output

def client_handler(client_socket):
    global upload
    global execute
    global command

    #check for upload
    if len(upload_destination):

        #read all bytes and write to destination
        file_buffer = ""

        #keep reading data until non is available?

        while TRUE:
            data = client_socket.recv(1024)

            if not data:
                break

            else:
                file_buffer += data

        #take bytes and try to write them
        try:
            file_descriptor = open(upload_destination,"wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            #acknowledge successful
            client_socket.send("Successfully saved file to %s\r\n:" % upload_destination)

        except:
            client_socket.sent("Failed to save file to %s\r\n" % upload_destination)


    if len(execute):
        #run command
        output = run_command(execute)

        client_socket.send(output)

    #another loop ifcommand shell was requested

    if command:
        while True:
            #show a simple prompt
            client_socket.send("<BHP:#> ")

            cmd_buffer=""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)

            #send command outpuit
            response = run_command(cmd_buffer)

            #send back the response
            client_socket.send(response)





if __name__ == "__main__":

    #define global variables
    listen = False
    command = False
    upload = False
    execute = ""
    target = ""
    #target = ""
    upload_destination =""
    port =0

    # global listen
    # global port
    # global execute
    # global command
    # global upload_destination
    # global target

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hle:t:p:cu", ["help","listen","execute","target","port","command", \
                                                                 "upload"])

    except getopt.GetoptError as err:
        print str(err)



    for o,a,in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-l","--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--ports"):
            port = int(a)
        else:
            assert False, "Unhandled Option"

        #are we going to listen or send data?

    if not listen and len(target) and port > 0:
            #read in the buffer form the comand line
            #this will block, so send CTRL-D if not sending input
            # to stdin
            buffer=sys.stdin.read()

            #send data
            client_sender(buffer)

        #listen and potentially upload, execute, drop a shell

    if not listen:
        server_loop()



