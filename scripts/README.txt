Zabbix start|stop scripts
===================================================================
The instructions are taken from this post on Zabbix forums:
http://www.zabbix.com/forum/showthread.php?p=123241


1. Zabbix server 
2. Zabbix agent  
3. Zabbix java-gateway 

After copying the script files into /etc/init.d/ execute the following: 
#sudo chmod 755 /etc/init.d/<<script_file_name>>

For starting Zabbix when the machine boots execute the following command: 
#sudo update-rc.d <<script_file_name>> defaults

Ref: http://www.zabbix.com/wiki/howto/ins.../ubuntuinstall
