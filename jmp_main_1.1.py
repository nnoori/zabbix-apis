#! /usr/bin/env python
#####################################################
# Test script for detecting JSB and add Zabbix #
# Host, Log items, screens #
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
#####################################################
#Set the log level and set the file for the auto-discovery
a = logging.basicConfig(filename='auto_discoverlog.log',level=logging.DEBUG)
logging.debug('Auto-discovery started running')

#####################################################
#####################################################

zabbix_info = jmp_zabbix.jmp_info('jmp.properties')
#####################################################
# Jasper HostGroup for 1.1 MGMT Platform
#####################################################
hostgroup='JasperServers'

z = jmp_zabbix.z_logging()
if z.test_login():
    #print 'Auth is working'
    logging.debug('authorized and gained access to zabbix')
else:
    #print 'Auth did not work'
    logging.debug(' no authorization nor gain access to zabbix')

#####################################################
# Get GroupID and check for JTA hosts
#####################################################
jasper_groupid = jmp_zabbix.get_jasper_groupid(z,hostgroup)
jta_list_hosts = jmp_zabbix.get_jasperhosts(z,jasper_groupid)
#print '###################JTA-HostList########################'
#print jta_list_hosts
logging.debug('###################JTA-HostList########################')
logging.debug(jta_list_hosts)       

jta_templateID = jmp_zabbix.get_jta_templateid(z,"JTA JMX Template")
deployed_jta_list = jta_checker.get_apps_diff()
host_interface = jmp_zabbix.get_hostinterface(z,jasper_groupid)

#print '###################Deployed_JTA_apps########################'
#print deployed_jta_list['deployed_apps']
logging.debug('###################Deployed_JTA_apps########################')
logging.debug(deployed_jta_list['deployed_apps'])

if not deployed_jta_list['deployed_apps']:
    #print "list empty noting to update \n"
    logging.debug("list empty noting to update \n")
else:
    #####################################################
    #start adding JTA hosts
    #####################################################
    for item in deployed_jta_list['deployed_apps']:
        if item in jta_list_hosts:
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
            z.host.create({
            'host':item,
            'interfaces':{
            'type':host_interface[0]['type'],
            'main':host_interface[0]['main'],
            'useip':'0',
            'ip':'',
            'dns':host_interface[0]['dns'],
            'port':host_interface[0]['port']
            },
            'groups':[{
            'groupid':jasper_groupid
            }],
            'templates':[{
            'templateid':jta_templateID
            }]
            })
            #####################################################
            # Add log items and the screens to display
            # Get host id
            #####################################################
            information = jmp_zabbix.z_info(jmp_zabbix.jmp_info('jmp.properties')['jsb_z_agent_conf'])
            host_log = z.host.get(
            {
            'filter': { 'host': information['Hostname']},
            'output': 'extend'
            })
            print "JTA add a new host"
            logging.debug("JTA add a new host")
            #####################################################
            #Add item using host ID
            #####################################################
            JTA_log_applicaitonID = z.application.get(
            {
            'hostids':host_log[0]['hostid'],
            'filter': { 'name': 'JTA-Logs'},
            'output': 'extend'
            })
            #print"######applicaiton id##############"
            #print JTA_log_applicaitonID
            #print JTA_log_applicaitonID[0]['applicationid']
            logging.debug("######applicaiton id##############")
            logging.debug(JTA_log_applicaitonID)
            logging.debug(JTA_log_applicaitonID[0]['applicationid'])
            log_interfaceID = jmp_zabbix.get_interface(z,host_log[0]['hostid'])
            print log_interfaceID[0]['interfaceid']
            #####################################################
            #Add log item to JTA_log applicaiotn in jasperServer-a
            #####################################################
            key_value = "log[{$JTA_SVR_PATH}/logs/" + item + ".log]"
            #print"######keyvalue##############"
            #print key_value
            logging.debug("######keyvalue##############")
            logging.debug(key_value)
            z.item.create({
            'name':item,
            'key_':key_value,
            'type':'7',
            'interfaceid':log_interfaceID[0]['interfaceid'],
            'applications':[JTA_log_applicaitonID[0]['applicationid']],
            'hostid':host_log[0]['hostid'],
            'value_type':'2',
            'delay':'10'
            })
            #####################################################
            # Create screen
            #####################################################
            JTA_log_screenID = z.screen.create({
                'name':item,
                'hsize':'1',
                'vsize':'1',
                })
            #print JTA_log_screenID
            logging.debug("############JTA_log_screenID################")
            logging.debug(JTA_log_screenID)
