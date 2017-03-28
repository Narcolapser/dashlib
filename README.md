= Amazon Dash Button Hijacking server.

This is a simple tool for hijacking the amazon dash buttons. You put the dash buttons on a seperate wifi network and this server acts as the DHCP host for that network. An IP address is never returned to the buttons so they cannot ever communicate out with amazon, but the request for an IP address then triggers this server to do something.
