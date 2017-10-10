import sys
import socket
import threading

import logging
from log import Logger

my_log = Logger('my_tcp_proxy', logging.DEBUG, 'my_tcp_proxy').boostrap()

# we dump 16 character one line
def hexdump(src, length=16):
	result = []
	# unicode is 2 bytes , ascii is 1 byte
	digits = 4 if isinstance(src, unicode) else 2
	print (digits)
	for i in xrange(0, len(src), length):
		s = src[i:i+length]
		# change it to bytes stream
		# change integer for per
		hexa = b' '.join(["%0*X" % ( digits, ord(x)) for x in s])
		# present ASCII-printable characters
		text = b''.join([x if 0x20 <=ord(x) < 0x7F else b'.' for x in s])
		result.append(b"%04X %-*s %s" % (i, length*(digits +1), hexa,text))

	print b'\n'.join(result)

def receive_from(connection):
	buffer = ""

	# We set a 2 second timeout; depending on
	# your target, this may need to be adjusted
	connection.settimeout(2)

	try:
		while True:
			data = connection.recv(4096)

			# we don't receive any data
			if not data:
				break

			buffer += data
	except:
		pass

	return buffer


def request_handler(buffer):

	# perform packet modifications
	return buffer

def response_handler(buffer):

	# perform packet modifications
	return buffer


def proxy_handler(client_socket, remote_host, remote_port, receive_first):
	my_log.info('Start a proxy handler')
	# connect to remote host
	state_remote = True
	try:
		remote_socket  = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		remote_socket.settimeout(2)
		remote_socket.connect((remote_host,remote_port))
		my_log.info('connected to remote services')
		# received data from remote end if necessary
		if receive_first :
			remote_buffer = receive_from(remote_socket)
			# dump the data into hex presentation
			hexdump(remote_buffer)

			# send it to our response handler
			remote_buffer = response_handler(remote_buffer)

			# if we have data to send to client ,send it
			if len(remote_buffer):
				my_log.info( "[<==] Sending %d bytes to localhost." % len(remote_buffer))
				client_socket.send(remote_buffer)
	except Exception as e :
		state_remote = False
		my_log.error('failed to connect remote server')

	# now let loops and read from local, send to remote ,send to local 
	# rinse , wash, repeat
	while True:
		remote_buffer = ""
		# read from local host
		local_buffer = receive_from(client_socket)

		if len(local_buffer):
			my_log.info("[==>] received %d from localhost" % len(local_buffer))
			hexdump(local_buffer)

			# send it to our request_hanlder 
			local_buffer = request_handler(local_buffer)

			if state_remote:
			# send off the data  to remote host
				remote_socket.send(local_buffer)
				my_log.info("[==>] Sent to remote")
		if state_remote:
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
		# COmmen this block until you have a remote server to work on it
		# if not data on either side, close the connection
		# if not len(remote_buffer) or not len(local_buffer):
		#	client_socket.close()
		#	remote_socket.close()
		#	print "[*] no more data.Closing connections."
		#	break


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
		print ("[==>] Received  incoming connection from %s:%s" %
			   (addr[0], addr[1]))

		# Start  a thread to talk  to remote host 
		proxy_thread = threading.Thread(target=proxy_handler,
										args=(client_socket, remote_host, remote_port, receive_first))

		proxy_thread.start()

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

