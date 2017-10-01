import sys
import socket
import getopt
import threading
import subprocess

# define some global variables
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

def client_sender(buffer):
    # create socket
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect(target,port)
        if len(buffer):
            client.send(buffer)

        while True:

            # now wait for data back
            recv_len = 1
            response = ""

            while recv_len:

                data = client.recv(4096)
                recv_len = len(data)
                response += data
                if recv_len < 4096 :
                    break

            print response
            # print wait for more input
            buffer = raw_input('press more : ')
            buffer += "\n"

            # send it off
            client.send(buffer)
    except :
        print("Exception, exiting")

        # Tear Down
        client.close()

def usage():
    print "Netcat tool"
    print
    print "Usage: python netcat.py -t target_host -p port"
    print "-l --listen  -listen on [host]:[port] for incoming connections"
    print "-e --excecute=file_to_run -execute the given file upon receiving a connection"

    print "-c --comand -Initialize a command shell"
    print "-u --upload=destination -upon receiving connetion upload a file and write to destination"

    print
    print
    sys.exit(0)

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    # read the command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu",
                                   ["help","listen","execute","target","port","command","upload"])
    except getopt.GetoptError as e :
        print(str(e))
        usage()


    for o,a in opts:
        if o in ("-h","--help"):
            usage()
        if o in ("-l","--listen"):
            listen = True
        if o in ("-e","--execute"):
            execute = a
        if o in ("-t","--target"):
            target = True
        if o in ("-p","--port"):
            port = True
        if o in ("-c","--command"):
            command = True
        if o in ("-u","--upload"):
            upload_destination = True
        else:
            print("Unhandled Option")


    # are you going to listen or just send data from stdin ?
    if not listen and len(target) and port >0:
        # read in buffer from the command line
        # this will block,  so send CTRL-D if not sending input to stdin
        buffer = sys.stdin.read()

        # send data off
        client_sender(buffer)

    # We are going to listen, potentially upload things ,execute commands
    # and drop a shell back depend on our command line options above

    if listen:
        server_loop()

if __name__ == '__main__':
    main()
