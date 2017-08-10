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
# SCRIPTNAME=/home/toben/Code/dash-server/dash-server.py
SCRIPTNAME=/usr/local/bin/dash-server
PATH=/sbin:/usr/sbin:/bin:/usr/bin
DESC="Dash button service"
NAME=dash-server
DAEMON=/home/toben/Code/dash-server/$NAME
DAEMON_ARGS=""
PIDFILE=/var/run/$NAME.pid
#SCRIPTNAME=/etc/init.d/$NAME

. /lib/lsb/init-functions

case "$1" in
start)
        $SCRIPTNAME start
#	start-stop-daemon --start --quiet --background --make-pidfile --pidfile $PIDFILE --exec $DAEMON --test > /dev/null \
#		|| return 1
#	start-stop-daemon --start --quiet --background --make-pidfile --pidfile $PIDFILE --exec $DAEMON -- \
#		$DAEMON_ARGS \
#		|| return 2
        ;;
stop)
        $SCRIPTNAME stop
        ;;
restart)
        $SCRIPTNAME restart
        ;;
status)
#        $SCRIPTNAME status
	status_of_proc "$DAEMON" "$NAME" && exit 0 || exit $?
        ;;
*)
        echo "Usage: $0 <start|stop|restart|status>" >&2
        exit 3
        ;;
esac
exit 0
