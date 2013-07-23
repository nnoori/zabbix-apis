Zabbix for Mule ESB
===================

Python scripts that help adding Mule ESB applications automatically to Zabbix 2.0.4

The scripts work very simple, 
 
1. Mule Apps checker (apps_checker.py) checks for any deployed Mule applications in Mule/apps folder

2. mule_zabbix.py has different routines that will add hosts, applications and items. Get interfaces, HostIDs, GroupID etc

3. main.py is the main part of the program that you would invoke to run the apps_checker and call routines from mule_zabbix.py

4. mule_zabbix.properties file has the required parameters to log into zabbix and directories and host names information 

