#! /usr/bin/env python
#####################################################
#  Zabbix rleated operations: login, check hosts,   #
#  update hosts, update applicaitons                #
#####################################################

import zabbix_api
import socket
import os
import sys
import json
import socket
import logging
import constants
from zabbix_api import ZabbixAPI, ZabbixAPIException

#####################################################
#  Function reads the jmp.properties file and       #
#  returns username,password, agent.conf path       #
# input:  path to jmp.properties file               #
# output:  list [username, password, path ]         #
#####################################################
def jmp_info(name):
        datafile = file(name)
        if not datafile:
            logging.error('file was not found')
        else:
            z_data = {}
            logging.info('file was found')
            for line in datafile:
                if "#" in line:
                    continue
                elif "jmpEnabled" in line:
                    line = line.strip('\n')
                    line = line.split("jmpEnabled=")
                    z_data['jmpEnabled'] = line[1]
                elif "username" in line:
                    line = line.strip('\n')
                    line = line.split("username=")
                    z_data['username'] = line[1]
                elif "password=" in line:
                    line = line.strip('\n')
                    line = line.split("password=")
                    z_data['password'] = line[1]
                elif "jsb_z_agent_conf" in line:
                    line = line.strip('\n')
                    line = line.split("jsb_z_agent_conf=")
                    z_data['jsb_z_agent_conf'] = line[1]
                elif "jta_z_agent_conf" in line:
                    line = line.strip('\n')
                    line = line.split("jta_z_agent_conf=")
                    z_data['jta_z_agent_conf'] = line[1]
                elif "jmp_template" in line:
                    line = line.strip('\n')
                    line = line.split("jmp_template=")
                    z_data['jmp_template'] = line[1]
                elif "jasper_home" in line:
                    line = line.strip('\n')
                    line = line.split("jasper_home=")
                    z_data['jasper_home'] = line[1]
                elif "jsb.jmxremote" in line:
                    line = line.strip('\n')
                    line = line.split("jsb.jmxremote=")
                    z_data['jsb.jmxremote'] = line[1]
                elif "jsbHostGroup" in line:
                    line = line.strip('\n')
                    line = line.split("jsbHostGroup=")
                    z_data['jsbHostGroup'] = line[1]
                elif "jtaHostGroup" in line:
                    line = line.strip('\n')
                    line = line.split("jtaHostGroup=")
                    z_data['jtaHostGroup'] = line[1]
                elif "jtaHostName" in line:
                    line = line.strip('\n')
                    line = line.split("jtaHostName=")
                    z_data['jtaHostName'] = line[1]
                elif "jsbHostName" in line:
                    line = line.strip('\n')
                    line = line.split("jsbHostName=")
                    z_data['jsbHostName'] = line[1]
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
        z_data = {}
        for line in datafile:
            if "#" in line:
                continue  
            elif "Server=" in line:
                line = line.strip('\n')
                line = line.split("Server=")
                z_data['Server'] = line[1]
            elif "ServerActive=" in line:
                line = line.strip('\n')
                line = line.split("ServerActive=")
                z_data['ServerActive'] = line[1]
            elif "Hostname=" in line:
                line = line.strip('\n')
                line = line.split("Hostname=")
                z_data['Hostname'] = line[1]
        return z_data
#####################End#############################
#####################################################
#  Function connects to Zabbix Server               #
# input:  void                                      #
# output:  Boolean                                  #
#####################################################
def z_logging():        
        status = None
        zabbix_info = {}
        zagent_info = {}
        zabbix_info = jmp_info('mule_zabbix.properties')
        #print zabbix_info
        logging.debug(zabbix_info)
        zagent_info = z_info(zabbix_info['jsb_z_agent_conf'])
        #print zagent_info
        logging.debug(zagent_info)
        zabbix_server_username=zabbix_info['username']
        zabbix_server_password=zabbix_info['password']
        zabbix_server_url='http://'+ zagent_info['Server'] + '/zabbix'
        #print zabbix_server_url
        logging.debug(zabbix_server_url)
        z=zabbix_api.ZabbixAPI(server=zabbix_server_url)
        z.login(user=zabbix_server_username, password=zabbix_server_password)
        return z
#####################End#############################
#####################################################
#  Function Check for the JapserServer Hostgroup    #
# input:  Zabbix Handle                             #
# output:  True or false                            #
#####################################################
def z_checkHostgroup(zabbix_handler, hostGroupName):        
        hostgroups = zabbix_handler.hostgroup.get(
        {
        #'filter': { 'name': hostgroup}, 
        'output': 'extend'
        })
        print hostgroups
        for item in hostgroup:
                if hostGroupName:
                    print "JasperServers exist"
                    return True
                else:
                    #print "JasperServer hostgroup is not there, talk to your system Administrator"
                    logging.debug("JasperServer hostgroup is not there, talk to your system Administrator")
                    return False
#####################End#############################
#####################################################
#  Function Check for JTA JMX Template templateid   #
# input:  Zabbix Handle , Template name             #
# output:  TemplateID if template exist             #
#####################################################
def get_jta_templateid(zabbix_handler, template_name):
        jta_template = zabbix_handler.template.get(
            {
            'filter': { 'name': template_name}, 
            'output': 'extend'
            })
        #print "JTA TEMPLATE ID IS"
        #print jta_template[0]['templateid']
        logging.info("JTA Template id is for"+ template_name)
        logging.info(jta_template[0]['templateid'])
        return jta_template[0]['templateid']
#####################End#############################
#####################################################
#  Function Check for zabbix \   version            #
# input:  Zabbix Handle , Template name             #
# output:  Zabbix verison                           #
#####################################################
def get_zabbix_api_version(zabbix_handler):
            print zabbix_handler.api_version()
#####################End#############################

#####################################################
#  Function Check for JasperServer group            #
# input:  Zabbix Handle , HostGroupName             #
# output:  GroupID                                  #
#####################################################
#Check for HostGroup JasperServer or what ever the name is for JTA hosts
def get_jasper_groupid(zabbix_handler,groupName):
        hostgroups = zabbix_handler.hostgroup.get(
            {
            'output': 'extend'
            })
        print hostgroups
        for item in hostgroups:
            #item = [s.encode('utf-8') for s in item]
            print item['name']
            if item['name'] == "JasperServers":
                print item['groupid']
                logging.debug('JasperServers is found')
                return item['groupid']
            else:
                continue    
        print "can't find JasperServers Group"
        logging.debug('Cannot find JasperServers Group please check your Zabbix installation')
        logging.debug('#####################################################################')
        return 0
#####################End#############################
#####################################################
#  Function get the hosts list for jTA's group      #
# input:  Zabbix Handle , HostGroupName             #
# output:  GroupID                                  #
##################################################### 
def get_jasperhosts(zabbix_handler,hostsgroupID):
        jta_apps_hosts = []
        hosts = zabbix_handler.host.get(
            {
            'filter': { 'groupid': hostsgroupID}, 
            'output': 'extend'
            })
        for item in hosts:
            if "jta" in item['host']:
                #print item['host']
                #print item['hostid']
                jta_apps_hosts.append(item['host'].strip('\n'))
        jta_apps_hosts = [s.encode('utf-8') for s in jta_apps_hosts]
        logging.debug('#####################################################')
        logging.debug(jta_apps_hosts)
        return jta_apps_hosts
#####################End#############################
#####################################################
#  Function retrive the host interface info for JTA #
# input:  Zabbix Handle , HostGroupName             #
# output:  Interface object                         #
##################################################### 
def get_hostinterface(zabbix_handler,hostsgroupID):
        hosts = zabbix_handler.host.get(
            {
            'filter': { 'groupid': hostsgroupID}, 
            'output': 'extend'
            })
        for item in hosts:
            if "jta" in item['host']:
                #print item['host']
                #print item['hostid']
                interface = zabbix_handler.hostinterface.get(
                {
                'filter': { 'hostid': item['hostid']}, 
                'output': 'extend'
                })
        #logging.debug('#####################################################')
        #logging.debug(jta_apps_hosts)
        return interface
#####################End#############################
#####################################################
#  Function retrive the host interface info for     #
#  any host                                         #
# input:  Zabbix Handle , HostID                    #
# output:  interface object                         #
##################################################### 
def get_interface(zabbix_handler,hostID):
        interface = zabbix_handler.hostinterface.get(
                {
                'filter': { 'hostid': hostID}, 
                'output': 'extend'
                })
        #logging.debug('#####################################################')
        #logging.debug(jta_apps_hosts)
        return interface
#####################End#############################
#####################################################
#  Function retrive the Application ID for JTA-Logs #
#  any host                                         #
# input:  Zabbix Handle , HostID                    #
# output:  interface object                         #
##################################################### 
def get_jta_log_applicaitonID(zabbix_handler,HostID):
        applicaitonID = zabbix_handler.application.get(
        {
        'hostids':HostID,
        'filter': { 'name': 'JTA-Logs'}, 
        'output': 'extend'
        })
        #print"######applicaiton id##############"
        #print applicaitonID
        #print applicaitonID[0]['applicationid']
        logging.debug("######applicaiton id##############")
        logging.debug(applicaitonID)
        logging.debug(applicaitonID[0]['applicationid'])
        return applicaitonID[0]['applicationid']
#####################End#############################
#####################################################
#  Function retrive the Application ID for JTA-Logs #
#  any host                                         #
# input:  Zabbix Handle , HostID                    #
# output:  interface object                         #
##################################################### 
def get_jta_applicaiton_list(zabbix_handler,HostID,keyword):
        jta_applicaiton_list=[]
        applicaitons = zabbix_handler.application.get(
        {
        'hostids':HostID,
        #'filter': { 'name': keyword}, 
        'output': 'extend'
        })
        for item in applicaitons:
             if keyword in item['name']:
                #print item['host']
                #print item['hostid']
                jta_applicaiton_list.append(item['name'].strip('\n'))
        jta_applicaiton_list = [s.encode('utf-8') for s in jta_applicaiton_list]
        #print jta_applicaiton_list
        logging.debug("######JTA applicaiton List##############")
        logging.debug(jta_applicaiton_list)
        return jta_applicaiton_list
#####################End#############################
#####################################################
#  Function to add items for the JTA application #
# input:  Zabbix Handle , HostGroupName             #
# output:  Interface object                         #
##################################################### 
def add_jta_jmx_items(zabbix_handler,jmx_item,jmx_interface, jmx_applicationID, jasper_hostID): 
            #####################################################
            #Create items for the JTA-JMX application-1
            #####################################################
            #jta_jmx_interfaceID = jmp_zabbix.get_interface(z,jta_server_hostID)
            print"##########Jasoer_HOstID#######"
            print jasper_hostID
            item_name = "JTA-JEC Connector Status"
            # jmx["{$JTANAME}:type=Connector,name=\"JEC.1\"",Started]
            key_value = 'jmx["Mule.' + jmx_item + ':type=Connector,name=\\"JEC.1\\"",Started]'
            print"######keyvalue##############"
            print key_value
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'3',
                'data_type':'3',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            print "###############Jasper_itemID 1##################"
            print jasper_itemID
            #####################################################
            #Create items for the JTA-JMX application-2
            #####################################################
            # jta_jmx_interfaceID = jmp_zabbix.get_interface(z,jta_server_hostID)
            item_name = "JTA AsyncEventsReceived"
            #jmx["{$JTANAME}:type=org.mule.Statistics,Application=application totals",AsyncEventsReceived]
            key_value = 'jmx["Mule.' + jmx_item + ':type=org.mule.Statistics,Application=application totals",AsyncEventsReceived]'
            print"######keyvalue##############"
            print key_value
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'3',
                'data_type':'0',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            print "###############Jasper_itemID 2##################"
            print jasper_itemID
            #####################################################
            #Create items for the JTA-JMX application-3
            #####################################################
            # jta_jmx_interfaceID = jmp_zabbix.get_interface(z,jta_server_hostID)
            item_name = "JTA AverageProcessingTime"
            #jmx["{$JTANAME}:type=org.mule.Statistics,Application=application totals",AverageProcessingTime]
            key_value = 'jmx["Mule.' + jmx_item + ':type=org.mule.Statistics,Application=application totals",AverageProcessingTime]'
            print"######keyvalue##############"
            print key_value
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'3',
                'data_type':'0',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            print "###############Jasper_itemID 3##################"
            print jasper_itemID
            #####################################################
            #Create items for the JTA-JMX application-4
            #####################################################
            # jta_jmx_interfaceID = jmp_zabbix.get_interface(z,jta_server_hostID)
            item_name = "JTA ExecutionErrors"
            #jmx["Mule.jtaDemo-client-aircrafts-1.1:type=org.mule.Statistics,Application=application totals",ExecutionErrors]
            key_value = 'jmx["Mule.' + jmx_item + ':type=org.mule.Statistics,Application=application totals",ExecutionErrors]'
            print"######keyvalue##############"
            print key_value
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'3',
                'data_type':'0',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
               'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            print "###############Jasper_itemID 4##################"
            print jasper_itemID
            #####################################################
            #Create items for the JTA-JMX application-5
            #####################################################
            # jta_jmx_interfaceID = jmp_zabbix.get_interface(z,jta_server_hostID)
            item_name = "JTA FatalErrors"
            #jmx["Mule.jtaDemo-client-aircrafts-1.1:type=org.mule.Statistics,Application=application totals",FatalErrors]
            key_value = 'jmx["Mule.' + jmx_item + ':type=org.mule.Statistics,Application=application totals",FatalErrors]'
            print"######keyvalue##############"
            print key_value
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'3',
                'data_type':'0',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            print "###############Jasper_itemID 5##################"
            print jasper_itemID
            #####################################################
            #Create items for the JTA-JMX application-6
            #####################################################
            # jta_jmx_interfaceID = jmp_zabbix.get_interface(z,jta_server_hostID)
            item_name = "JTA Free Memory"
            #jmx[Mule.jtaDemo-client-aircrafts-1.1:name=MuleContext,FreeMemory]
            key_value = 'jmx[Mule.' + jmx_item + ':name=MuleContext,FreeMemory]'
            print"######keyvalue##############"
            print key_value
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'3',
                'data_type':'0',
                'units':'M Bytes',
                'formula':'0.000001',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            print "###############Jasper_itemID 6##################"
            print jasper_itemID
            #####################################################
            #Create items for the JTA-JMX application-7
            #####################################################
            # jta_jmx_interfaceID = jmp_zabbix.get_interface(z,jta_server_hostID)
            item_name = "JTA Host IP"
            #jmx[Mule.jtaDemo-client-aircrafts-1.1:name=MuleContext,HostIp]
            key_value = 'jmx[Mule.' + jmx_item + ':name=MuleContext,HostIp]'
            print"######keyvalue##############"
            print key_value
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'4',
                'data_type':'0',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            print "###############Jasper_itemID 7##################"
            print jasper_itemID
            #####################################################
            #Create items for the JTA-JMX application-8
            #####################################################
            # jta_jmx_interfaceID = jmp_zabbix.get_interface(z,jta_server_hostID)
            item_name = "JTA Host Name"
            #jmx[Mule.jtaDemo-client-aircrafts-1.1:name=MuleContext,Hostname]
            key_value = 'jmx[Mule.' + jmx_item + ':name=MuleContext,Hostname]'
            print"######keyvalue##############"
            print key_value
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'3',
                'data_type':'4',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            print "###############Jasper_itemID 8##################"
            print jasper_itemID
             #####################################################
            #Create items for the JTA-JMX application-9
            #####################################################
            #jta_jmx_interfaceID = jmp_zabbix.get_interface(z,jta_server_hostID)
            item_name = "JTA InstanceId"
            #jmx[Mule.jtaDemo-client-aircrafts-1.1:name=MuleContext,HostIp]
            key_value = 'jmx[Mule.' + jmx_item + ':name=MuleContext,InstanceId]'
            print"######keyvalue##############"
            print key_value
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'4',
                'data_type':'0',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            print "###############Jasper_itemID 9##################"
            print jasper_itemID
             #####################################################
            #Create items for the JTA-JMX application-10
            #####################################################
            #jta_jmx_interfaceID = jmp_zabbix.get_interface(z,jta_server_hostID)
            item_name = "JTA JdkVersion"
            #jmx[Mule.jtaDemo-client-aircrafts-1.1:name=MuleContext,JdkVersion]
            key_value = 'jmx[Mule.' + jmx_item + ':name=MuleContext,JdkVersion]'
            print"######keyvalue##############"
            print key_value
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'4',
                'data_type':'0',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            print "###############Jasper_itemID 10##################"
            print jasper_itemID
             #####################################################
            #Create items for the JTA-JMX application-11
            #####################################################
            #jta_jmx_interfaceID = jmp_zabbix.get_interface(z,jta_server_hostID)
            item_name = "JTA Max Memory"
            #jmx[Mule.jtaDemo-client-aircrafts-1.1:name=MuleContext,MaxMemory]
            key_value = 'jmx[Mule.' + jmx_item + ':name=MuleContext,MaxMemory]'
            print"######keyvalue##############"
            print key_value
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'3',
                'data_type':'0',
                'units':'M Bytes',
                'formula':'0.000001',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            print "###############Jasper_itemID 11##################"
            print jasper_itemID
             #####################################################
            #Create items for the JTA-JMX application-12
            #####################################################
            #jta_jmx_interfaceID = jmp_zabbix.get_interface(z,jta_server_hostID)
            item_name = "JTA MaxProcessingTime"
            #jmx[Mule.jtaDemo-client-aircrafts-1.1:type=org.mule.Statistics,Application=application totals",MaxProcessingTime]
            key_value = 'jmx["Mule.' + jmx_item + ':type=org.mule.Statistics,Application=application totals",MaxProcessingTime]'
            print"######keyvalue##############"
            print key_value
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'3',
                'data_type':'0',
                'units':'Micro Second per event',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            print "###############Jasper_itemID 12##################"
            print jasper_itemID
             #####################################################
            #Create items for the JTA-JMX application-13
            #####################################################
            #jta_jmx_interfaceID = jmp_zabbix.get_interface(z,jta_server_hostID)
            item_name = "JTA MinProcessingTime"
            #jmx[Mule.jtaDemo-client-aircrafts-1.1:type=org.mule.Statistics,Application=application totals",MinProcessingTime]
            key_value = 'jmx["Mule.' + jmx_item + ':type=org.mule.Statistics,Application=application totals",MinProcessingTime]'
            print"######keyvalue##############"
            print key_value
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'3',
                'data_type':'0',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            print "###############Jasper_itemID 13##################"
            print jasper_itemID
             #####################################################
            #Create items for the JTA-JMX application-14
            #####################################################
            #jta_jmx_interfaceID = jmp_zabbix.get_interface(z,jta_server_hostID)
            item_name = "JTA ProcessedEvents"
            #jmx[Mule.jtaDemo-client-aircrafts-1.1:name=MuleContext,HostIp]
            key_value = 'jmx["Mule.' + jmx_item + 'type=org.mule.Statistics,Application=application totals",ProcessedEvents]'
            print"######keyvalue##############"
            print key_value
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'3',
                'data_type':'0',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            print "###############Jasper_itemID 14##################"
            print jasper_itemID
             #####################################################
            #Create items for the JTA-JMX application-15
            #####################################################
            #jta_jmx_interfaceID = jmp_zabbix.get_interface(z,jta_server_hostID)
            item_name = "JTA Stopped"
            #jmx[Mule.jtaDemo-client-aircrafts-1.1:name=MuleContext,Stopped]
            key_value = 'jmx[Mule.' + jmx_item + ':name=MuleContext,Stopped]'
            print"######keyvalue##############"
            print key_value
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'3',
                'data_type':'0',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            print "###############Jasper_itemID 15##################"
            print jasper_itemID
             #####################################################
            #Create items for the JTA-JMX application-16
            #####################################################
            #jta_jmx_interfaceID = jmp_zabbix.get_interface(z,jta_server_hostID)
            item_name = "JTA SyncEventsReceived"
            #jmx[Mule.jtaDemo-client-aircrafts-1.1:type=Application,name=\"application totals\"",SyncEventsReceived]
            key_value = 'jmx["Mule.' + jmx_item + ':type=Application,name=\\"application totals\\"",SyncEventsReceived]'
            print"######keyvalue##############"
            print key_value
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'3',
                'data_type':'0',
                'formula':'1',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            print "###############Jasper_itemID 16##################"
            print jasper_itemID
            #####################################################
            #Create items for the JTA-JMX application-17
            #####################################################
            #jta_jmx_interfaceID = jmp_zabbix.get_interface(z,jta_server_hostID)
            item_name = "JTA TotalEventsReceived"
            #jmx[Mule.jtaDemo-client-aircrafts-1.1:name=MuleContext,HostIp]
            key_value = 'jmx["Mule.' + jmx_item + ':type=org.mule.Statistics,Application=application totals",TotalEventsReceived]'
            print"######keyvalue##############"
            print key_value
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'3',
                'data_type':'0',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            print "###############Jasper_itemID 17##################"
            print jasper_itemID
            #####################################################
            #Create items for the JTA-JMX application-18
            #####################################################
            #jta_jmx_interfaceID = jmp_zabbix.get_interface(z,jta_server_hostID)
            item_name = "JTA Total Memory"
            #jmx[Mule.jtaDemo-client-aircrafts-1.1:name=MuleContext,HostIp]
            key_value = 'jmx[Mule.' + jmx_item + ':name=MuleContext,TotalMemory]'
            print"######keyvalue##############"
            print key_value
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'3',
                'data_type':'0',
                'formula':'0.000001',
                'units':'M Bytes',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            print "###############Jasper_itemID 18##################"
            print jasper_itemID
             #####################################################
            #Create items for the JTA-JMX application-19
            #####################################################
            #jta_jmx_interfaceID = jmp_zabbix.get_interface(z,jta_server_hostID)
            item_name = "JTA TotalProcessingTime"
            #jmx[Mule.jtaDemo-client-aircrafts-1.1:name=MuleContext,HostIp]
            key_value = 'jmx["Mule.' + jmx_item + ':type=org.mule.Statistics,Application=application totals",TotalProcessingTime]'
            print"######keyvalue##############"
            print key_value
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'3',
                'units':'sec',
                'formula':'0.000001',
                'data_type':'0',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            print "###############Jasper_itemID 19##################"
            print jasper_itemID
            return True
#####################End#############################





