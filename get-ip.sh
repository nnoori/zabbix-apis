    #!/bin/bash
    # Shell script scripts to read ip address
    # -------------------------------------------------------------------------
    # Copyright (c) 2005 nixCraft project <http://cyberciti.biz/fb/>
    # This script is licensed under GNU GPL version 2.0 or above
    # -------------------------------------------------------------------------
    # This script is part of nixCraft shell script collection (NSSC)
    # Visit http://bash.cyberciti.biz/ for more information.
    # -------------------------------------------------------------------------
    # Get OS name
    OS=`uname`
    echo $OS
    IP="" # store IP
    case $OS in
    Linux) IP=`ifconfig | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}'`;;
    Darwin) IP=`ifconfig | grep 'inet'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $2}'`;;
    *) IP="Unknown";;
    esac
    echo "$IP" 