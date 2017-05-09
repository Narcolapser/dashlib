#!/bin/sh
# Linux Standard Base comments
### BEGIN INIT INFO
# Provides:          Dash Server
# Required-Start:    $local_fs $network $remote_fs
# Required-Stop:     $local_fs $network $remote_fs
# Should-Start:
# Should-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Dash Button Server
# Description:       A DHCP server that hijacks the Amazon Dash Buttons.
### END INIT INFO

#############################################################
# Init script for Dash Server
#############################################################

# Defaults
# SCRIPTNAME=/usr/local/DashServer/DashServer.py
SCRIPTNAME=/home/toben/Code/dash-server/dash-server.py

case "$1" in
start)
        $SCRIPTNAME start
        ;;
stop)
        $SCRIPTNAME stop
        ;;
restart)
        $SCRIPTNAME restart
        ;;
force-reload)
        $SCRIPTNAME force-reload
        ;;
status)
        $SCRIPTNAME status
        ;;
*)
        echo "Usage: $0 <start|stop|restart|force-reload|status>" >&2
        exit 3
        ;;
esac
exit 0
