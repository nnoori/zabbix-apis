#! /usr/bin/env python
#####################################################
#  Test script for detecting JSB and add Zabbix     #
#  Host, Log items, screens                         #
#####################################################

import zabbix_api
import socket
import os
import sys
import json
import socket
from zabbix_api import ZabbixAPI, ZabbixAPIException


#####################################################
#  Function reads the jmp.properties file and       #
#  returns username,password, agent.conf path       #
# input:  path to jmp.properties file               #
# output:  list [username, password, path ]         #
#####################################################
def z_log_info(name):
        datafile = file(name)
        z_data = []
        for line in datafile:
            if "username" in line:
            	line = line.strip('\n')
            	line = line.lstrip("username")
            	z_data.append(line.strip(' '))
            elif "password" in line:
            	line = line.strip('\n')
            	line = line.lstrip("password")
            	z_data.append(line.strip(' '))
            elif "z_agent_conf" in line:
            	line = line.strip('\n')
            	line = line.lstrip("z_agent_conf")
            	z_data.append(line.strip(' '))
        return z_data
#####################End#############################

#####################################################
#  Function reads the agentd.conf file and returns  #
#  Server, ServerActive, Hostname                   #
# input:  path to zabbix_agentd.conf file           #
# output:  list [Server, ServerActive, Hostname ]   #
#####################################################
def z_info(name):
        datafile = file(name)
        z_data = []
        for line in datafile:
            if "#" in line:
                continue  
            elif "Server" in line:
            	line = line.strip('\n')
            	line = line.lstrip("Server=")
            	z_data.append(line.strip(' '))
            elif "ServerActive" in line:
            	line = line.strip('\n')
            	line = line.lstrip("ServerActive=")
            	z_data.append(line.strip(' '))
            elif "Hostname" in line:
            	line = line.strip('\n')
            	line = line.lstrip("Hostname=")
            	z_data.append(line.strip(' '))
        return z_data
#####################End#############################

#####################################################
#  Function connects to Zabbix Server               #
# input:  void                                      #
# output:  Boolean                                  #
#####################################################
def z_logging():
        
        status = None
        zabbix_info = []
        zagent_info = []
        zabbix_info = z_log_info('jmp.properties')
        print zabbix_info
        zagent_info = z_info(zabbix_info[2])
        print zagent_info
        zabbix_server_username=zabbix_info[0]
        zabbix_server_password=zabbix_info[1]
        zabbix_server_url='http://'+ zagent_info[0] + '/zabbix'
        print zabbix_server_url
        z=zabbix_api.ZabbixAPI(server=zabbix_server_url)
        z.login(user=zabbix_server_username, password=zabbix_server_password)
        return z
#####################End#############################


# Connect to Zabbix server
hostgroup='JasperServers'
#z=zabbix_api.ZabbixAPI(server=zabbix_url)
#z.login(user=username, password=password)
#if z.test_login():
#	print 'Auth is working'
#else:
#	print 'Auth did not work'
z = z_logging()
if z.test_login():
	print 'Auth is working'
else:
	print 'Auth did not work'
print z.api_version()
# Get hosts in JasperServer group to check for JTA-Server and JSB-Server
#First check if JasperServer Hostgroup is there?
hostgroups = z.hostgroup.get(
    {
    #'filter': { 'name': hostgroup}, 
    'output': 'extend'
    })
print hostgroups
for item in hostgroup:
	if "JasperServers":
		print "JasperServers exist"
		#Check if ant JSB and JTA Servers host exist
		break
	else:
		print "JasperServer hostgroup is nothere Goto create one"

#groupID = hostgroups[0]['groupid']
#print hostgroups[0]['groupid']
print "---------------------------"
#hosts = z.host.get(
 #   {
  #  'filter': { 'groupid': groupID}, 
   # 'output': 'extend'
    #})
#print hosts 
#print "---------------------------"
