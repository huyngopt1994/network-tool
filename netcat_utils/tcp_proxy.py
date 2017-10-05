import sys
import socket
import threading

import logging
from log import Logger

my_log = Logger('my_tcp_proxy', logging.DEBUG, 'my_tcp_proxy').boostrap()

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