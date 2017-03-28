#!/usr/bin/env python

#originally from https://github.com/psychomario/PyPXE

import socket,binascii,time,os,sys,IN
import requests
from sys import exit
from optparse import OptionParser

ebStart = 0

if not hasattr(IN,"SO_BINDTODEVICE"):
	IN.SO_BINDTODEVICE = 25  #http://stackoverflow.com/a/8437870/541038

def slicendice(msg,slices):  #generator for each of the dhcp fields
	for x in slices:
		if str(type(x)) == "<type 'str'>": x=eval(x) #really dirty, deals with variable length options
		yield msg[:x]
		msg = msg[x:]

def doTheThing(mac):
	print mac
	global ebStart
	try:
		if mac == 'F0:4F:7C:BD:8E:EB':
			if time.time() > ebStart + 60:
				print "Kitchen light button was pushed."
				ebStart = time.time()
				requests.get("http://192.168.0.101/toggle",timeout=1)
		if mac == 'F0:27:2D:3B:1D:4B':
			if time.time() > ebStart + 60:
				print "Garage door button was pushed!"
				ebStart = time.time()
				requests.get("http://192.168.0.102/toggle",timeout=1)
		if mac == '74:C2:46:B1:27:2A':
			if time.time() > ebStart + 60:
				print "Un-assigned was pushed."
				ebStart = time.time()
#				requests.get("http://192.168.0.13/toggle",timeout=0.001)

		if mac == 'B4:CE:F6:09:A2:D7':
			print "Hello there Iron!"
	except requests.exceptions.Timeout:
		print "timeout."
	except:
		print "had a woopsie!"

if __name__ == "__main__":
	parser = OptionParser(description='%prog - a simple DHCP server', usage='%prog [options]')
	parser.add_option("-a", "--address", dest="address", action="store", help='server ip address (required).')
	parser.add_option("-i", "--interface", dest="interface", action="store", help='network interface to use (default all interfaces).')
	parser.add_option("-p", "--port", dest="port", action="store", help='server port to bind (default 67).')
	parser.add_option("-f", "--from", dest="offerfrom", action="store", help='ip pool from (default x.x.x.100).')
	parser.add_option("-t", "--to", dest="offerto", action="store", help='ip pool to (default x.x.x.150).')
	parser.add_option("-b", "--broadcast", dest="broadcast", action="store", help='broadcast ip to reply (x.x.x.254).')
	parser.add_option("-n", "--netmask", dest="netmask", action="store", help='netmask (default 255.255.255.0).')
	parser.add_option("-s", "--tftp", dest="tftp", action="store", help='tftp ip address (default ip address provided).')
	parser.add_option("-d", "--dns", dest="dns", action="store", help='dns ip address (default 8.8.8.8).')
	parser.add_option("-g", "--gateway", dest="gateway", action="store", help='gateway ip address (default ip address provided).')
	parser.add_option("-x", "--pxefilename", dest="pxefilename", action="store", help='pxe filename (default pxelinux.0).')
	parser.add_option("-q", "--quiet", dest="quiet", action="store_true", default=False, help='quiet mode (default off).')

	(options, args) = parser.parse_args()

	if not (args or options.address):
		parser.print_help()
		exit(1)

	if options.interface:
		interface = options.interface
	else:
		interface = '' # Symbolic name meaning all available interfaces

	if options.port:
		port = options.port
	else:
		port = '67'
		port = int(port)

	if options.address:
		address = options.address
		elements_in_address = address.split('.')
		if len(elements_in_address) != 4:
			sys.exit(os.path.basename(__file__) + ": invalid ip address")
	else:
		exit(1)

	if options.offerfrom:
		offerfrom = options.offerfrom
	else:
		offerfrom = '.'.join(elements_in_address[0:3])
		offerfrom = offerfrom + '.100'

	if options.offerto:
		offerto = options.offerto
	else:
		offerto = '.'.join(elements_in_address[0:3])
		offerto = offerto + '.150'

	if options.broadcast:
		broadcast = options.broadcast
	else:
		broadcast = '.'.join(elements_in_address[0:3])
		broadcast = broadcast + '.254'

	if options.netmask:
		netmask = options.netmask
	else:
		netmask = '255.255.255.0'

	if options.tftp:
		tftp = options.tftp
	else:
		tftp = address

	if options.dns:
		dns = options.dns
	else:
		dns = '8.8.8.8'

	if options.gateway:
		gateway = options.gateway
	else:
		gateway = address

	if options.pxefilename:
		pxefilename = options.pxefilename
	else:
		pxefilename = 'pxelinux.0'

	leasetime=86400 #int

	leases=[]
	#next line creates the (blank) leases table. This probably isn't necessary.

	if port < 1024:
		if not os.geteuid() == 0:
			sys.exit(os.path.basename(__file__) + ": root permitions are necessary to bind to port " + str(port) + ", use -p to specify a non privileged port or run as root.")

	for ip in ['.'.join(elements_in_address[0:3])+'.'+str(x) for x in range(int(offerfrom[offerfrom.rfind('.')+1:]),int(offerto[offerto.rfind('.')+1:])+1)]:
		leases.append([ip,False,'000000000000',0])

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET,IN.SO_BINDTODEVICE,interface+'\0') #experimental
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	s.bind(('',port))
	#s.sendto(data,(ip,port))

	if not options.quiet:
		print  "Starting %s..." % (os.path.basename(sys.argv[0]))
		if not address or address == '0.0.0.0':
		  print "  address: all interfaces"
		else:
		  print "  address:	  " + address
		print   "  tftp:		 " + str(tftp)
		print   "  gateway:	  " + str(gateway)
		print   "  dns:		  " + str(dns)
		print   "  netmask:	  " + str(netmask)
		print   "  port:		 " + str(port)
		print   "  pxe filename: " + str(pxefilename)
		print   "  pid:		  " + str(os.getpid())
		print   "  serving:	  " + str(offerfrom) + " - " + str(offerto)
		print   "Press <Ctrl-C> to exit.\n"

	while 1: #main loop
		try:
			message, addressf = s.recvfrom(8192)
			if not message.startswith('\x01') and not addressf[0] == '0.0.0.0':
				continue #only serve if a dhcp request

			dhcpfields=[1,1,1,1,4,2,2,4,4,4,4,6,10,192,4,"msg.rfind('\xff')",1,None]
			hexmessage=binascii.hexlify(message)
			messagesplit=[binascii.hexlify(x) for x in slicendice(message,dhcpfields)]
			mac_temp = messagesplit[11].upper()
			mac = ""
			for i in range(5):
				mac += mac_temp[i*2:i*2+2]
				mac += ":"
			mac += mac_temp[10:]
			doTheThing(mac)

#			data=reqparse(message) #handle request
#			if data:
#				s.sendto(data,('<broadcast>',68)) #reply
#			release() #update releases table
		except KeyboardInterrupt:
			exit()
	#	except:
	#		continue
