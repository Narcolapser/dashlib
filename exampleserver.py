from dashlib import *
import os

kitchenLights = HTTP_Task('F0:4F:7C:BD:8E:01','http://192.168.0.101/offon')
garageDoor = HTTP_Task('F0:27:2D:3B:1D:02','http://192.168.0.102/open')
bedroomLights = IFTTT_Task('74:C2:46:B1:27:03',event='bedroom_ligts_event',key='your IFTTT webhook key')

#The first argument is the interface you want to use.
#The second argument is it's IP address. You will have to set this to a static
# IP address.
server = DashServer('wlan0','192.168.1.1')
server.append(kitchenLights)
server.append(garageDoor)
server.append(bedroomLights)

pid = os.fork()
if pid == 0:
	server.run()
else:
	print("New process started with a PID of: ", pid)
	with open("/var/run/dash-server.pid",'w') as f:
		f.write(str(pid))



