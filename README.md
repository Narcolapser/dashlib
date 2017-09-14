# Amazon Dash Button Hijacking server.

This is a simple tool for hijacking the amazon dash buttons. You put the dash buttons on a seperate wifi network and this server acts as the DHCP host for that network. An IP address is never returned to the buttons so they cannot ever communicate out with amazon, but the request for an IP address then triggers this server to do something.

This library was intended to facility the hijacking (and perhaps hijinks-ing) of the Amazon Dash Button to be a general purpose IoT button that you can get for cheap, or if you play your cards right, you can get for free.

# How to use

Two main steps. First you must create your tasks. Right now there are only two veriftes, but they cover the majority of things. There are "HTTP_Task" and "IFTT_Task" available.

```python

kitchenLights = HTTP_Task('F0:4F:7C:BD:8E:01','http://192.168.0.101/offon')

bedroomLights = IFTTT_Task('74:C2:46:B1:27:03',event='bedroom_ligts_event',key='your IFTTT webhook key')

```
the HTTP_Task takes the mac address of the dash button, and then the url it is supposed to call. Nothing is done with the call, this is mean to simply trigger an event. It is up to you to do something with that call.

Similarly, the IFTTT_Task takes the mac address of the dash button, and then the event you want to call with your IFTTT webhook key. When you press the button, the event will be triggered.

Slightly more complicated is the server. I'll come back to the setting up of that in a moment. But code wise it looks something like this:

```python

server = DashServer('wlan0','192.168.1.1')
server.append(kitchenLights)
server.append(bedroomLights)
server.run()
```

As you can see, we make the server, passing the interface the service will be hosted on, at the interface's IP address. After that you simply append the tasks to the server and call "run" on the server.

# How it works

This system hijacks the DHCP system to achieve it's goals. What happens is that when you press the button, the dash button turns on and attempts to connect to the wifi network. Once connected it attempts to get an IP address. However if you have this server running as the DHCP server it will never recieve an IP address, but it will trigger this server to take an action. The button will keep trying a total of 4 times, about a minute, and then unable to get an IP address will flash red and give up then turn off.

# Setting up the server

### Remember this is a seperate network, not your main network.

In order to make it so that the you don't order a 12 pack of red bull every time you use your dash button, we are going to put it on a seperate network so that it can't reach amazon. I did this with a raspberry pi and a wifi adapter. The wired connection of the raspberry pi provides it's ability to communicate out, but it's wifi connection is used to host a hidden wifi network. If you are doing something similar it, you will probably be using the interface 'wlan0' if you don't know what I'm talking about or you are doing something different, feel free to open an issue and I'll try help you through there. But assuming you are working the same as me, edit /etc/network/interfaces to contain something like this:

```
allow-hotplug wlan0
iface wlan0 inet static
        address 192.168.1.1
        netmask 255.255.255.0

```

You will also need to setup your device as a wireless access point, a good tutorial for that is [here](http://elinux.org/RPI-Wireless-Hotspot).

Then you should be set.

