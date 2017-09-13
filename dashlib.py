#!/usr/bin/env python

#originally from https://github.com/psychomario/PyPXE

import socket,binascii,time,os,sys,IN,signal
import requests
from sys import exit

ebStart = 0

if not hasattr(IN,"SO_BINDTODEVICE"):
	IN.SO_BINDTODEVICE = 25  #http://stackoverflow.com/a/8437870/541038

def slicendice(msg,slices):  #generator for each of the dhcp fields
	for x in slices:
		if str(type(x)) == "<type 'str'>": x=eval(x) #really dirty, deals with variable length options
		yield msg[:x]
		msg = msg[x:]



class DashServer( Object ):
	def __init__(interface,address):
		self.interface = interface
		self.address = address
		self.loop = False

	def run(self):
#		interface = 'wlan0'
		interface = self.interface
#		address = '192.168.1.1'
		address = self.address
		elements_in_address = address.split('.')
	        port = 67
	        offerfrom = '.'.join(elements_in_address[0:3])
        	offerfrom = offerfrom + '.100'
	        offerto = '.'.join(elements_in_address[0:3])
	        offerto = offerto + '.150'
	        broadcast = '.'.join(elements_in_address[0:3])
	        broadcast = broadcast + '.254'
	        netmask = '255.255.255.0'
	        tftp = address
	        dns = '8.8.8.8'
	        gateway = address
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

		self.loop = True
		while self.loop: #main loop
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

			except KeyboardInterrupt:
				exit()

	def executeTask(self,mac):
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
					print "fairy lights pushed."
					ebStart = time.time()
					requests.post("https://maker.ifttt.com/trigger/fair_dash_button/with/key/oKuztFyPxzSFMGyuI4S9mzyNT3_C3WeFYe1Nlo-p0_h")

			if mac == 'B4:CE:F6:09:A2:D7':
				print "Hello there Iron!"
		except requests.exceptions.Timeout:
			print "timeout."
		except:
			print "had a woopsie!"
		

class Task( Object ):
	def __init__(self):
		self.timer = 0
		self.delay = 60

	def __call__(self):
		if self.timer < (time.time() - self.delay):
			self.run()
			self.timer = time.time()

	def run(self):
		print("Default task run")

class IFTTT_Task( Task ):
	def __init__(self,event=none,key=none,url=url):
		super(IFTTT_Task,self).__init__()
		self.event = event
		self.key = key
		self.url = url

	def run(self):
		if self.event:
			requests.post("https://maker.ifttt.com/trigger/"+self.event+"/with/key/"+self.key)
		else:
			requests.post(self.url)

class HTTP_Task( Task ):
	def __init__(self,request):
		self.request = request

	def run(self):
		requests.get(self.request)

def start():
	pid = os.fork()
	if pid == 0:
		server()
#		print("I am the new process!", pid)
#		while 1:
#			print("Running!")
#			time.sleep(1)
	else:
		print("New process started with a PID of: ", pid)
		with open("/var/run/dash-server.pid",'w') as f:
			f.write(str(pid))

def stop():
	with open("/var/run/dash-server.pid") as f:
		pid = int(f.read())
	try:
		os.kill(pid,signal.SIGKILL)
	except OSError as ose:
		print("No process to stop")
	with open("/var/run/dash-server.pid",'w') as f:
		f.write('')

def status():
	with open("/var/run/dash-server.pid") as f:
		pid = int(f.read())
	print("Dash service found at: " +str( pid))


if __name__ == "__main__":
	if sys.argv[1] == 'start':
		start()
	elif sys.argv[1] == 'stop':
		stop()
	elif sys.argv[1] == 'restart':
		stop()
		start()
	elif sys.argv[1] == 'status':
		status()
	else:
		print("Coming soon")

