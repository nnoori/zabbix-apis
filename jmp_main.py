#! /usr/bin/env python
#####################################################
#  Test script for detecting JSB and add Zabbix     #
#  Host, Log items, screens                         #
#####################################################
import logging
import zabbix_api
import socket
import os
import sys
import json
import socket
import jmp_constants
from zabbix_api import ZabbixAPI, ZabbixAPIException
import jmp_zabbix
import jta_checker

#####################################################
#Set the log level and log file name
#####################################################
a = logging.basicConfig(filename='auto_discoverlog.log',level=logging.DEBUG)
logging.debug('Auto-discovery started running')

#####################################################
#  Log onto Zabbix                                  #
#####################################################
zabbix_info = jmp_zabbix.jmp_info('jmp.properties')
print "##########Zabbix_info#########"
print zabbix_info
print zabbix_info['jtaHostName']
z = jmp_zabbix.z_logging()
if z.test_login():
	#print 'Auth is working'
    logging.debug('authorized and gained access to zabbix')
else:
	#print 'Auth did not work'
    logging.debug(' no authorization nor gain access to zabbix')

hostgroup='JasperServers'
jasper_groupid = jmp_zabbix.get_jasper_groupid(z,hostgroup)
jta_list_hosts = jmp_zabbix.get_jasperhosts(z,jasper_groupid)
#print '###################HostList########################'
#print jta_list_hosts
logging.debug('###################HostList########################')    
logging.debug(jta_list_hosts)   

deployed_jta_list = jta_checker.get_apps_diff()
#host_interface = jmp_zabbix.get_hostinterface(z,jasper_groupid)
#print '###################deployed_apps########################'
#print deployed_jta_list['deployed_apps']
logging.debug('###################deployed_apps########################')
logging.debug(deployed_jta_list['deployed_apps'])

#####################################################
# Get the list of JTA applicaitons under           #
# JTA server host == JTA-jasperServer-a             #
#####################################################
host_jta_server = z.host.get(
        {
        'filter': { 'host': zabbix_info['jtaHostName']}, 
        'output': 'extend'
        })
jta_server_hostID=host_jta_server[0]['hostid']
host_interface = jmp_zabbix.get_interface(z,jta_server_hostID)
log_interfaceID = jmp_zabbix.get_interface(z,jta_server_hostID)
print "list of interfaces \n"
print log_interfaceID
#####################################################
#  Check for the JTA's and add the missing ones     #
#####################################################
deployed_jta_applicaiton_list = jmp_zabbix.get_jta_applicaiton_list(z,jta_server_hostID,"jta")
print deployed_jta_applicaiton_list
if not deployed_jta_list['deployed_apps']:
    print "list empty noting to update \n"
else: 
    #start adding JTA hosts
    for item in deployed_jta_list['deployed_apps']:
        if item in deployed_jta_applicaiton_list:
            print item
            print "\n Item is already added"
            logging.debug(item)
            logging.debug("\n Item is already added")
            continue 
        else:
            #####################################################
            # Add log items and the screens to display
            # get host id
            #####################################################
            information = jmp_zabbix.z_info(zabbix_info['jsb_z_agent_conf'])
            print "##############Information####################"
            print information
            #####################################################
            # Add log item for the JTA-Log applicaiton
            #####################################################
            jta_log_applicaitonID = jmp_zabbix.get_jta_log_applicaitonID(z,jta_server_hostID)
            print "######LOG-ApplicaitonID##############"
            print jta_log_applicaitonID
                    
            #####################################################
            #Get interface ID
            #####################################################
            jta_interfaceID = jmp_zabbix.get_interface(z,jta_server_hostID)
            print "######Interface ID##############"
            print jta_interfaceID
            print jta_interfaceID[0]['interfaceid']
            #####################################################
            #Add log item to JTA_log applicaiotn in jasperServer-a
            #####################################################
            item_name = item + "-log"
            key_value = "log[{$JTA_SVR_PATH}/logs/" + item + ".log]"
            print "######Key value##############"
            print key_value
            jasper_itemID = z.item.create({
                'name':item_name,
                'key_':key_value,
                'type':'7',
                'interfaceid':jta_interfaceID[0]['interfaceid'],
                'applications':[jta_log_applicaitonID],
                'hostid':jta_server_hostID,
                'value_type':'2',
                'delay':'10'
                })
            #####################################################
            # Create screen for the new JTA log
            ####################################################
            jta_screen_name = item + 'logs'
            JTA_log_screenID = z.screen.get(
            {
            'selectScreenItems':'extend',
            'filter': { 'name': jta_screen_name}, 
            'output': 'extend'
            })
            print JTA_log_screenID
            screen_name = item + " log"
            jta_log_screen = z.screen.create({
                'name':screen_name,
                'hsize':'1',
                'vsize':'1',
                })
            jta_log_screen['screenids'] = [s.encode('utf-8') for s in jta_log_screen['screenids']]
            print "#############ScreenID################"
            print jta_log_screen['screenids'][0]

            #####################################################
            # Add new application to JTA-jasperServer-a host
            #####################################################
            jta_jmx_application_name = item+"-JMX"
            new_jta_application = z.application.create({
                'name':jta_jmx_application_name,
                'hostid':jta_server_hostID
                })
            print "###### NEW applicaiton id##############"
            print new_jta_application

            new_jta_application['applicationids'] = [s.encode('utf-8') for s in new_jta_application['applicationids']]
            new_jta_applicationID = new_jta_application['applicationids'][0]
            print new_jta_applicationID
            print jta_interfaceID[1]['interfaceid']
            jta_jmx_interfaceID = jta_interfaceID[1]['interfaceid']
            #jmp_zabbix.get_interface(z,jta_server_hostID)
            jmp_zabbix.add_jta_jmx_items(z,item,jta_jmx_interfaceID,new_jta_applicationID,jta_server_hostID)




  

