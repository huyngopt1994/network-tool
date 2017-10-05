import sys
import socket
import threading

import logging
from log import Logger

my_log = Logger('my_tcp_proxy', logging.DEBUG, 'my_tcp_proxy').boostrap()

def proxy_handler(client_socket, remote_host, remote_port, receive_first):

	# connect to remote host
	remote_socket  = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	remote_socket.connect((remote_host,remote_port))

	# received data from remote end if necessary 
	if receive_first :
		remote_buffer = receive_from(remote_socket)
		hexdump(remote_buffer)

		# send it to our response handler 
		remote_buffer = response_handler(remote_buffer)

		# if we have data to send to client ,send it
		if len(remote_buffer):
			my_log.info( "[<==] Sending %d bytes to localhost." % len(remote_buffer))
			client_socket.send(remote_buffer)

	# now let loops and read from local, send to remote ,send to local 
	# rinse , wash, repeat
	while True:
		# read from local host
		local_buffer = receive_from(client_socket)

		if len(local_buffer):
			my_log.info("[==>] received %d from localhost" % len(local_buffer))
			hexdump(local_buffer)

			# send it to our request_hanlder 
			local_buffer = request_handler(local_buffer)

			# send off the data  to remote host 
			remote_socket.send(local_buffer)
			my_log.info("[==>] Sent to remote")

		# receive back from the response 
		remote_buffer = receive_from(remote_socket)

		if len(remote_buffer):
			my_log.info("[<===] received %d from remote_buffer" % len(remote_buffer))
			hexdump(remote_buffer)

			# send it to our response handler 
			remote_buffer = response_handler(remote_buffer)

			# send off the data  to local host 
			client_socket.send(remote_buffer)
			my_log.info("[<==] Sent to local host")
		# if not data on either side, close the connection
		if not len(remote_buffer) or not len(local_buffer):


def server_loop(local_host, local_port,remote_host, remote_port, receive_first):

	# Create server socket
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		server.bind((local_host, local_port))
	except:
		my_log.error('Failed to listen on %s %d' %(local_host, local_port))
		sys.exit(0)

	server.listen(5)

	while True:
		client_socket, addr = server.accept()

		# print out the local connection information 
		print ("[==>] Received  incoming connection from %s:%" %
			   (addr[0], addr[1]))

		# Start  a thread to talk  to remote host 
		proxy_thread = threading.Thread(target=proxy_handler,
										args=(client_socket, remote_host, remote_port, receive_first))

		proxy_thead.start()

def main():
	if len(sys.argv[1:]) != 5:
		print "Usage: python tcp_proxy.py [localhost] [localport] [remotehost] [remoteport] [receivefirst]"
		print "Example : python tcp_proxy.py 127.0.0.1 9000 8.8.8.8 9000 True"
		sys.exit(0)

	# setup local listening parameters
	local_host = sys.argv[1]
	local_port = int(sys.argv[2])

	# setup remote target
	remote_host = sys.argv[3]
	remote_port = int(sys.argv[4])

	receive_first = sys.argv[5]

	if "True" in receive_first:
		receive_first = True
	else:
		receive_first = False 

	# now spin up  our listen socket 
	server_loop(local_host, local_port, remote_host, remote_port, receive_first)


if __name__ == '__main__':
	main()

