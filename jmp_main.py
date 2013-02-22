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
z = jmp_zabbix.z_logging()
if z.test_login():
	#print 'Auth is working'
    logging.debug('authorized and gained access to zabbix')
else:
	#print 'Auth did not work'
    logging.debug(' no authorization nor gain access to zabbix')
#####################################################
#  Get TemplateID,JasperHosts list etc              #
#####################################################
hostgroup='JasperServers'
#jta_templateID = jmp_zabbix.get_jta_templateid(z,"JTA JMX Template")
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
#  Get the list of JTA applicaitons under           #
# JTA server host == JTA-jasperServer-a             #
#####################################################
host_jta_server = z.host.get(
        {
       # 'filter': { 'host': 'jta-server-0-jmx'},
        'filter': { 'host': 'JTA-jasperServer-a'}, 
        'output': 'extend'
        })
jta_server_hostID=host_jta_server[0]['hostid']
host_interface = jmp_zabbix.get_interface(z,jta_server_hostID)
log_interfaceID1 = jmp_zabbix.get_interface(z,jta_server_hostID)
print "list of interfaces \n"
print log_interfaceID1

deployed_jta_applicaiton_list = jmp_zabbix.get_jta_applicaiton_list(z,jta_server_hostID,"jta")
print deployed_jta_applicaiton_list
#####################################################
#  Check for the JTA's and add the missing ones     #
#####################################################
if not deployed_jta_list['deployed_apps']:
    print "list empty noting to update \n"
else: 
    #start adding JTA hosts
    for item in deployed_jta_list['deployed_apps']:
        #if item in jta_list_hosts:
        if item in deployed_jta_applicaiton_list:
            #print item
            #print "\n Item is already added"
            logging.debug(item)
            logging.debug("\n Item is already added")
            continue 
        else:
            #####################################################
            # Add new host + attach tamplate (JTA JMX Template) 
            # + update macro if needed
            #####################################################
            # z.host.create({
            #     'host':item,
            #     'interfaces':{
            #     'type':host_interface[0]['type'],
            #     'main':host_interface[0]['main'],
            #     'useip':'0',
            #     'ip':'',
            #     'dns':host_interface[0]['dns'],
            #     'port':host_interface[0]['port']
            #     },
            #     'groups':[{
            #     'groupid':jasper_groupid
            #     }],
            #     'templates':[{
            #     'templateid':jta_templateID
            #     }]
            #     })
            #####################################################
            # Add new application to JTA Server host
            #####################################################
            new_jta_application = z.application.create({
                'name':item,
                'hostid':jta_server_hostID
                })
            #####################################################
            # Add new application to JTA Server host
            #####################################################
            print"######NEW applicaiton id##############"
            print new_jta_application
            new_jta_application['applicationids'] = [s.encode('utf-8') for s in new_jta_application['applicationids']]
            new_jta_applicationID = new_jta_application['applicationids'][0]
            print new_jta_applicationID

            #####################################################
            # Add log items and the screens to display
            # get host id
            #####################################################
            information = jmp_zabbix.z_info(jmp_zabbix.jmp_info('jmp.properties')['jsb_z_agent_conf'])
            # host_log = z.host.get(
            # {
            # 'filter': { 'host': information['Hostname']}, 
            # 'output': 'extend'
            # })
            # jta_log_hostID=host_log[0]['hostid']
            #print "JTA add a new host"
            logging.debug("JTA add a new host")
            #####################################################
            # Add item using host ID
            #####################################################
            
            jta_log_applicaitonID = jmp_zabbix.get_jta_log_applicaitonID(z,jta_server_hostID)
            print"######applicaiton id##############"
            print jta_log_applicaitonID
                    
            #####################################################
            #Get interface ID
            #####################################################
            log_interfaceID = jmp_zabbix.get_interface(z,host_jta_server[0]['hostid'])
            print log_interfaceID[0]['interfaceid']
            #####################################################
            #Add log item to JTA_log applicaiotn in jasperServer-a
            #####################################################
            item_name = item + "-log"
            key_value = "log[{$JTA_SVR_PATH}/logs/" + item + ".log]"
            print"######keyvalue##############"
            print key_value
            jasper_itemID = z.item.create({
                'name':item_name,
                'key_':key_value,
                'type':'7',
                'interfaceid':log_interfaceID[0]['interfaceid'],
                'applications':[jta_log_applicaitonID],
                'hostid':host_jta_server[0]['hostid'],
                'value_type':'2',
                'delay':'10'
                })
            #####################################################
            #create screen
            #####################################################
            # JTA_log_screenID = z.screen.get(
            # {
            # 'selectScreenItems':'extend',
            # 'filter': { 'name': 'jtaDemo-client-ground-vehicles logs'}, 
            # 'output': 'extend'
            # })
            # print JTA_log_screenID
            screen_name = item + " log"
            # jta_log_screen = z.screen.create({
            #     'name':screen_name,
            #     'hsize':'1',
            #     'vsize':'1',
            #     })
            # jta_log_screen['screenids'] = [s.encode('utf-8') for s in jta_log_screen['screenids']]
            # print jta_log_screen['screenids'][0]
            

         

