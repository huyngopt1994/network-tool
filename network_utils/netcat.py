import sys
import socket
import getopt
import gevent
import threading
import subprocess
import logging
from log import Logger
# define some global variables
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

my_log = Logger('my_netcat', logging.DEBUG, 'my_netcat').boostrap()

def client_sender(buffer):
    # create socket
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect((target,port))
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
    except Exception as e :
        print("Exception, exiting :%s " %e)

        # Tear Down
        client.close()

def server_loop():
    global target

    my_log.info('create a server loop')

    # if no target is defined , we listen on all interfaces
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target,port))
    server.listen(5)
    my_log.info('create a server loop at ip %s ,at port %s' %(target,port))
    while True:
        client_socket , addr = server.accept()
        print('get a client_socket')
        # spin off a gevent greenlet  to hanlde our new client
        thread = threading.Thread(target=client_handler, args=(client_socket,))
        thread.start()
     #   gevent.spawn(client_handler, client_socket)


def run_command(command):

    # trim the newline
    command = command.rstrip()

    # run the command and get the ouput back
    try :
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Failed to execute command.\r\n"

    # send the output back to the client
    return output

# implement the logic to do file uploads, command execution, and our shell

def client_handler(client_socket):
  
    global upload
    global execute
    global command

    my_log.info('get a client handler')
    # check for upload:
    if len(upload_destination):

        # read in all of bytes and write to our destination
        file_buffer = ""

        # keep reading data until none is avaiable
        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data

        # now we take these bytes and try to write them out
        try:
            file_description = open(upload_destination,"wb")
            file_description.write(file_buffer)
            file_description.close()

            # acknowledge that we wrote the file out
            client_socket.send('Successfully save file to %s \r\n' % upload_destination)
        except:
            client_socket.send('Failed to save file to %s\r\n' % upload_destination)
       # gevent.idle()

    # check for command execution

    if len(execute):

        # run the command
        output = run_command(execute)

        client_socket.send(output)

    # now we go into another loop if a comand shell was requested

    if command:
        my_log.info("in command mode")

        while True:
            # Show a simple prompt
            client_socket.send("<BHP:#>")


            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)

            my_log.info("get cmd buffer from client %s", cmd_buffer)
            # send back the command output
            response = run_command(cmd_buffer)
          #  gevent.idle()
            # send back the response
            client_socket.send(response)
         #   gevent.idle()

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
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
                                   ["help","listen","execute","target","port","command","upload"])
    except getopt.GetoptError as e :
        print(str(e))
        usage()

    for o, a in opts:
        if o in ("-h","--help"):
            usage()
        if o in ("-l","--listen"):
            listen = True
        if o in ("-e","--execute"):
            execute = a
        if o in ("-t","--target"):
            target = a
        if o in ("-p","--port"):
            port = int(a)
        if o in ("-c","--command"):
            command = True
        if o in ("-u","--upload"):
            upload_destination = True
        else:
            print("Unhandled Option")


    # are you going to listen or just send data from stdin ?
    if not listen and len(target) and port > 0:
        # read in buffer from the command line
        # this will block,  so send CTRL-D if not sending input to stdin
        buffer = raw_input('press some thing to get data :')
        # send data off
        client_sender(buffer)

    # We are going to listen, potentially upload things ,execute commands
    # and drop a shell back depend on our command line options above

    if listen:
        server_loop()

if __name__ == '__main__':
    main()
